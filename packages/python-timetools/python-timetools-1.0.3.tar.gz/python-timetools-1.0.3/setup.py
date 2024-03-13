import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="python-timetools",
    version="1.0.3",
    author="neason",
    author_email="xgx93610@gmail.com",
    description="python time tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/xuguox/timetools",
    packages=setuptools.find_packages(),
    python_requires='>=3.7.0',
    install_requires=["requests"],
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    project_urls={
        "Source": "https://github.com/xuguox/timetools",
    },
)