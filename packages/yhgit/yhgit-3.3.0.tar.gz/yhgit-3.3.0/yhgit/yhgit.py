import json
import os
import sys
from time import sleep

import runcmd
import yaml
import shutil
import sys
import ruamel.yaml
from git import Repo
import logging
import re
from urllib.parse import urlparse
from prettytable import PrettyTable, ALL
import pkg_resources  # part of setuptools
from progress.bar import Bar
import argparse

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

# 创建参数解析器
parser = argparse.ArgumentParser()

# 添加参数
parser.add_argument('-d', '--detail', type=bool, help='detail')
parser.add_argument('-m', '--modules', type=list, help='modules')


class YHModuleDependency:
    name = ''
    count = 0
    native = 0
    deplist = []
    natvielist = []

    def __init__(self, name, count, native, deplist, natvielist):
        self.name = name
        self.count = count
        self.native = native
        self.deplist = deplist
        self.natvielist = natvielist


# yaml 数据模型
class YamlModuleModel:
    module = ''
    pod = ''
    version = ''
    git = ''
    branch = ''
    tag = ''
    path = ''
    new_tag = ''
    configurations = ''
    inhibit_warnings = False
    third = False
    source = ''

    def __init__(self, module, pod, version, git, branch, tag, path, newtag, configurations, inhibit_warnings, source):
        """
        :param module:
        :param pod:
        :param version:
        :param git:
        :param branch:
        :param tag:
        :param path:
        :param newtag:
        :param configurations:
        :param inhibit_warnings:
        """
        self.module = module
        self.pod = pod
        self.git = git
        self.branch = branch
        self.tag = tag
        self.path = path
        self.new_tag = newtag
        self.configurations = configurations
        self.inhibit_warnings = inhibit_warnings
        self.source = source


# 文件状态，如果result = 1 表示成功，result = 0 表示失败 -1 表示其他异常
class ModuleStatusModel:
    module = ''
    pod = ''
    result = 0
    pod = ''
    branch = ''
    msg = ''
    tag = ''
    git = ''
    third = False
    configurations = ''
    inhibit_warnings = False
    source = None

    def __init__(self, module, pod, res, branch, msg='', tag='', git='', configurations = '', inhibit_warnings = False,source = None):
        """
        :param module: 模块名字
        :param pod: pod名字
        :param res: 结果 0 表示失败 1 表示成功 -1 表示其他异常
        :param branch: 分支
        :param msg: 错误信息
        """
        self.module = module
        self.result = res
        self.pod = pod
        self.msg = msg
        self.branch = branch
        self.tag = tag
        self.git = git
        self.configurations = configurations
        self.inhibit_warnings = inhibit_warnings
        self.source = source

# 读取yaml文件数据
def yaml_data(yaml_path):
    """
    :param yaml_path: ymal路径
    :return: 返回yaml数据
    """
    with open(yaml_path, 'r') as y:
        yaml = ruamel.yaml.YAML()
        temp_yaml = yaml.load(y.read())
        return temp_yaml


# 写入文件
def update_yaml(yaml_path, data):
    """
    :param yaml_path: yaml路径
    :param data: yaml数据
    :return: 无返回值
    """
    with open(yaml_path, "w", encoding="utf-8") as f:
        yaml = ruamel.yaml.YAML()
        yaml.dump(data, f)


# 加载yml文件
def load_yaml(data):
    """
    :param data: 读取yaml数据
    :return: 返回转换之后的模型
    """
    convertDepList = []
    for i in range(0, len(data)):
        cur_dep = data[i]
        module = YamlModuleModel(module=cur_dep.get("module", None),
                                 pod=cur_dep["pod"],
                                 version=cur_dep.get("version", None),
                                 git=cur_dep.get("git", None),
                                 branch=cur_dep.get("branch", None),
                                 tag=cur_dep.get("tag", None),
                                 path=cur_dep.get("path", None),
                                 newtag=cur_dep.get("newtag", None),
                                 configurations=cur_dep.get("configurations", None),
                                 inhibit_warnings=cur_dep.get("inhibit_warnings", False),
                                 source = cur_dep.get("source", None)
                                 )
        convertDepList.append(module)

    return convertDepList


# 删除文件
def del_path(path):
    """
    :param path: 文件路径
    :return: 无返回值
    """
    # os.listdir(path_data)#返回一个列表，里面是当前目录下面的所有东西的相对路径
    os.remove(path)


# 清空文件夹及目录
def del_dir(path):
    """
    :param path: 文件路径
    :return: 无返回值
    """
    # os.listdir(path_data)#返回一个列表，里面是当前目录下面的所有东西的相对路径
    shutil.rmtree(path)


# 清空或者创建一个新的目录
def create_file(path):
    """
    情况或者创建一个目录
    :param path: 目录
    :return:
    """
    if not os.path.exists(path):
        os.makedirs(path)
    else:
        del_dir(path)
        os.makedirs(path)


class RepoGit:
    """
    项目仓库管理
    """
    proj_path = ""
    repo = Repo

    def __init__(self, proj_path):
        """
        :param proj_path: 路径
        """
        self.proj_path = proj_path
        self.repo = Repo(path=proj_path, search_parent_directories=True)

    def most_recent_commit_message(self, branch):
        """
        当前分支最后一次的提交信息
        :return:
        """
        self.switch_branch(branch)
        commits = list(self.repo.iter_commits(branch, max_count=10))
        for commit in commits:
            message = commit.message
            if message and len(
                    message) > 0 and "Merge" not in message and "no message" not in message and "自动" not in message:
                return message, commit
        return "", ""

    def switch_branch(self, branch):
        """
        切换到新分支
        :param branch: 新分支名字
        :return:
        """
        # self.repo.head.reference = branch
        branch_list = self.repo.git.branch("-r")
        if branch in branch_list:
            self.repo.git.checkout(branch)
        else:
            self.repo.git.branch(branch)

    # 获取所有的分支
    def get_branches(self):
        """
        :return: 返回分支列表
        """
        branch_list = self.repo.git.branch("-r")
        return branch_list

    # 获取当前分支
    def getCurrentBranch(self):
        """
        :return: 当前分支
        """
        return str(self.repo.active_branch)

    # 创建新分支
    def create_branch(self, branch):
        """
        :return: 新分支名
        """
        return self.repo.create_head(branch)

    # 推送分支到远端
    def push_branch(self, branch):
        """
        :return: 新分支名
        """
        self.repo.remotes.origin.push(refspec=branch)

    # 获取当前工作目录的文件状态，是否有改动
    # True 表示有改动未提交 False表示没有改动
    def is_dirty(self):
        return self.repo.is_dirty(index=True, working_tree=True, untracked_files=True)

    # 查看文件状态
    def status(self):
        return self.repo.git.status()

    @property
    def getStatusFormatStr(self):
        cmd = ["git", "status", "-s"]
        r = runcmd.run(cmd, cwd=self.proj_path)._raise()
        lines = r.out.splitlines()
        return "\n".join(lines)

    def _startswith(self, string):
        """return a list of files startswith string"""
        cmd = ["git", "status", "-s"]
        r = runcmd.run(cmd, cwd=self.proj_path)._raise()
        lines = r.out
        lines = []
        for line in r.out.splitlines():
            if line.find(string) == 0:
                lines.append(" ".join(line.split(" ")[2:]))
        return lines

    def untracked(self):
        """return a list of untracked files"""
        return self._startswith("??")

    # 提交代码
    def commit(self, msg):
        # self.repo.index.commit(msg)
        self.repo.git.commit(m=msg)

    def add(self, files):
        self.repo.git.add(all=True)


# 获取podspec对应的版本号
def get_version_for(pod_spec_path):
    """
    获取tag版本号
    :param pod_spec_path: podspec路径
    :param new_tag: 新的tag名字
    :return:
    """
    with open(pod_spec_path, 'r', encoding="utf-8") as f:
        for line in f:
            if "s.version" in line and "s.source" not in line:
                # 获取版本号
                cur_tag = tag_with_version(line)
                return cur_tag
        f.close()
        return ""


