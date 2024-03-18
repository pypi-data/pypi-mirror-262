from setuptools import setup, find_packages
import datetime
try:
    # 只在包打包发布时需要
    with open('../requirements.txt') as f:
        install_requires = f.read().splitlines()
except:
    pass
def get_current_date_as_string():
    # 获取当前的日期时间
    current_datetime = datetime.datetime.now()
    # 将日期时间格式化为yearmonthdayHHMMSS.ffffff格式的字符串
    date_str = current_datetime.strftime('%Y%m%d%H%M%S')
    millisec_str = current_datetime.strftime('%f')[:3]  # 获取前3位表示毫秒
    formatted_datetime = f"{date_str}.{millisec_str}"
    return formatted_datetime

setup(
    name="CyberU",
    version="2.20."+get_current_date_as_string(),
    # packages=find_packages(),
    packages=['CyberU'],
    package_data={
        'CyberU': ['all.json'],
    },
    install_requires=install_requires,
    author="an-Underpriviliged-ZJUer",
    author_email="1737177378@qq.com",
    description="""
    Your spider tool based on selenium and an even general platform based on Python.
    version 2 means that We've beugn to use the latest public version of CyberU.""",
    long_description=open('../Kaleidoscope.md','r', encoding='utf-8').read(),
    long_description_content_type="text/markdown",


    url="https://github.com/an-Underpriviliged-ZJUer/Kaleidoscope_public",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        # ...
    ],
)
print('setup done.')