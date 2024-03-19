from setuptools import setup, find_packages

with open("README.md", "r",encoding='utf-8') as fh:
  long_description = fh.read()

setup(
  name="zhr_utils",
  version="0.0.1",
  author="zaoheren",
  author_email="zaoheren@hotmail.com",
  description="常用方法库",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/zaoheren/zhr_utils",
  packages=find_packages(),
  classifiers=[
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: MIT License",
  "Operating System :: OS Independent",
  ],
)