# 重写podspec里对应的版本
def update_versionfor_podspec(pod_spec_path, new_tag):
    """
    重写podspec里对应的版本
    :param pod_spec_path: podspec路径
    :param new_tag: 新tag
    :return:
    """
    file_data = ""
    with open(pod_spec_path, 'r', encoding="utf-8") as f:
        for line in f:
            if "s.version" in line and "s.source" not in line:
                cur_tag = tag_with_version(line)
                line = line.replace(cur_tag, new_tag)
                print("修改tag " + cur_tag + " => " + new_tag)
            file_data += line
    with open(pod_spec_path, 'w', encoding="utf-8") as f:
        f.write(file_data)
        f.close()


# 获取字符串中的版本信息
def tag_with_version(version):
    """
    获取字符串中的版本信息
    :param version: 版本号
    :return:
    """
    p = re.compile(r'\d+\.(?:\d+\.)*\d+')
    vers = p.findall(version)
    ver = vers[0]
    return ver


# 根据tag自增生成新的tag
def incre_tag(tag):
    """
    tag最后一位自增
    :param tag: 原tag
    :return: 返回最后一位自增1后的tag
    """
    tags = tag.split(".")
    tag_len = len(tags)
    if tag_len > 1:
        endtag = tags[tag_len - 1]
        end_tag_num = int(endtag) + 1
        endtag = str(end_tag_num)
        tags[tag_len - 1] = endtag

    new_tag = ".".join(tags)
    return new_tag


def get_filename(url_str):
    """
    获取路径中的文件名
    :param url_str: 文件路径
    :return: 返回文件名
    """
    url = urlparse(url_str)
    i = len(url.path) - 1
    while i > 0:
        if url.path[i] == '/':
            break
        i = i - 1
    folder_name = url.path[i + 1:len(url.path)]
    if not folder_name.strip():
        return False
    if ".git" in folder_name:
        folder_name = folder_name.replace(".git", "")
    return folder_name


# 判断两个版本的大小，去除小数点，变为整数数组，依次比较大小1
# 2.2.3 = [2, 2, 3]
# 2.2.10 = [2, 2, 10]  2.2.10 > 2.2.3
# 相等返回0， v1 > v2 返回 1 v1 < v2 返回 -1
def compare_version(v1, v2):
    """
    比较两个tag， 判断两个版本的大小，去除小数点，变为整数数组，依次比较大小1
    :param v1: v1 tag入参
    :param v2:  v2 tag 入参
    :return: 相等返回0， v1 > v2 返回 1 v1 < v2 返回 -1
    """
    v1_list = v1.split(".")
    v2_list = v2.split(".")
    max_len = max(len(v1_list), len(v2_list))
    idx = 0
    while idx < max_len:
        c_v1 = 0
        c_v2 = 0
        if len(v1_list) > idx:
            c_v1 = int(v1_list[idx])
        if len(v2_list) > idx:
            c_v2 = int(v2_list[idx])
        if c_v2 > c_v1:
            return -1
        else:
            return 1
        idx += 1
    return 0


# 写入文件
def update_yaml(yaml_path, data):
    """
    :param yaml_path: yaml路径
    :param data: yaml数据
    :return: 无返回值
    """
    with open(yaml_path, "w", encoding="utf-8") as f:
        yaml = ruamel.yaml.YAML()
        yaml.dump(data, f)


# 更新podfileModule文件
def update_module_files(yaml_path, local_yaml_path, branch_result, n_branch, modules_name):
    """
    更新ymal文件，修改本地依赖和分支依赖
    :param yaml_path: PodfileModule路径
    :param local_yaml_path: PodfileLocal路径
    :param branch_result: 操作成功的模块列表
    :param n_branch: 新分支名
    :param modules_name: 模块仓库的父路径默认为modules
    :return:
    """
    # 获取ymal 数据
    podfile_module_data = yaml_data(yaml_path)
    dependenceList = []
    if "dependencies" in podfile_module_data:
        local_dependenceList = podfile_module_data["dependencies"]
        if local_dependenceList:
            dependenceList = local_dependenceList

    before_branch = ''
    if "branch" in podfile_module_data:
        before_branch = podfile_module_data['branch']
    # 转换成模型数组
    conver_deplist = load_yaml(dependenceList)

    index = 0
    for a in conver_deplist:
        for mo_re in branch_result:
            if a.module and mo_re.module and a.module == mo_re.module and mo_re.result == 1:
                module_dict = {"module": mo_re.module, "pod": a.pod, "git": a.git, "branch": n_branch,
                               "configurations": a.configurations,
                               "inhibit_warnings": a.inhibit_warnings}
                dependenceList[index] = module_dict
        index += 1
    # print("convert=======" + str(dependenceList))
    except_list = [
        module for module in branch_result if ((module.result == 1) and (module.module not in [
            pod.module for pod in conver_deplist]))]
    if len(except_list) > 0:
        for mo_re in except_list:
            module_dict = {
                "module": mo_re.module,
                "pod": mo_re.pod,
                "git": mo_re.git,
                "branch": n_branch
            }
            dependenceList.append(module_dict)

    # print("except_list=======" + str(dependenceList))
    if not (before_branch and len(before_branch) > 0):
        before_branch = n_branch
    podfile_data = {"version": "1.0.0", "branch": str(before_branch), "dependencies": dependenceList}
    update_yaml(yaml_path, podfile_data)

    after_convert = []
    if not os.path.exists(local_yaml_path):
        shutil.copy(yaml_path, local_yaml_path)  # 复制文件
        for mo_re in branch_result:
            if mo_re.result == 1:
                module_dict = {"module": mo_re.module, "pod": mo_re.module, "path": modules_name + "/" + mo_re.module}
                after_convert.append(module_dict)
        local_module_data = {"version": "1.0.0", "branch": str(n_branch), "dependencies": after_convert}
        save_dict_to_yaml(local_module_data, local_yaml_path)

    else:
        # 获取ymal 数据
        local_module_data = yaml_data(local_yaml_path)
        local_dependenceList = []
        conver_deplist = []
        if local_module_data:
            if "dependencies" in local_module_data:
                local_dependenceList = local_module_data["dependencies"]
            if not local_dependenceList:
                local_dependenceList = []
            # 转换成模型数组
            conver_deplist = load_yaml(local_dependenceList)
        # debugInfo(str([a.module for a in conver_deplist]))
        # debugInfo(str([a.module for a in branch_result]))
        except_list = [
            module for module in branch_result if ((module.result == 1) and (module.module not in [
                pod.module for pod in conver_deplist]))]
        # debugInfo(str([a.module for a in except_list]))
        if len(except_list) > 0:
            for mo_re in except_list:
                module_dict = {"module": mo_re.module, "pod": mo_re.pod, "path": modules_name + "/" + mo_re.module}
                local_dependenceList.append(module_dict)

        local_module_data = {"version": "1.0.0", "branch": str(n_branch), "dependencies": local_dependenceList}
        update_yaml(local_yaml_path, local_module_data)


# 更新podfileModule文件
def merge_for_module_files(yaml_path, branch_result, n_branch):
    """
    更新ymal文件，修改本地依赖和分支依赖
    :param yaml_path: PodfileModule路径
    :param branch_result: 操作成功的模块列表
    :param n_branch: 新分支名
    :return:
    """
    # 获取ymal 数据
    podfile_module_data = yaml_data(yaml_path)
    dependenceList = podfile_module_data["dependencies"]
    # 转换成模型数组
    conver_deplist = load_yaml(dependenceList)

    index = 0
    for a in conver_deplist:
        for mo_re in branch_result:
            if a.module and mo_re.module and a.module == mo_re.module and mo_re.result == 1:
                module_dict = {"module": a.module, "pod": a.pod, "git": a.git, "tag": mo_re.tag,
                               "configurations": a.configurations,
                               "inhibit_warnings": a.inhibit_warnings}
                dependenceList[index] = module_dict
        index += 1
    podfile_data = {"version": "1.0.0", "branch": n_branch, "dependencies": dependenceList}
    update_yaml(yaml_path, podfile_data)


