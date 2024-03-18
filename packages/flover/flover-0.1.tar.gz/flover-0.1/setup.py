from setuptools import setup, find_packages

setup(
    name='flover',  # 你的包名
    version='0.1',  # 版本号
    packages=find_packages(),  # 自动查找所有包
    install_requires=[  # 你的包依赖的其他包
        'requests',
    ],
    # 其他元数据
    author='Orange',
    author_email='learningpro.dong@gmail.com',
    description='An easy RAG runtime',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/learningpro/flover',  # 你的项目主页
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
)