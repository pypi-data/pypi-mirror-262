from setuptools import setup, find_packages

setup(
    name='caretML',
    version='0.1.0',
    author='David Condrey',
    author_email='davidcondrey@protonmail.com',
    packages=find_packages(),
    license='LICENSE',
    description='A utility library for machine learning inspired by lodash.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'numpy==1.22.3',
        'networkx==2.6.3',
        'python-louvain==0.15',  # community detection library, often installed with "community" as an alias
        'matplotlib==3.5.1',
        'plotly==5.6.0',
        'scipy==1.7.3',
        'scikit-learn==1.0.2',
        'scikit-image==0.18.3',  # skimage
        'numba==0.55.1',
        'tensorflow==2.8.0',  # For keras
        'pymoo==0.5.0',
    ],
)