# 自动打tag 自动合并失败时返回空字符串
# 1. 清空当前工作目录
# 2. 拉取代码
# 3. 修改s.version
# 4. 提交代码
# 5. 拉取工作分支
# 5. 推送代码
def auto_release_path(filepath, git, pod, branch, new_tag):
    """
    自动合并branch到master中，并提交tag
    :param filepath: 文件路径
    :param git: git地址
    :param pod: pod模块
    :param branch: 分支
    :param new_tag: 新tag
    :return:
    """
    create_file(filepath)

    # return
    # 进入模块
    # clone 代码
    git_clone_command = "git clone -b master" + " " + git + " " + filepath
    # git add 代码
    git_add_command = "git add -A"
    # git pull branch 代码
    git_pull_command = "git pull origin " + branch

    # git push
    git_push_command = "git push origin master"
    # 用newTag来修改podspec中version
    os.system(git_clone_command)
    # print("执行 " + git_clone_command)
    # master分支下的版本号

    # 获取开发分支最后一次提交的信息
    repogit = RepoGit(proj_path=filepath)
    commit_message, commit = repogit.most_recent_commit_message(branch)
    repogit.switch_branch('master')
    git_commit_command = "git commit -m \'自动提交，修改tag\'"
    os.chdir(filepath)
    cur_tag = get_version_for(pod + ".podspec")
    os.system("pwd")
    os.system("ls")
    os.system(git_add_command)
    # print("执行 " + git_add_command)
    os.system(git_commit_command)
    # print("执行 " + git_commit_command)
    pul_status = os.system(git_pull_command)
    # print("执行 " + git_pull_command)
    if not pul_status == 0:
        debugInfo("代码冲突了")
        return ""
    dev_branch_tag = get_version_for(pod + ".podspec")
    new_tag_p = dev_branch_tag
    if dev_branch_tag == cur_tag:
        # 版本号一样就最后一位自增
        new_tag_p = incre_tag(cur_tag)
    else:
        # 版本号不一样，就比较如果开发分支比较大就用开发分支，否则还是自增
        res = compare_version(dev_branch_tag, cur_tag)
        if res == -1:
            new_tag_p = incre_tag(cur_tag)

    update_versionfor_podspec(pod + ".podspec", new_tag_p)
    os.system(git_add_command)
    # print("执行 " + git_add_command)
    os.system(git_commit_command)
    # print("执行 " + git_commit_command)
    # print("代码已经提交到master")
    # git pull branch 代码

    full_tag_message = '自动Tag 分支: {0} '.format(branch)
    if commit_message and len(commit_message) > 0:
        full_tag_message = full_tag_message + "最后提交信息： \"{0}\"   提交号：{1}".format(commit_message, commit.hexsha)
    git_tag_command = "git tag -a {0} -m \'{1}\'".format(new_tag_p, full_tag_message)
    # os.system(git_tag_command)
    # git_push_tag_command = "git push origin {0} ".format(new_tag_p)
    os.system(git_push_command)
    # print("执行 " + git_push_command)
    return new_tag_p


# 基于podfileModule来给每个组件创建一个分支
def create_branch(module_list, module_f_path, n_branch, modules, c_path):
    """
    基于列表，拉取对应代码，并创建一个开发分支
    :param module_list: 模块列表
    :param module_f_path: 路径
    :param n_branch: 新分支
    :param modules: 这些模块新建n_branch分支
    :param c_path: 当前的工作目录
    :return:
    """
    create_branch_result = []
    bar = Bar('install...', fill="*", max=len(modules))
    for a in module_list:
        if a.module in modules:
            bar.next()
            if (a.branch and len(str(a.branch)) > 0) or (a.tag and len(str(a.tag)) > 0):
                filename = a.module
                module_path = module_f_path + filename + "/"
                error_info = ''
                if not os.path.exists(module_path):
                    git_url = a.git
                    if not (a.git and len(a.git) > 0):
                        git_url = "http://gitlab.yonghui.cn/operation-xm-qdjg/{0}-snapshot.git".format(a.module.lower)
                    branch_name = auto_create_branch(module_path, git_url, a.branch, a.tag, n_branch)
                else:
                    local_branch = RepoGit(proj_path=module_path).getCurrentBranch()
                    error_info = "本地有工作目录: {0}，当前分支是：{1}".format(a.pod, local_branch)
                    branch_name = ''
                res = 1
                if not (branch_name and len(branch_name) > 0):
                    res = 0
                new_branch_model = ModuleStatusModel(a.module, a.pod, res, n_branch, error_info, inhibit_warnings=a.inhibit_warnings, configurations=a.configurations, source=a.source)
                create_branch_result.append(new_branch_model)
            else:
                new_branch_model = ModuleStatusModel(a.module, a.pod, 0, n_branch,
                                                     "podfileModule.yaml 中组件: " + a.pod + " 的branch或者tag为空, 不能确定要拉取的代码的位置",inhibit_warnings=a.inhibit_warnings, configurations=a.configurations, source=a.source)
                create_branch_result.append(new_branch_model)
        os.chdir(c_path)
    bar.finish()
    return create_branch_result


# 基于master 和 f_tag，创建一个新的分支new_branch，如果存在仓库则先清空仓库，再拉取分支
# 1. 清空当前工作目录
# 2. 拉取代码
# 3. 新建分支
# 4. 推送分支
def auto_create_branch(filepath, git, f_branch, f_tag, n_branch):
    """
    :param filepath: 文件路径
    :param git: git地址
    :param f_branch: 基于哪个分支切一个新的开发分支
    :param f_tag: 基于哪个tag切开发分支
    :param n_branch: 新分支名
    :return: 成功返回新分支名，失败返回空字符串
    """
    # 创建分支
    create_file(filepath)
    return new_branch(filepath, git, f_branch, f_tag, n_branch)


# 新建分支
def new_branch(filepath, git, f_branch, f_tag, n_branch):
    """
    f_branch 和 f_tag，创建一个新的分支n_branch
    2. 拉取代码
    3. 判断是否存在新分支，有新分支直接切到新分支
    3. 新建分支
    4. 切换到新分支
    4. 推送分支
    :param filepath: 路径
    :param git: git地址
    :param f_branch: 基于哪个分支切一个新的开发分支
    :param f_tag:  基于哪个tag切开发分支
    :param n_branch: 新分支名
    :return: 成功返回新分支名，失败返回空字符串
    """
    origin_branch = f_branch
    if not (f_branch and len(f_branch) > 0):
        origin_branch = "master"
    if f_branch and len(f_branch) > 0 and f_branch == n_branch:
        origin_branch = "master"
    # clone 代码
    git_clone_command = "git clone -b " + origin_branch + " " + git + " " + filepath
    # 创建一个新分支
    git_create_branch = "git branch " + n_branch
    if f_tag and len(f_tag) > 0:
        git_create_branch += " " + f_tag
    create_status = 0
    create_status += os.system(git_clone_command)
    # master分支下的版本号
    repoGit = RepoGit(proj_path=filepath)
    branchs = repoGit.get_branches()
    # debugInfo(str(branchs))
    os.chdir(filepath)
    if n_branch in branchs:
        debugInfo(n_branch + "分支已存在")
        repoGit.repo.git.execute(['git', 'checkout', n_branch])
        return n_branch
    try:
        # 创建并切换到新分支
        new_b = repoGit.create_branch(n_branch)
        new_b.checkout()
        # 推送新分支到远程仓库
        repoGit.push_branch(new_b)
    except Exception as e:
        print(str(e))
        debugInfo("新分支创建失败")
        return ""
    debugInfo("新分支创建成功")
    return n_branch


# 基于PodfileLocal，提交所有模块开发分支代码
def commit_branch(module_list, include_list, module_f_path, msg):
    """
    基于列表，提交对应开发分支代码
    :param module_list: 模块列表
    :param module_f_path: 路径
    :param msg: 提交信息
    :return: 返回操作的分支
    """
    commit_result = []
    invert_list = module_list
    if len(include_list) > 0:
        invert_list = [i for i in module_list if i.module in include_list]
    for i, module in enumerate(invert_list):
        path = module.path
        if not (path is not None and os.path.exists(path)):
            path = module_f_path + module.module + "/"
        module.path = path
    bar = Bar('commit...', fill="*", max=len(invert_list))
    for module in invert_list:
        bar.next()
        module_path = module.path
        result = 1
        branch = ''
        error_msg = ''
        if not os.path.exists(module_path):
            result = 0
            error_msg = "本地开发路径为空"
        else:
            git = None
            try:
                git = RepoGit(module_path)
            except Exception as e:
                result = 0
                error_msg = str(e)
            finally:
                if result != 0:
                    branch = git.getCurrentBranch()
                    error_msg = ''
                    result = 0
                    if not git.is_dirty():
                        error_msg = "很干净，没有可提交的"
                    else:
                        # 判断是否有没有追踪的文件
                        untracks = git.untracked()
                        git.add(untracks)
                        git.commit(msg)
                        result = not git.is_dirty()
                        if result == 0:
                            error_msg = "提交失败"
        modul_branch_model = ModuleStatusModel(module.module, module.pod, result, branch, error_msg)
        commit_result.append(modul_branch_model)
    bar.finish()
    return commit_result


