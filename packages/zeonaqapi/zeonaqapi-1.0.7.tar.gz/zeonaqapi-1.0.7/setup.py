# setup.py

from setuptools import setup, find_packages

setup(
    name='zeonaqapi',
    version='1.0.7',
    packages=find_packages(),
    install_requires=[
        # Add your project's dependencies here
        'requests', 'pandas', 'monsterapi', 'openai'
    ],
    author='Craig Carmichael',
    author_email='operations@darkhorsestech.com',
    description='An API client library for the ZeonAQ API.',
    license='MIT',
    url='https://github.com/darkhorsestech/zeonaqapi',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)
