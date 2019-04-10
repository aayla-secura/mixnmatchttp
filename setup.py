from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='mixnmatchttp',
    version='0.2a-r1',
    url='https://github.com/aayla-secura/mixnmatchttp',
    author='AaylaSecura1138',
    author_email='aayla.secura.1138@gmail.com',
    description='Modular HTTP server: Auth, Caching, Proxy, and more',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        ],
    packages=find_packages(),
    install_requires=[
        'future>=0.12',
        'wrapt>=1',
        ],
    zip_safe=False)