# 基于podfileModule，提交模块开发分支代码
def pull_branch(module_list, include_list, module_f_path):
    """
    基于列表，提交对应开发分支代码
    :param module_list: 模块列表
    :param module_f_path: 路径
    :return: 返回操作的分支
    """
    invert_list = module_list;
    if len(include_list) > 0:
        invert_list = [i for i in module_list if i.module in include_list]

    for i, module in enumerate(invert_list):
        path = module.path
        if not (path is not None and os.path.exists(path)):
            path = module_f_path + module.module + "/"
        module.path = path

    pull_result = []
    bar = Bar('pull...', fill="*", max=len(invert_list))
    for module in invert_list:
        bar.next()
        msg = ''
        result = 1
        module_path = module.path
        branch = ''
        if not os.path.exists(module_path):
            result = 0
            msg = "本地开发路径为空"
        else:
            git = RepoGit(module_path)
            branch = git.getCurrentBranch()
            if git.is_dirty():
                result = -1
                msg = "本地有变动未提交，请确认"
            else:
                # ori = git.repo.remotes.origin
                try:
                    git.repo.git.pull('--progress', '--no-rebase', 'origin', branch)
                except Exception as e:
                    result = 0
                    msg = str(e)

        modul_branch_model = ModuleStatusModel(module.module, module.pod, result, branch, msg)
        pull_result.append(modul_branch_model)
    bar.finish()
    return pull_result


# 基于podfileModule，提交模块开发分支代码
def push_branch(module_list, include_list, module_f_path):
    """
    基于列表，提交对应开发分支代码
    :param module_list: 模块列表
    :param module_f_path: 路径
    :return: 返回操作的分支
    """

    index = 0
    pull_result = []
    invert_list = module_list;
    if len(include_list) > 0:
        invert_list = [i for i in module_list if i.module in include_list]

    for i, module in enumerate(invert_list):
        path = module.path
        if not (path is not None and os.path.exists(path)):
            path = module_f_path + module.module + "/"
        module.path = path

    bar = Bar('push...', fill="*", max=len(invert_list))
    for module in invert_list:
        bar.next()
        module_path = module.path
        msg = ''
        result = 1
        branch = ''
        if not os.path.exists(module_path):
            result = 0
            msg = "本地开发路径为空"
        else:
            git = RepoGit(module_path)
            branch = git.getCurrentBranch()

            if git.is_dirty():
                result = -1
                msg = "本地有变动未提交，请确认"
            else:
                try:
                    git.repo.git.pull('--progress', '--no-rebase', 'origin', branch)
                    git.repo.git.push('--progress', 'origin', branch)
                except Exception as e:
                    result = 0
                    msg = str(e)

        modul_branch_model = ModuleStatusModel(module.module, module.pod, result, branch, msg)
        pull_result.append(modul_branch_model)
    bar.finish()
    return pull_result


# 合并from_branch中代码到当前的开发分支
def merge_branch(module_list, convert_list, module_f_path, from_branch):
    """
    基于列表，提交对应开发分支代码
    :param module_list: 模块列表
    :param convert_list: 模块列表
    :param module_f_path: 路径
    :param from_branch: 要合并的分支
    :return: 返回操作的分支
    """
    index = 0
    pull_result = []
    invert_list = convert_list
    if len(module_list) > 0:
        invert_list = [i for i in convert_list if i.module in module_list]

    for i, module in enumerate(invert_list):
        path = module.path
        if not (path is not None and os.path.exists(path)):
            path = module_f_path + module.module + "/"
        module.path = path

    bar = Bar('merge...', fill="*", max=len(invert_list))
    for module in invert_list:
        if module.module in module_list:
            bar.next()
            module_path = module.path
            msg = ''
            result = 1
            branch = ''
            if not os.path.exists(module_path):
                result = 0
                msg = "本地开发路径为空"
            else:
                git = RepoGit(module_path)
                branch = git.getCurrentBranch()
                if git.is_dirty():
                    result = -1
                    msg = "本地有变动未提交，请确认"
                else:
                    branchs = git.get_branches()
                    if from_branch not in branchs:
                        result = -1
                        msg = "分支： {0} 不存在".format(from_branch)
                    else:
                        try:
                            if 'origin/' not in from_branch:
                                from_branch = "origin/" + from_branch
                            git.repo.git.pull('--progress', '--no-rebase', 'origin', branch)
                            git.repo.git.merge(from_branch)
                            git.repo.git.push('--progress', 'origin', branch)
                        except Exception as e:
                            result = 0
                            msg = str(e)
            modul_branch_model = ModuleStatusModel(module.module, module.pod, result, branch, msg)
            pull_result.append(modul_branch_model)
        index += 1
    bar.finish()
    return pull_result


# 合并from_branch中代码到当前的开发分支
def rebase_branch(module_list, convert_list, module_f_path, from_branch):
    """
    基于列表，提交对应开发分支代码
    :param module_list: 模块列表
    :param convert_list: 模块列表
    :param module_f_path: 路径
    :param from_branch: 要合并的分支
    :return: 返回操作的分支
    """
    index = 0
    pull_result = []
    if len(module_list) > 0:
        invert_list = [i for i in convert_list if i.module in module_list]

    for i, module in enumerate(invert_list):
        path = module.path
        if not (path is not None and os.path.exists(path)):
            path = module_f_path + module.module + "/"
        module.path = path

    bar = Bar('rebase...', fill="*", max=len(invert_list))
    for module in invert_list:
        if module.module in module_list:
            bar.next()
            module_path = module.path
            msg = ''
            result = 1
            if not os.path.exists(module_path):
                result = 0
                msg = "本地开发路径为空"
            else:
                git = RepoGit(module_path)
                branch = git.getCurrentBranch()
                msg = ''
                result = 1
                if git.is_dirty():
                    result = -1
                    msg = "本地有变动未提交，请确认"
                else:
                    branchs = git.get_branches()
                    if from_branch not in branchs:
                        result = -1
                        msg = "分支： {0} 不存在".format(from_branch)
                    else:
                        try:
                            git.repo.git.merge(from_branch)
                            git.repo.git.push('--progress', 'origin', branch)
                        except Exception as e:
                            result = 0
                            msg = str(e)
            modul_branch_model = ModuleStatusModel(module.module, module.pod, result, branch, msg)
            pull_result.append(modul_branch_model)
        index += 1
    bar.finish()
    return pull_result


# 基于podfileModule，提交模块开发分支代码
def release_branch(module_list, include_list, tag_path, c_path, f_branch):
    """
    基于模块列表，合并对应开发分支代码到master并打新的tag
    :param module_list: 所有模块列表
    :param include_list: release的模块列表
    :param tag_path:  这些模块排除在外，不提交n_branch代码
    :param c_path: 当前运行分支
    :param f_branch: 配置的全局统一分支，每个模块可以单独配置分支
    :return: 返回操作成功的分支
    """

    index = 0
    merge_result = []
    invert_list = module_list
    if len(include_list) > 0:
        invert_list = [i for i in invert_list if (i.module in include_list) and (i.branch and len(i.branch) > 0)]

    bar = Bar('release...', fill="*", max=len(invert_list))
    for a in invert_list:
        bar.next()
        if not (a.branch and len(a.branch) > 0) and not (a.tag and len(a.tag) > 0):
            a.branch = f_branch
        if a.branch and len(a.branch) > 0:
            filename = get_filename(a.git)
            module_path = tag_path + filename + "/"
            create_tag = auto_release_path(module_path, a.git, a.pod, a.branch, a.new_tag)
            result = 0
            if create_tag and len(create_tag) > 0:
                result = 1
                a.new_tag = create_tag
            merge_model = ModuleStatusModel(a.module, a.pod, result, a.branch, tag=create_tag)
            merge_result.append(merge_model)

        index += 1
        os.chdir(c_path)
    bar.finish()
    return merge_result


