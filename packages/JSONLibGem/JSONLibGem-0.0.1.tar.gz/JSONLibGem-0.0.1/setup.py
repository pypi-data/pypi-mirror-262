from setuptools import setup, find_packages


def readme():
  with open('README.md', 'r') as f:
    return f.read()


setup(
  name='JSONLibGem',
  version='0.0.1',
  author='Gemion',
  author_email='ms.m4x@yandex.ru',
  description='This is the simplest module for serializing and deserializing json.',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='',
  packages=find_packages(),
  install_requires=[],
  classifiers=[
    'Programming Language :: Python :: 3.12',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='json ',
  project_urls={
  },
  python_requires='>=3.6'
)