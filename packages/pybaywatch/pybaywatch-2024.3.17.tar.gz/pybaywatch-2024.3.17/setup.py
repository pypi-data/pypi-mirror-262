from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='pybaywatch',  # required
    version='2024.3.17',
    description='PyBAYWATCH: BAYWATCH in Python',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    author='Feng Zhu, Jessica Tierney',
    author_email='fengzhu@ucar.edu, jesst@arizona.edu',
    url='https://github.com/fzhu2e/pybaywatch',
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    zip_safe=False,
    keywords='Proxy System Models for Ocean Sediments',
    classifiers=[
        'Natural Language :: English',
        'Programming Language :: Python :: 3.11',
    ],
    install_requires=[
        'colorama',
        'oct2py',
    ],
)