def fetch_dependency(module_list, include_list, c_path, modules_path, f_branch):
    def checkout_code(git_url, tag, path):
        # 使用 git 命令拉取代码到本地
        command = f'git clone -b master {git_url} {path}'
        print("执行git指令\n" + command)
        os.system(command)

    def get_direct_dependencies(podspec_file):
        dependencies = []
        with open(podspec_file) as file:
            for line in file:
                if '.dependency' in line:
                    dependencylist = line.split("'")
                    if len(dependencylist) >= 2:
                        dependency = dependencylist[1]
                        dependencies.append(dependency)

        return dependencies

    def get_all_dependencies(component, all_dependencies, cupath, modules_path, level=0):

        if component.third or not (component.git is not None and len(component.git) > 0):
            all_dependencies.append((component.pod + "_", level))
            return
        git_url = component.git
        tag = component.branch
        module_path = modules_path + component.pod + "/"
        if not os.path.exists(module_path):
            create_file(module_path)
            checkout_code(git_url, tag, module_path)
        # 拉取代码到本地
        # os.chdir(module_path)

        # 获取 .podspec 文件路径
        podspec_file = f'{module_path}{component.pod}.podspec'
        if os.path.exists(podspec_file):
            # 获取直接依赖
            direct_dependencies = get_direct_dependencies(podspec_file)
            all_dependencies.append((component.pod, level))
            results = [string.split("/", 1)[0] for string in direct_dependencies]
            for dependency in results:
                # 如果依赖不在已获取的依赖列表中，则递归获取依赖的依赖
                if dependency not in [dep[0] for dep in all_dependencies]:
                    find_module = getmodule_with_name(dependency, module_list)
                    if find_module is not None:
                        get_all_dependencies(find_module, all_dependencies, cupath, modules_path, level + 1)

    def getmodule_with_name(name, list):
        result_list = [module for module in list if module.module == name]
        if len(result_list) > 0:
            return result_list[0]
        return None

    index = 0
    new_list = module_list
    if len(include_list) > 0:
        new_list = [obj for obj in module_list if any(obj.module == other for other in include_list)]

    bar = Bar('release...', fill="*", max=len(new_list))
    all_dependencies = []
    for a in new_list:
        bar.next()
        get_all_dependencies(a, all_dependencies, curPath, modules_path, level=0)
        index += 1
        bar.finish()
    return all_dependencies


# 打印表格
def printTable(list, info):
    table = PrettyTable(["编号", "组件名", "分支", "异常信息"])
    # debugInfo(len(list))
    if len(list) > 0:
        for index in range(len(list)):
            model = list[index]
            table.add_row([index, model.module, model.branch, model.msg])
        table.align[1] = '1'
        table.border = True
        table.junction_char = '+'
        table.horizontal_char = '-'
        table.vertical_char = '|'
        table.sortby = '分支'
        table.hrules = ALL
        debugInfo("\n[!] 以下是 \"{0}\"\n".format(info))
        debugInfo(table)
        debugInfo("\n")
    else:
        debugInfo("\n[!] 暂无 \"{0}\"\n".format(info))


def save_dict_to_yaml(dict_value: dict, save_path: str):
    """dict保存为yaml"""
    with open(save_path, 'w') as file:
        file.write(yaml.dump(dict_value, sort_keys=False))


