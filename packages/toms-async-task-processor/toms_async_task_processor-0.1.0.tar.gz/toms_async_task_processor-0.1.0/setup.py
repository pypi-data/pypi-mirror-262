from setuptools import setup, find_packages

setup(
    name="toms_async_task_processor",
    version="0.1.0",
    author="Tom Samwel",
    author_email="tommiesamwel@gmail.com",
    description="A simple asynchronous task processor",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/tomsamwel/AsyncTaskProcessor.git",
    packages=find_packages(),
    install_requires=[
        "pydantic>=1.8.2",
        "pytest>=6.2.5",
        "pytest-asyncio>=0.15.1",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
