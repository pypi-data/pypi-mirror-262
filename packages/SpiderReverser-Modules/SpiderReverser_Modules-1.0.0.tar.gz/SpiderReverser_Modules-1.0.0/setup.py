from setuptools import setup, find_packages

setup(
    name='SpiderReverser_Modules',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        "requests",
        "httpx",
        "httpx[http2]",
        "fake_useragent",
        "loguru"
        # 添加其他依赖
    ],
    author="SpiderReverser",
    author_email="spiderreverser@foxmail.com",
    description="SpiderReverser person modules",
    url="https://github.com/SpiderReverser/SpiderReverser_Modules",
)
