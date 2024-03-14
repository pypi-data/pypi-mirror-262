from setuptools import setup, find_packages

with open('README.md') as f:
    description = f.read()

setup(
    name='templify',
    version='0.0.15',
    packages=find_packages(),
    install_requires=[
        'django>=4.2',
        'typer~=0.9.0'
    ],
    author='Yunusov Abdulmajid',
    author_email='toepammiddle@email.com',
    description='This package provides templates for you to start developing your application',
    entry_points={
        "console_scripts": [
            "templify = templify:run",
        ],
    },
    url='https://github.com/toEpam/templify',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    long_description=description,
    long_description_content_type='text/markdown',
    # download_url='https://github.com/toEpam/templify/archive/refs/heads/master.zip'
)