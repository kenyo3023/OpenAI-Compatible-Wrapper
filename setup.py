from setuptools import setup, find_packages

setup(
    name="openai_compatible_wrapper",
    version="0.1.0",
    package_dir={"": "src"},
    packages=find_packages("src"),
    install_requires=[
        "openai>=1.0.0",
    ],
    author="kenyo3023",
    author_email="kenyo3023@gmail.com",
    description="A wrapper for OpenAI API with default parameter support",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/kenyo3023/OpenAI-Compatible-Wrapper",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)