# 创建分支的对象
# branch 组件新分支名字
class yhgit:

    # 拉取壳工程代码
    def clone(self, git, o_branch, n_branch):
        f_path = os.getcwd()
        os.chdir(f_path)
        result = new_branch(f_path, git, o_branch, '', n_branch)
        res = 0
        if result and len(result):
            res = 1
        error = '分支创建失败'
        if result and len(result):
            error = ''
        resultModule = [ModuleStatusModel("壳工程拉取成功", "壳工程拉取成功", res, n_branch, error, git=git)]
        succ_list = []
        fail_list = []
        for merg_Model in resultModule:
            if merg_Model.result == 1:
                succ_list.append(merg_Model)
            else:
                fail_list.append(merg_Model)
        printTable(succ_list, "分支创建成功的模块")
        printTable(fail_list, "分支创建失败的模块")

    def init(self, n_branch, git):
        """
        如果本地没有PodfileModule，该命令会自动生成PodfileModule文件，然后可以使用后续指令进行状态检测，推拉代码，提交及打tag的操作，如果有就会只执行后续的新增分支及拉取代码的操作
        :return:
        """
        c_path = ""
        f_path = os.getcwd()
        file_name = os.path.basename(git)
        file_name, file_ext = os.path.splitext(file_name)
        modules_name = "modules"
        modules_path = c_path + "modules/"
        # 子目录，用来存放子模块仓库, 如果没有需要创建一个
        if not os.path.exists(modules_path):
            create_file(modules_path)

        module_path = modules_path + file_name
        result = auto_create_branch(module_path, git, n_branch, '', n_branch)
        os.chdir(f_path)

        error = ""
        res = 1
        newfile_name = ""
        # debugInfo("执行结果" + result)
        if result and len(result) > 0:
            # 新分支创建成功
            # 更新模块的名字{file_name}为{podspec}名字
            debugInfo(module_path)
            files = [filename for filename in os.listdir(f_path + "/" + module_path) if filename.endswith(".podspec")]
            # debugInfo(files)
            if len(files) > 0:
                newfile_name = files[0]
                newfile_name, file_ext = os.path.splitext(newfile_name)

            isSame = newfile_name == file_name

            # debugInfo("执行结果" + newfile_name)
            newfile_path = modules_path + newfile_name
            # 判断是否有newfile_name对应的文件夹
            find = False
            for name in os.listdir(f_path + "/" + modules_path):
                # 检查文件夹名称是否以指定字符串开头
                if name.startswith(newfile_name) and os.path.isdir(os.path.join(f_path + "/" + modules_path, name)):
                    find = True
            if not find and newfile_name and len(newfile_name) > 0:
                os.rename(f_path + "/" + module_path, f_path + "/" + newfile_path)
            else:
                # 删除旧的文件夹
                if os.path.exists(f_path + "/" + module_path):
                    if not isSame:
                        del_dir(f_path + "/" + module_path)
                        res = 1
                        error = "存在同名文件夹，新建分支失败，请手动切换"
                    else:
                        res = 1
                        error = "新建分支成功，请手动切换"

        # 判断是否有PodfileModule文件夹
        pre_path = f_path + "/"
        # debugInfo(pre_path)
        localyamlPath_ = pre_path + 'PodfileLocal.yaml'
        yamlPath_ = pre_path + 'PodfileModule.yaml'
        localyamlPath = c_path + 'PodfileLocal.yaml'
        yamlPath = c_path + 'PodfileModule.yaml'
        if os.path.exists(localyamlPath_) and os.path.getsize(localyamlPath) == 0:
            del_path(localyamlPath_)

        if os.path.exists(yamlPath_) and os.path.getsize(yamlPath) == 0:
            del_path(yamlPath_)

        if not os.path.exists(yamlPath_):
            open(yamlPath, 'w').close()
            after_convert = []
            module_dict = {"module": newfile_name, "pod": newfile_name, "git": git, "branch": n_branch}
            after_convert.append(module_dict)
            podmodule_data = {"version": "1.0.0", "branch": str(n_branch), "dependencies": after_convert}
            save_dict_to_yaml(podmodule_data, yamlPath)

        branch_res = [ModuleStatusModel(newfile_name, newfile_name, res, n_branch, error, git=git)]
        update_module_files(yamlPath, localyamlPath, branch_res, n_branch, modules_name)
        succ_list = []
        fail_list = []
        for merg_Model in branch_res:
            if merg_Model.result == 1:
                succ_list.append(merg_Model)
            else:
                fail_list.append(merg_Model)
        printTable(succ_list, "分支创建成功的模块")
        printTable(fail_list, "分支创建失败的模块")

    # 初始化项目仓库，自动拉取组件仓库，并创建新分支
    def install(self, n_branch, modules=[]):
        """
        基于初始化的配置信息，初始化开发分支； 创建工程目录，创建每个模块的工作目录，创建开发分支，创建工作目录
        1. 如果本地有该组件的目录，就跳过，不会切换到新分支（避免造成，手动切换分之后，又自定切换到新分支）
        2. 如果本地没有改组件目录，就新建目录，拉取master下tag的代码，然后创建新分支
        :param n_branch: 新分支的名字
        :param modules: 拉取这些模块，并创建新分支。
        :return:
        """
        c_path = os.getcwd()
        fa_path = ""
        modules_file_name = "modules"
        new_branch = n_branch

        yamlPath = fa_path + 'PodfileModule.yaml'
        modules_path = fa_path + modules_file_name + "/"
        yamlPath = fa_path + 'PodfileModule.yaml'
        localyamlPath = fa_path + 'PodfileLocal.yaml'

        # 子目录，用来存放子模块仓库, 如果没有需要创建一个
        if not os.path.exists(modules_path):
            create_file(modules_path)
        # 获取ymal 数据
        podfile_module_data = yaml_data(yamlPath)
        # 获取依赖数据
        dependenceList = podfile_module_data["dependencies"]
        # 转换成模型数组
        conver_deplist = load_yaml(dependenceList)
        branch_res = create_branch(conver_deplist, modules_path, new_branch, modules, c_path)
        if len(branch_res) > 0:
            update_module_files(yamlPath, localyamlPath, branch_res, new_branch, modules_file_name)
        if len(branch_res) == 0:
            debugInfo("没有要执行yhgit install的模块")
        else:
            succ_list = []
            fail_list = []
            for merg_Model in branch_res:
                if merg_Model.result == 1:
                    succ_list.append(merg_Model)
                else:
                    fail_list.append(merg_Model)
            printTable(succ_list, "分支创建成功的模块")
            printTable(fail_list, "分支创建失败的模块")

    # 获取podfileLocal.yaml中各模块状态, 提示： 1. 很干净没有未提交的代码 2. 有改动未提交 3. 没有相关文件报错误
    def status(self, include_modules):
        """
        获取podfileLocal.yaml中各模块状态, 提示： 1. 很干净没有未提交的代码 2. 有改动未提交
        1. 如果podfileLocal.yaml是空则终止
        2. 如果moduls为空则终止
        :return:
        """
        modules_file_name = "modules"
        modules_path = modules_file_name + "/"
        local_yaml_path = 'PodfileLocal.yaml'

        # 子目录，用来存放子模块仓库, 如果没有需要创建一个
        if not os.path.exists(modules_path):
            debugInfo("本地modules为空，无法查看组件的状态")
            return
        if not os.path.exists(local_yaml_path):
            debugInfo("本地local_yaml_path为空，无法查看组件的状态")
            return
        podfile_module_data = yaml_data(local_yaml_path)
        local_dependenceList = podfile_module_data["dependencies"]
        if local_dependenceList is None:
            local_dependenceList = []
        # 转换成模型数组
        module_list = load_yaml(local_dependenceList)
        status_result = []
        invert_list = module_list
        if len(include_modules) > 0:
            invert_list = [i for i in module_list if i.module in include_modules]

        bar = Bar('status...', fill="*", max=len(invert_list))
        for module in invert_list:
            bar.next()
            result = 0
            branchname = ''
            msg = ''
            if not (module.path and len(module.path) > 0):
                result = -1
                msg = "请检查PodfileLocal.yaml中模块：" + module.module + " 的path"
            else:
                if os.path.exists(module.path):
                    repogit = RepoGit(module.path)
                    result = not repogit.is_dirty()
                    branchname = repogit.getCurrentBranch()
                    # 如果是有改动，列出文件的改动状态
                    if result == 0:
                        msg = repogit.getStatusFormatStr
                else:
                    result = -1
                    msg = "请检查模块：" + module.module + " 的路径 " + module.path + " 是否为空"
            new_branch_model = ModuleStatusModel(module.module, module.pod, result, branchname, msg)
            status_result.append(new_branch_model)
        bar.finish()
        if len(status_result) == 0:
            debugInfo("没有要执行git status的模块")
        else:
            error_list = []
            fail_list = []
            success_list = []
            for merg_Model in status_result:
                if merg_Model.result == 1:
                    success_list.append(merg_Model)
                elif merg_Model.result == 0:
                    fail_list.append(merg_Model)
                elif merg_Model.result == -1:
                    error_list.append(merg_Model)
            printTable(success_list, "没有代码要提交的模块")
            printTable(fail_list, "有代码要提交的模块")
            printTable(error_list, "检查失败的模块")

    # 自动提交本地修改的内容
    def commit(self, include_list, msg):
        """
        基于podfileModules的配置信息，提交本地开发分支代码
        :param msg: 这些模块不需要修改，不能提交代码
        :return:
        """
        fa_path = ""
        modules_file_name = "modules"
        modules_path = fa_path + modules_file_name + "/"
        # 子目录，用来存放子模块仓库
        if not os.path.exists(modules_path):
            debugInfo("没有modules目录，不能提交")
            return

        local_yaml_path = fa_path + 'PodfileLocal.yaml'

        # 子目录，用来存放子模块仓库, 如果没有需要创建一个
        if not os.path.exists(local_yaml_path):
            debugInfo("本地无PodfileLocal.yaml，无法继续提交")
            return
        if not (msg and len(msg) > 0):
            debugInfo("提交信息为空，无法继续提交")
            return
        podfile_module_data = yaml_data(local_yaml_path)
        local_dependenceList = podfile_module_data["dependencies"]
        # 转换成模型数组
        module_list = load_yaml(local_dependenceList)
        branch_res = commit_branch(module_list, include_list, modules_path, msg)
        if len(branch_res) == 0:
            debugInfo("没有要提交代码的模块")
        else:
            succ_list = []
            fail_list = []
            for merg_Model in branch_res:
                if merg_Model.result == 1:
                    succ_list.append(merg_Model)
                else:
                    fail_list.append(merg_Model)
            printTable(succ_list, "代码提交成功的模块")
            printTable(fail_list, "代码提交失败的模块")

    # 自动拉取远端代码
    def pull(self, include_list):
        """
        基于PodfileLocal的配置信息，提交本地开发分支代码
        :return:
        """
        fa_path = ""
        modules_file_name = "modules"
        modules_path = fa_path + modules_file_name + "/"
        # 子目录，用来存放子模块仓库
        if not os.path.exists(modules_path):
            logging.info("没有modules目录，不能提交")
            print("没有modules目录，不能提交")
            return

        local_yaml_path = fa_path + 'PodfileLocal.yaml'

        # 子目录，用来存放子模块仓库, 如果没有需要创建一个
        if not os.path.exists(local_yaml_path):
            debugInfo("本地无PodfileLocal.yaml，无法继续提交")
            return
        podfile_module_data = yaml_data(local_yaml_path)
        local_dependenceList = podfile_module_data["dependencies"]
        # 转换成模型数组
        module_list = load_yaml(local_dependenceList)
        branch_res = pull_branch(module_list, include_list, modules_path)
        if len(branch_res) == 0:
            logging.info("没有要拉取远端代码的模块")
        else:
            succ_list = []
            fail_list = []
            for merg_Model in branch_res:
                if merg_Model.result == 1:
                    succ_list.append(merg_Model)
                else:
                    fail_list.append(merg_Model)
            printTable(succ_list, "代码拉取成功的模块")
            printTable(fail_list, "代码拉取失败的模块")

    # 自动推送本地修改到远端
    def push(self, include_list=[]):
        """
        基于PodfileLocal的配置信息，拉取本地开发分支代码
        :return:
        """
        fa_path = ""
        modules_file_name = "modules"
        modules_path = fa_path + modules_file_name + "/"
        # 子目录，用来存放子模块仓库
        if not os.path.exists(modules_path):
            logging.info("没有modules目录，不能提交")
            print("没有modules目录，不能提交")
            return

        local_yaml_path = fa_path + 'PodfileLocal.yaml'

        # 子目录，用来存放子模块仓库, 如果没有需要创建一个
        if not os.path.exists(local_yaml_path):
            debugInfo("本地无PodfileLocal.yaml，无法继续提交")
            return
        podfile_module_data = yaml_data(local_yaml_path)
        local_dependenceList = podfile_module_data["dependencies"]
        # 转换成模型数组
        module_list = load_yaml(local_dependenceList)
        branch_res = push_branch(module_list, include_list, modules_path)
        if len(branch_res) == 0:
            logging.info("没有要推送代码的模块")
        else:
            succ_list = []
            fail_list = []
            for merg_Model in branch_res:
                if merg_Model.result == 1:
                    succ_list.append(merg_Model)
                else:
                    fail_list.append(merg_Model)
            printTable(succ_list, "代码推送成功的模块")
            printTable(fail_list, "代码推送失败的模块")

    # 将from_branch 中的代码合并到当前的开发分支
    def merge(self, from_branch, module_list):
        """
                基于PodfileLocal的配置信息，拉取本地开发分支代码
                :return:
                """
        fa_path = ""
        modules_file_name = "modules"
        modules_path = fa_path + modules_file_name + "/"
        # 子目录，用来存放子模块仓库
        if not os.path.exists(modules_path):
            logging.info("没有modules目录，不能提交")
            print("没有modules目录，不能提交")
            return

        yamlPath = fa_path + 'PodfileModule.yaml'
        # 获取ymal 数据
        podfile_module_data = yaml_data(yamlPath)
        # 获取依赖数据
        dependenceList = podfile_module_data["dependencies"]
        # 转换成模型数组
        conver_deplist = load_yaml(dependenceList)

        branch_res = merge_branch(module_list, conver_deplist, modules_path, from_branch)
        if len(branch_res) == 0:
            logging.info("没有要merge代码的模块")
        else:
            succ_list = []
            fail_list = []
            for merg_Model in branch_res:
                if merg_Model.result == 1:
                    succ_list.append(merg_Model)
                else:
                    fail_list.append(merg_Model)
            printTable(succ_list, "代码merge成功的模块")
            printTable(fail_list, "代码merge失败的模块")

    def read_all_yaml(self, filename):
        fa_path = ''
        yamlPath = fa_path + filename
        # 子目录，用来存放子模块仓库, 如果没有需要创建一个
        if not os.path.exists(yamlPath):
            debugInfo("本地无PodfileModule.yaml，无法继续提交")
            return []
        # 获取yaml 数据
        podfile_module_data = yaml_data(yamlPath)
        logging.info("读取yaml数据")
        # 获取依赖数据
        dependenceList = podfile_module_data["dependencies"]
        return dependenceList

    # 查找组件的依赖
    def dependency(self, include_list=[], detail=False):
        c_path = os.getcwd()
        fa_path = ''
        modules_file_name = "tagpath"
        modules_path = fa_path + modules_file_name + "/"
        # 子目录，用来存放子模块仓库
        if not os.path.exists(modules_path):
            create_file(modules_path)
        yamlPath = fa_path + 'PodfileModule.yaml'
        dependenceList = []
        dependenceList_yaml = self.read_all_yaml('PodfileModule.yaml')
        dependenceList_third = self.read_all_yaml('PodfileThirdParty.yaml')
        for moduel in dependenceList_third:
            moduel.third = True
        dependenceList += dependenceList_yaml
        dependenceList += dependenceList_third
        # 子目录，用来存放子模块仓库, 如果没有需要创建一个
        if not os.path.exists(yamlPath):
            debugInfo("本地无PodfileModule.yaml，无法继续提交")
            return
        # 获取yaml 数据
        logging.info("读取yaml数据")
        # 转换成模型数组
        conver_deplist = load_yaml(dependenceList)
        logging.info("转换成模型")
        new_inclue = include_list
        if len(include_list) == 0:
            new_inclue += [module.module for module in conver_deplist]
        branch_res = fetch_dependency(conver_deplist, new_inclue, c_path, modules_path, 'master')
        logging.info("dependency成功的模块\n")
        count = 1
        native = 1
        prde = ''
        dep_list = []
        c_module_list = []
        third_module_list = []
        for dependency, level in branch_res:
            if level == 0:
                if len(prde) > 0:
                    if count >= 1 and len(prde) > 0:
                        moduleDep = YHModuleDependency(prde, count - 1, native - 1, c_module_list, third_module_list)
                        dep_list.append(moduleDep)
                    count = 1
                    native = 1
                    c_module_list = []
                    third_module_list = []
                prde = dependency
            else:
                if dependency not in c_module_list:
                    count += 1
                    c_module_list.append(dependency)
                    if not dependency.endswith('_'):
                        native += 1
                        third_module_list.append(dependency)
                # print("插入后")
                # print(len(c_module_list))

        # resu = f"{prde} 共 {count - 1} 原生 {count - native - 1}"
        if count >= 1 and len(prde) > 0:
            moduleDep = YHModuleDependency(prde, count - 1, native - 1, c_module_list, third_module_list)
            dep_list.append(moduleDep)
        return dep_list
        # if os.path.exists(modules_path):
        #     del_dir(modules_path)

    # 自动提交子模块的代码
    def release(self, include_list=[]):
        """
        基于podfileModules的配置信息，merge开发分支到master，获取开发分支的版本号，如果版本号大于master分支，新的tag就为开发分支版本号，如果版本号相等，那那么就末尾自增1，自动打tag
        :return:
        """
        c_path = os.getcwd()
        fa_path = ''
        modules_file_name = "tagpath"
        modules_path = fa_path + modules_file_name + "/"
        # 子目录，用来存放子模块仓库
        if not os.path.exists(modules_path):
            create_file(modules_path)
        yamlPath = fa_path + 'PodfileModule.yaml'

        # 子目录，用来存放子模块仓库, 如果没有需要创建一个
        if not os.path.exists(yamlPath):
            debugInfo("本地无PodfileModule.yaml，无法继续提交")
            return
        # 获取yaml 数据
        podfile_module_data = yaml_data(yamlPath)
        logging.info("读取yaml数据")
        # 获取依赖数据
        dependenceList = podfile_module_data["dependencies"]
        branch = podfile_module_data["branch"]
        # 转换成模型数组
        conver_deplist = load_yaml(dependenceList)
        logging.info("转换成模型")
        branch_res = release_branch(conver_deplist, include_list, modules_path, c_path, branch)
        if len(branch_res) > 0:
            merge_for_module_files(yamlPath, branch_res, branch)
        if len(branch_res) == 0:
            logging.info("没有要realse的模块")
        else:
            succ_list = []
            fail_list = []
            for merg_Model in branch_res:
                if merg_Model.result == 1:
                    succ_list.append(merg_Model)
                else:
                    fail_list.append(merg_Model)
            printTable(succ_list, "release成功的模块")
            printTable(fail_list, "realse失败的模块")

        if os.path.exists(modules_path):
            del_dir(modules_path)

    # 自动提交子模块的代码
    def clean(self):
        """
        基于podfileModules的配置信息，merge开发分支到master，获取开发分支的版本号，如果版本号大于master分支，新的tag就为开发分支版本号，如果版本号相等，那那么就末尾自增1，自动打tag
        :return:
        """
        local_yaml_path = 'PodfileLocal.yaml'
        # 子目录，用来存放子模块仓库, 如果没有需要创建一个
        if os.path.exists(local_yaml_path):
            os.remove(local_yaml_path)
        modules_path = "modules/"
        if os.path.exists(modules_path):
            del_dir(modules_path)

        debugInfo("执行成功")

    def help(self):
        table = PrettyTable(["编号", "指令", "参数", "说明", "使用"])
        table.add_row(
            [0, "init", "-b 指定分支名; 组件git地址",
             "根据git地址，新建分支，然后自动更新PodfileModule.yaml及PodfileLocal.yaml文件",
             "yhgit init -b test git@gitlab.yonghui.cn:operation-xm-qdjg/yhfoundation-ios.git"])
        table.add_row(
            [0, "install", "-b 指定分支名; 组件 指定 新建分支的组件",
             "根据分支branch，然后基于组件或者PodfileLocal.yaml中的配置，新建分支branch",
             "yhgit install -b test abc \n yhgit install"])
        table.add_row(
            [1, "status", "", "根据本地PodfileLocal.yaml中配置的仓库，获取所有仓库的开发分支及仓库状态", "yhgit status"])
        table.add_row([2, "commit", "-m 指定提交的信息", "根据本地PodfileLocal.yaml中配置的仓库，提交本地仓库中的修改",
                       "yhgit commit -m \'提交信息\'"])
        table.add_row([3, "pull", "", "根据本地PodfileLocal.yaml中配置的仓库，拉取远端仓库中代码", "yhgit pull"])
        table.add_row([4, "push", "", "根据本地PodfileLocal.yaml中配置的仓库，推送本地代码到远端", "yhgit push"])
        table.add_row(
            [5, "merge", "-b 指定分支名; 组件 指定 merge的组件", "然后基于组件merge 分支到当前开发分支，并自动提交",
             "yhgit merge -b master abc"])
        table.add_row([6, "release", "组件： 指定组件",
                       "根据本地PodfileModule.yaml中配置的仓库或者手动指定仓库，合并开发分支到master，并自动打新的tag",
                       "yhgit release abc"])
        table.add_row([7, "clean", "", "清空本地PodfileLocal.yaml 及 modules文件夹", "yhgit clean"])
        table.add_row([8, "version", "", "查看版本号", "yhgit version \n yhgit -v"])
        table.add_row([8, "help", "", "查看帮助文档", "yhgit help \n yhgit -h"])

        table.align[1] = '1'
        table.border = True
        table.junction_char = '+'
        table.horizontal_char = '-'
        table.vertical_char = '|'
        table.hrules = ALL
        debugInfo(table)
        debugInfo("\n")


