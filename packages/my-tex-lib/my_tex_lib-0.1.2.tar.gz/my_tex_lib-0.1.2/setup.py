from setuptools import setup, find_packages


def readme():
  with open('README.md', 'r') as f:
    return f.read()


setup(
  name='my_tex_lib',
  version='0.1.2',
  author='nkocherin',
  author_email='nkocherin@inbox.ru',
  description='Test module',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com/nick15431543/python_course/tree/main/hw_2',
  packages=find_packages(),
  install_requires=['requests>=2.25.1'],
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='files speedfiles ',
  project_urls={
    'GitHub': 'https://github.com/nick15431543/python_course/tree/main/hw_2'
  },
  python_requires='>=3.6'
)