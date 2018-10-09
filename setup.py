from setuptools import setup, find_packages

setup(
    name='gureume',
    version='0.3',
    packages=find_packages(exclude=['__pycache__']),
    include_package_data=True,
    install_requires=[
        'click',
        'click-spinner',
        'colorama',
        'termcolor',
        'requests',
        'botocore',
        'boto3',
        'warrant',
        'GitPython'
    ],
    entry_points='''
        [console_scripts]
        gureume=gureume.cli:cli
    ''',
)
