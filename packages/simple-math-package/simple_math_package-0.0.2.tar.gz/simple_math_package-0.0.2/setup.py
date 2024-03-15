from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="simple_math_package",
    version="0.0.2",
    author="matheus_eiji_faria_komatsu",
    author_email="matheuskomatsu@hotmail.com",
    description="This package is used for simple math operations. It's used as an exercise to understand how to create and distribute a package.",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MatheusKomatsu/SimpleMathPackage",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)