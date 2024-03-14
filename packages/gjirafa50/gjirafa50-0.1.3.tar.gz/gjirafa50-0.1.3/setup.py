from setuptools import setup, find_packages

setup(
    name='gjirafa50',
    version='0.1.3',
    description='A Python client for interacting with the Gjirafa50 API',
    author='Altin and Aiko',
    author_email='altinbb2@gmail.com',
    url='https://github.com/slumbersage/gjirafa50',
    packages=find_packages(),
    install_requires=[
        'requests',
        'fastapi',
        'pydantic',
        'beautifulsoup4'
    ],
)
