from setuptools import setup, find_packages

setup(
    dependency_links=[],
    name="piedmont",
    version="0.1.6",
    description="A python library that helps you to build ProtoPie Bridge App or plugin more efficiently",
    long_description=open("README.md").read(),
    long_description_content_type=("text/markdown"),
    author="Nestor",
    author_email="admin@nestor.me",
    url="https://github.com/nestorrid/piedmont",
    packages=find_packages(),
    install_requires=[
        "bidict==0.23.1; python_version >= '3.8'",
        "certifi==2025.1.31; python_version >= '3.6'",
        "charset-normalizer==3.4.1; python_version >= '3.7'",
        "h11==0.14.0; python_version >= '3.7'",
        "idna==3.10; python_version >= '3.6'",
        "python-engineio==4.11.2; python_version >= '3.6'",
        "python-socketio==5.12.1; python_version >= '3.8'",
        "pyyaml==6.0.2; python_version >= '3.8'",
        "requests==2.32.3; python_version >= '3.8'",
        "simple-websocket==1.1.0; python_version >= '3.6'",
        "urllib3==2.3.0; python_version >= '3.9'",
        "websocket-client==1.8.0; python_version >= '3.8'",
        "wsproto==1.2.0; python_full_version >= '3.7.0'",
    ],
)
