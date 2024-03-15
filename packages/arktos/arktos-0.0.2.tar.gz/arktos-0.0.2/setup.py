from setuptools import setup, find_packages

setup(
    name='arktos',
    version='0.0.2',
    packages=find_packages(),
    description='A brief description of Arktos',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',  # This assumes you have a README.md
    author='W Robert Long',
    author_email='longrob604@gmail.com',
    url='https://github.com/yourusername/arktos',
    install_requires=[
        # dependencies
    ],
)