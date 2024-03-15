from setuptools import setup, find_packages

setup(
    name='pyndat',
    version='0.0.1',
    packages=find_packages(include=['pyndat']),
    license='Apache License 2.0',
    description='A toolbox for analyzing hydrological drought',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Savalan Naser Neisary',
    author_email='savalan.neisary@gmail.com',
    url='https://github.com/savalann/pydat',
    python_requires='>=3.9',
    install_requires=[
        'numpy>=1.26.4',
        'pandas>=2.2.1',
        'matplotlib>=3.8.0',
        'dataretrieval>=1.0.6',
    ],
    keywords=['Drought Analysis', 'Hydrology'],
    classifiers=[
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux"
    ]
)
