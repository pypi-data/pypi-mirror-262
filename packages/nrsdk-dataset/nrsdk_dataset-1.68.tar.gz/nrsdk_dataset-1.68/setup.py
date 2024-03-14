from setuptools import setup, find_packages

setup(
    name='nrsdk_dataset',  # 需要打包的名字,即本模块要发布的名字
    version='1.68',  # 版本
    description='A  module for query data collected by NeuroRecorder',  # 简要描述
    packages=find_packages(),  # 需要打包的模块
    author='Puzhe Li',  # 作者名
    author_email='li_puzhe@qq.com',  # 作者邮件
    url='http://gitlab.eegion.cn/lglab/nrsdk_dataset',  # 项目地址,一般是代码托管的网站
    requires=['mne'],  # 依赖包,如果没有,可以不要
    license='MIT'
)
