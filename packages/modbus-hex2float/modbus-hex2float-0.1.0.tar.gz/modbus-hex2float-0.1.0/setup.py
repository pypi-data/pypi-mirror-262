from setuptools import setup, find_packages

setup(
    name='modbus-hex2float',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        # 필요한 의존성이 있다면 여기에 추가
    ],
    # 다른 메타데이터를 추가할 수 있습니다.
    author='Your Name',
    author_email='your@email.com',
    description='A short description of your project',
    #long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/your_username/my_package',
    classifiers=[
        'Programming Language :: Python :: 3',
        # 다른 분류도 추가할 수 있습니다.
    ],
)