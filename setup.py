from setuptools import setup, find_packages



with open('requirements.txt','r') as file:
    data = file.read()
    requirements = data.split()

setup(
    name='hollarek',
    version='0.9.1',
    author='Daniel Hollarek',
    author_email='daniel.hollarek@googlemail.com',
    description='Collection of general python utilities for future projects',
    url='https://github.com/Somerandomguy10111/hollarek',
    packages=find_packages(),
    package_data={'hollarek.devtools.spoof': ['*']},
    python_requires='>=3.8',
    include_package_data=True,
    install_requires=requirements
)
