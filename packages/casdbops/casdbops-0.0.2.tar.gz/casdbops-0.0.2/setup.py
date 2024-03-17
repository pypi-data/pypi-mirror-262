from setuptools import setup, find_packages
import os

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()     
   
HYPEN_E_DOT='-e .'

def get_requirements(file_path):
    requirements=[]
    print(os.listdir(os.getcwd()),"\n",os.listdir(os.path.dirname(os.getcwd())))
    with open(file_path) as file_obj:
        requirements=file_obj.readlines()
        requirements=[req.replace("\n","") for req in requirements]

        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)

    return requirements

__version__ = "0.0.2"
REPO_NAME = "cassandra_conector_db"
PKG_NAME= "casdbops"
AUTHOR_USER_NAME = "pranav-c01"
AUTHOR_EMAIL = "pranavc430@gmail.com"

setup(
    name=PKG_NAME,
    version=__version__,
    author=AUTHOR_USER_NAME,
    author_email=AUTHOR_EMAIL,
    description="A python package for connecting with database.",
    long_description=open('README.md').read(),
    long_description_content='text/markdown',
    long_description_content_type='text/markdown',
    url=f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}",
    project_urls={"Bug Tracker": f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}/issues"},
    packages=find_packages(),
    install_requires = ["astrapy==0.7.7","pandas","numpy","ensure","pytest==7.1.3"]

    )



