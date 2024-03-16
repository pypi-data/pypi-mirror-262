# Copyright 2024 The casbin Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from setuptools import setup, find_packages, __version__


with open("README.md", "r") as readme_file:
    readme = readme_file.read()


setup(
    name="casbin-async-postgresql-watcher",
    author="hsluoyz",
    author_email="hsluoyz@gmail.com",
    description="Async casbin role watcher to be used for monitoring updates to policies for PyCasbin",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/pycasbin/async-postgres-watcher",
    packages=find_packages(),
    install_requires=open('requirements.txt', encoding='utf-16').read().splitlines(),
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: Apache Software License",
    ],
)
