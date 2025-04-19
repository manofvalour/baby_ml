from setuptools import setup, find_packages
from typing import List


HYPEN_E_DOT = "-e ."
def get_requirements(file_path:str)->List[str]:

    '''function for accessing the requirements.txt in the setup.py packages'''

    requirements=[]
    with open(file_path, 'r') as file_obj:
        requirements=file_obj.readlines()
        [req.replace('\n', '') for req in requirements]
        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)

    return requirements


setup(
    name='baby_predict',
    version='0.0.1',
    description="ML model for predicting the baby weight at birth based on several factors",
    author= 'Emmanuel Ajala',
    author_email='ajalae2@gmail.com',
    maintainer= 'Emmanuel',
    packages=find_packages(),
    intall_requires=get_requirements('requirements.txt')  #getting requirements through the get_requirements function
)