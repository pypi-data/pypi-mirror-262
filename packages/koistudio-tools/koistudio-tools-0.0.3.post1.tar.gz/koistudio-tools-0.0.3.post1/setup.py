import setuptools
import os

# Readme
readme_file = os.path.join(os.path.dirname(__file__), 'README.md')
with open(readme_file, 'r') as f:
    long_description = f.read()

# Module dependencies
requirements_file = os.path.join(os.path.dirname(__file__), 'requirements.txt')
with open(requirements_file, 'r') as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name='koistudio-tools',
    version='0.0.3-R1',
    author='KoiReader Technologies',
    author_email='support@koireader.com',
    description='KoiStudio common tools',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://gitlab.com/koireader/internal/label-studio-tools',
    packages=setuptools.find_packages(),
    license='Apache License 2.0',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=requirements,
)
