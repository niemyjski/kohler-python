from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

setup(name='kohler',
    version='0.0.5',
    description='Python library for talking to Kohler devices',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/niemyjski/kohler-python',
    author='Blake Niemyjski',
    author_email='bniemyjski@gmail.com',
    license='Apache',
    packages=['kohler'],
    install_requires=[
        'requests',
    ],
    zip_safe=False)
