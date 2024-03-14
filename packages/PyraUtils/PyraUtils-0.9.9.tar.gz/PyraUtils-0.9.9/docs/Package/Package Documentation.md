# 封装Python

## 源码包与二进制包什么区别？

Python 包的分发可以分为两种：

- 以源码包的方式发布

    源码包安装的过程，是先解压，再编译，最后才安装，所以它是跨平台的，由于每次安装都要进行编译，相对二进包安装方式来说安装速度较慢。

    源码包的本质是一个压缩包，其常见的格式有：zip, gz, tar, bz2等

- 以二进制包形式发布

    二进制包的安装过程省去了编译的过程，直接进行解压安装，所以安装速度较源码包来说更快。

    由于不同平台的编译出来的包无法通用，所以在发布时，需事先编译好多个平台的包。

    二进制包的常见格式有：whl, egg

## eggs 与 wheels 有什么区别？

Egg 格式是由 setuptools 在 2004 年引入，而 Wheel 格式是由 PEP427 在 2012 年定义。Wheel 的出现是为了替代 Egg，它的本质是一个zip包，其现在被认为是 Python 的二进制包的标准格式。

以下是 Wheel 和 Egg 的主要区别：

- Wheel 有一个官方的 PEP427 来定义，而 Egg 没有 PEP 定义
- Wheel 是一种分发格式，即打包格式。而 Egg 既是一种分发格式，也是一种运行时安装的格式，并且是可以被直接 import
- Wheel 文件不会包含 .pyc 文件
- Wheel 使用和 PEP376 兼容的 .dist-info 目录，而 Egg 使用 .egg-info 目录
- Wheel 有着更丰富的命名规则。
- Wheel 是有版本的。每个 Wheel 文件都包含 wheel 规范的版本和打包的实现
- Wheel 在内部被 sysconfig path type 管理，因此转向其他格式也更容易
- wheel 包可以通过 pip 来安装，只不过需要先安装 wheel 模块，然后再使用 pip 的命令。

## 封装Python的方法

- 方法一(推荐):

    - 安装模块

            $ pip install twine
            $ pip install build
            $ pip install wheel
            $ pip install --upgrade setuptools

    - 执行当前程序包文件的构建操作命令(build默认会创建一个虚拟环境，并且默认会生成`tar.gz`和`.whl`格式的安装包)

            $ python -m build

    - 上传项目

            $ twine upload dist/*

- 方法二:

    如果不希望创建虚拟环境，或者本身开发项目已经在虚拟环境下运行，请看这里。

    - 安装模块

            $ pip install twine
            $ pip install wheel
            $ pip install --upgrade setuptools

    - 执行当前程序包文件的构建操作命令

            $ python setup.py sdist bdist_wheel

    - 上传项目

            $ twine upload dist/*

## [pypi免密上传](https://packaging.python.org/specifications/pypirc/)

pypi免密上传, 通过twine配置文件实现。

    $ vim HOME/.pypirc

        [distutils]
        index-servers =
            pypi
            pypitest
            private-repository
        
        [pypi]
        username: __token__
        password: <PyPI token>

        [pypitest]
        username: __token__
        password: <PyPI token>    

        [private-repository]
        repository = <private-repository URL>
        username = <private-repository username>
        password = <private-repository password>

    $ chmod 600 HOME/.pypirc

## 参考文件

<https://blog.konghy.cn/2018/04/29/setup-dot-py/>

<https://zhuanlan.zhihu.com/p/276461821>

<https://packaging.python.org/specifications/pypirc/>