def debugInfo(msg):
    logging.info(msg)
    print(msg)


def main(argvs=None):
    """The main routine."""

    if argvs is None:
        argvs = sys.argv
    # 获取指令类型
    if len(argvs) <= 1:
        yhgit().help()
        return
    command = argvs[1]
    branchname = ''
    modules = []
    if command == "install":
        if len(argvs) > 2:
            subcommand = argvs[2]
            if subcommand and len(subcommand) > 0 and subcommand == "-b":
                # 需要获取具体的分支名
                branchname = argvs[3]
                if branchname and len(branchname) > 0:
                    # 获取需要创建分支的组件
                    modules = argvs[4:]
            else:
                modules = argvs[2:]

        if not (branchname and len(branchname) > 0):
            # 获取本地配置的分支名称
            # 获取ymal 数据
            cuPath = os.getcwd()
            local_yaml_path = cuPath + '/PodfileLocal.yaml'
            branchname = ""
            if os.path.exists(local_yaml_path):
                podfile_module_data = yaml_data(local_yaml_path)
                branchname = podfile_module_data.get("branch", None)
        if not (branchname and len(branchname) > 0):
            logging.error("请指定分支名字，\n 1. 指令后面指定分支 \n2. 在PodfileLoacal.yaml中指定branch")
        if not (modules and len(modules) > 0):
            logging.error("请指定具体的模块")
        else:
            yhgit().install(branchname, modules)
    elif command == "init":
        git = ""
        if len(argvs) > 2:
            subcommand = argvs[2]
            if subcommand and len(subcommand) > 0 and subcommand == "-b" and len(argvs) >= 4:
                # 需要获取具体的分支名
                branchname = argvs[3]
                if branchname and len(branchname) > 0 and len(argvs) >= 5:
                    # 获取需要创建分支的组件
                    git = argvs[4]

        if (not (git and len(git) > 0)) or (not (branchname and len(branchname) > 0)):
            logging.error("请指定分支或者git地址")
        else:
            yhgit().init(branchname, git)

    elif command == "merge":
        if len(argvs) > 2:
            subcommand = argvs[2]
            if subcommand and len(subcommand) > 0 and subcommand == "-b":
                # 需要获取具体的分支名
                branchname = argvs[3]
                if branchname and len(branchname) > 0:
                    # 获取需要创建分支的组件
                    modules = argvs[4:]
        if not (branchname and len(branchname) > 0):
            debugInfo("必须指定merge的分支: -b 分支")
            exit()
        if not (modules and len(modules) > 0):
            logging.error("请指定具体的模块")
        else:
            yhgit().merge(branchname, modules)

    elif command == "status":
        # 查看本地代码的状态
        modules = []
        if len(argvs) > 2:
            modules = argvs[2:]
        yhgit().status(modules)
    elif command == "commit":
        commit_msg = ''
        if len(argvs) > 2:
            subcommand = argvs[2]
            if subcommand and len(subcommand) > 0 and subcommand == "-m":
                # 需要获取具体的分支名
                commit_msg = argvs[3]
                if commit_msg and len(commit_msg) > 0 and len(argvs) > 3:
                    modules = argvs[4:]
        if not (commit_msg and len(commit_msg) > 0):
            debugInfo("必须添加-m 和 commit_msg")
        else:
            yhgit().commit(modules, commit_msg)
    elif command == "pull":
        modules = []
        if len(argvs) > 2:
            modules = argvs[2:]
        yhgit().pull(modules)

    elif command == "push":
        modules = []
        if len(argvs) > 2:
            modules = argvs[2:]
        yhgit().push(modules)

    elif command == "release":
        modules = []
        if len(argvs) > 2:
            modules = argvs[2:]
        yhgit().release(modules)
    elif command == "dependency":
        args = parser.parse_args()
        detail = False
        modules = []
        if args.detail is not None:
            detail = True if args.detail == 1 else False
        if args.modules is not None:
            modules = args.modules
        if len(modules).count == 0:
            dependenceList_yaml = yhgit().read_all_yaml('PodfileModule.yaml')
            conver_deplist = load_yaml(dependenceList_yaml)
            modules = [moduel.module for moduel in conver_deplist]
        if len(modules).count == 0:
            print("执行失败，没有指定模块")
        print("执行中")
        result = []
        for modu in modules:
            list = yhgit().dependency([modu], detail)
            result += list
        dep_list = sorted(result, key=lambda YHModuleDependency: YHModuleDependency.native, reverse=True)
        # dep_list = [dep for dep in dep_list if dep is not None]
        res_str = ''
        bar = Bar('dependency...', fill="*", max=len(dep_list))
        for module in dep_list:
            bar.next()
            module_info = '\n '.join(module.natvielist)
            # print(module.deplist)
            # print(module.natvielist)
            if detail:
                res_str += f"{module.name} 共 {module.count} 原生 {module.native} \n {module_info}\n"
            else:
                res_str += f"{module.name} 共 {module.count} 原生 {module.native} \n"
            print(res_str)
            res_str = ''
        bar.finish()
    elif command == "clean":
        yhgit().clean()
    elif command == "version" or command == "-v":
        debugInfo(pkg_resources.require("yhgit")[0].version)
    elif command == "help" or command == "-h":
        yhgit().help()


