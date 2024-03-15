from setuptools import setup, find_packages

setup(
    name='hcattesta',
    version='0.0.5',
    packages=find_packages(),
    install_requires=[
        # 任何依赖项都在这里列出
        'httpcat-sdk',
        'myhttpcat',
        'httpcatlab'
    ],
    author='dwge1',
    author_email='dwge1234@outlook.com',
    description='hcattesta',
    license='MIT',
    keywords='hcattesta',
    url='https://github.com/dwge1/hcattesta',
    download_url='https://github.com/dwge1/hcattesta',
    project_urls={
        'Source':'https://github.com/dwge1/hcattesta',
    }
)

