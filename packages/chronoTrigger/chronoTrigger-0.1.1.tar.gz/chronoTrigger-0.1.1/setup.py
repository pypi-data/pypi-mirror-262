from setuptools import setup

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='chronoTrigger',
    version='0.1.1',
    description='Library for working with intervals',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=['chronoTrigger'],
    author_email='dmitriybreus5@gmail.com',
    zip_safe=False
)