from setuptools import setup, find_packages



with open('requirements.txt','r') as file:
    data = file.read()
    requirements = data.split()

setup(
    name='hollarek',
    version='0.3.0',
    author='Daniel Hollarek',
    author_email='daniel.hollarek@googlemail.com',
    description='A brief description of the hollarek package',
    url='https://github.com/Somerandomguy10111/hollarek',
    packages=find_packages(),
    python_requires='>=3.8',
    install_requires=requirements
)