if __name__ == '__main__':
    # cuPath = os.getcwd()
    # main('yhgit dependency')
    # fa_path = "../../Desktop/operation-cp-hcwms/yhdos/yhdos/ios/"
    # project_git = "http://gitlab.yonghui.cn/operation-pc-mid-p/yh-rme-srm-purchase-ios.git"
    # # 分支的名字，如果没有指定将用年月日表示
    # n_branch = "221107"

    # main
    # cb.init_project(clean_proj=False)
    # cb.pull_modules()
    # cb.push_modules()
    # cb.merge_modules()
    # os.chdir(fa_path)
    # os.system("pod install")

    # yhgit().dependency(["SXMyCollectionModule"])

    mod_list = ['IntelligentReplenishModule',
                'YHNetExceptionDiaglog',
                'YHMarketingExecute',
                'YHMarketResearch',
                'SXShoppingCart',
                'SXFreshDetailModule',
                'SXApproachReportModule'
                'SXTransferInShopModule',
                'SXFreshFeedback',
                'SXOrderList',
                'SXFreight',
                'SXBatchOrderModule',
                'SXMyCollectionModule',
                'SXDailyOrderModule',
                'SXFreshOrderModule',
                'SXOutOfStock',
                'YHDOSClothesRefund',
                'YHDOSFreshRefund',
                'SXFoodEncyclopediaModule',
                'YHFreshDisplaySpace']
    mod_list = ['IntelligentReplenishModule']
    # dependenceList_yaml = yhgit().read_all_yaml('PodfileModule.yaml')
    # conver_deplist = load_yaml(dependenceList_yaml)
    # list = [moduel.module for moduel in conver_deplist]
    result = []
    detail = True
    for modu in mod_list:
        list = yhgit().dependency([modu])
        sleep(0.2)
        result += list
        # print(resu)
    dep_list = sorted(result, key=lambda YHModuleDependency: YHModuleDependency.native, reverse=True)
    # dep_list = [dep for dep in dep_list if dep is not None]
    res_str = ''
    bar = Bar('dependency...', fill="*", max=len(dep_list))
    for module in dep_list:
        bar.next()
        module_info = '\n '.join(module.natvielist)
        # print(module.deplist)
        # print(module.natvielist)
        if detail:
            res_str += f"{module.name} 共 {module.count} 原生 {module.native} \n {module_info}\n"
        else:
            res_str += f"{module.name} 共 {module.count} 原生 {module.native} \n"
        print(res_str)
        res_str = ''
    bar.finish()
    """
    argv[0]:  获取命令的类型 如下
    install

    argv[1]:  命令的


    """
