from setuptools import setup, find_packages

requirements = [
        'loguru',  # 依赖项列表
        'tqdm',
        'pyyaml',
        'wandb',
        'torch',
        'torchvision',
    ]

setup(
    name='collagenai',  # 包名称
    version='0.0.1',  # 包版本
    author='Ray',  # 作者名称
    author_email='170863868@qq.com',  # 作者邮箱
    description='CollaGen: Collaborative Learning Tool for Generative Model',  # 简短描述
    long_description=open('README.md').read(),  # 长描述，通常是README
    long_description_content_type='text/markdown',  # 长描述的内容类型，例如：text/markdown 或 text/plain
    url='https://github.com/fedcontinuum/CollaGen',  # 项目主页链接
    packages=find_packages(),  # 自动查找包含 '__init__.py' 的目录
    keywords=[
        "Distributed Machine Learning",
        "Federated Learning",
        "Collaborative Learning",
        "LLM",
        "Generative Model",
        "VLM",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",  # 支持的 Python 版本
        'License :: OSI Approved :: Apache Software License',  # 许可证
        'Operating System :: OS Independent',  # 操作系统
    ],
    install_requires=requirements,
    python_requires='>=3.11',  # Python 版本要求
)
