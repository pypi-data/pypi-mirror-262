from setuptools import setup, find_packages


with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="py_configurator_logger",
    version='1.1',
    packages=find_packages(),
    description="A custom logger which includes json log format and plain text log format",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[],
    author="Abbas Shaikh",
    author_email="abbasshxikh77@gmail.com",
    license="MIT"
)
