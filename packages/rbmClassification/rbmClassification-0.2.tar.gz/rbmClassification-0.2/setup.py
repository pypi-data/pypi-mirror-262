from setuptools import setup, find_packages

setup(
    name='rbmClassification',
    version='0.2',
    packages=find_packages(),
    description='RBM Classification',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Pytorch',
    author_email='infol@pytorch.com',
    url='https://github.com/yourusername/my_package',
    license='MIT',
    install_requires=[
        # List of dependencies
    ],
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.org/classifiers/
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
