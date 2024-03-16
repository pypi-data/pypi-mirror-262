from setuptools import setup, find_packages

setup(
    name='danty',
    version='1.0.1',
    packages=find_packages(),
    install_requires=['psutil'], 
    author='Danty.aburai',
    author_email='danty.aburai@gmail.com',
    description='Uma biblioteca Python para mineração de criptomoedas',
    url='https://github.com/danty.aburai/danty-miner',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
