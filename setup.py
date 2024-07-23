from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="dify-cli",
    version="1.0.3",
    author="yujiang",
    author_email="501540155@qq.com",
    description="A package for interacting with the Dify Service-API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/qdyujiang002/dify-client-python",
    license='MIT',
    packages=['dify_client'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "httpx",
        "httpx-sse",
        "pydantic",
        "StrEnum",
    ],
    keywords='dify nlp ai language-processing',
    include_package_data=True,
)
