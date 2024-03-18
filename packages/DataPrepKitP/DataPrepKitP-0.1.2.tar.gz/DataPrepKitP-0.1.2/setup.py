import setuptools 

def readme():
    with open('README.md') as f:
        README = f.read()
    return README

setuptools.setup( 
    name='DataPrepKitP',   
    version='0.1.2', 
    author="Roqaiah Bin Jamil", 
    author_email="roqaiahjamil@gmail.com", 
    description="A Python package for data preparation tasks.", 
    long_description=readme(),
    long_description_content_type='text/markdown',
    readme = "README.md",
    requires_python = ">=3.8",
    packages=setuptools.find_packages(), 
    install_requires=[
            'pandas',
            'numpy',
        ],
    classifiers=[ 
    "Programming Language :: Python :: 3", 
    "License :: OSI Approved :: MIT License", 
    "Operating System :: OS Independent", 
    ], 
) 