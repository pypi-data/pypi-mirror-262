from setuptools import setup, Extension # python标准库内置编译辅助


# 读取 README.md 文件的内容
import os
import codecs
project_root = os.path.abspath(os.path.dirname(__file__))
with codecs.open(os.path.join(project_root, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

print(project_root)

# Extension会根据文件后缀，选择不同的编译器进行编译
check_os_extension = Extension(
    'my_tiny_check_os_tools', 
    sources=['check_os.c']
);
  

setup(
    # 发布pip后的包名 -> 即pip install后的压缩文件名称 -> 即解压后的文件夹名称
    name="zyn-py-pkg-test-2024-03-13", 
    # 包的版本控制，可配合pip install zyn-py-pkg-test-2024-03-13=0.0.x
    version="0.0.1",  
    # 需要的Python环境最低版本
    python_requires=">=3.7", 
    # 第三方依赖
    install_requires=[
    
    ],
    # 此字段用于定义其他语言的模块，由于此Demo加载的Extension的源码文件后缀名是.c，所以会自动调用gcc编译为二进制文件
    ext_modules=[check_os_extension],
    # 简短描述, 用于PyPI搜索优化
    description="This is a test python module", 
    # 使用文档
    long_description=long_description, 
    # 使用文档原文件类型
    long_description_content_type="text/markdown", 
    # owner姓名
    author="Your Name",
    # owner邮箱
    author_email="you@example.com", 
    # 项目源码仓库地址
    url="https://github.com/your/repo", 
    # 开源协议标准
    license="MIT", 
    # PyPI过滤搜索优化
    classifiers=[  
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3.7',  # 应与python_requires设置的最低版本一致或更低
    ]
)