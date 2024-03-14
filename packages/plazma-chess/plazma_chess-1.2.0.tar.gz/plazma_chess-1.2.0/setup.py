from setuptools import setup, find_packages

with open('README.md', 'rb') as f:
    description = f.read().decode('utf-16le').encode('utf-8').decode('utf-8')

setup(
    name='plazma_chess',
    version='1.2.0',
    packages=find_packages(),
    install_requires=[],
    long_description=description,
    long_description_content_type="text/markdown",
)