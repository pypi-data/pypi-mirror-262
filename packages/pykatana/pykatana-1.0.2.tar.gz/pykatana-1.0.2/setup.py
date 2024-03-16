#
# بسم الله الرحمن الرحیم
# اللهم صل علی محمد و آل محمد
# ---------------------------
# Created on Fri Mar 15 2024
#
# Copyright (c) 2024 Abolfazl Danayi
# adanayidet@gmail.com
#

from setuptools import setup, find_packages

setup(
    name="pykatana",
    version="1.0.2",
    author="Abolfazl Danayi",
    author_email="adanayidet@gmail.com",
    description="A Python-based build system for creating static websites with ease and flexibility.",
    long_description="""
# pykatana

**pykatana** is a Python-based build system designed for creating static websites with ease and flexibility.

## Overview

A **Katana** project comprises several essential components:

1. **`src/make.py`**: This file contains a `run` function responsible for building the website. Whenever the contents of the `src` folder change, this function is triggered. It takes an EZJinja object and processes the templates to generate the website.

2. **Jinja2 Templates**: Found in the `src/templates` directory, these templates form the backbone of your website's structure and content. They provide the flexibility to customize and design your site according to your requirements.

3. **Static Files**: The `src/static` directory houses static files such as CSS, JavaScript, images, and other assets required for your website. These files are served directly to users without any processing.

4. **Meta Technique Files**: Located in the `src/meta` directory, these files enable dynamic content generation for your website. Using the meta technique, you can access and utilize metadata stored in JSON files within your Jinja2 templates. This allows for dynamic updates and customization of your site based on external data sources.

## Installation

### Method 1: Install via pip

You can install **pykatana** using pip:
```bash
pip install pykatana
```

### Method 2: Use prebuilt executables
Download prebuilt executables from the Releases section.

### Method 3: Clone the repository
Clone the repository and copy "pykatana/pykatana" inside your project folder. You can then access **pykatana** using:

```bash
python3 -m pykatana [args]
```

### Method 4: Clone and build from source
1. Clone the repository:
```bash
git clone https://github.com/adanayi/pykatana.git
cd pykatana
```
2. Copy the necessary files:
```bash
cp -r pykatana/__make/* .
```
3. On Linux:
```bash
./make.sh
```
On Windows:
```bash
./make.bat
```
On Mac:
**pykatana** never supports mac.

4. The executable will be generated as ./dist/pykatana (or pykatana.exe).

## Usage
### How to use pykatana?
#### Method1: Executable files (prebuilt or built)
```bash
pykatana [args]
```


#### Method2: With python packages (pip3 or clone)
```bash
python3 -m pykatana [args]
```

### Usage modes
#### Development server
cd to your project's folder (root), then simply run **pykatana** without any args. If the folder is empty, pykatana initializes it and opens the development server. Otherwise, it sets up the development server, allowing you to continue your development.

#### Deploy
The output of your project will always be put into the ./build folder alongside ./src. You can statically serve this folder. If you want to only build the folder without starting the development server, you can use:
```bash
pykatana -b
```
or
```bash
python3 -m pykatana -b
```

## License
This project is licensed under the GNU General Public License v3.0.
    """,
    long_description_content_type="text/markdown",
    url="https://github.com/adanayi/pykatana",
    packages=find_packages(),
    install_requires=[
        "jinja2",
        "watchdog",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)
