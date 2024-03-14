from setuptools import setup, find_packages

# with open('README.md') as f:
#     description = f.read()

setup(
    name='templify',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'django>=4.2'
    ],
    # entry_points={
    #     "console_scripts": [
    #         "pixegami-hello = pixegami:hello",
    #     ],
    # },
    # long_description=description,
    # long_description_content_type='text/markdown',
)