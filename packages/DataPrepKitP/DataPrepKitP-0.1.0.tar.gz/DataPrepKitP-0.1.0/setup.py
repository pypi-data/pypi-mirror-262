import setuptools 

setuptools.setup( 
    name='DataPrepKitP',   
    version='0.1.0', 
    author="Roqaiah Bin Jamil", 
    author_email="roqaiahjamil@gmail.com", 
    description="A Python library for data preparation tasks.", 
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