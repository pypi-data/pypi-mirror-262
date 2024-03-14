from setuptools import setup, find_packages

def readme():
  with open('README.md', 'r') as f:
    return f.read()

setup(
  name='SuiBotProject',
  version='1.0.0',
  author='Kujira',
  author_email='nopemo93@gmail.com',
  description='Sui Bot package',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com/DreamBreakk/SuiBotProject',
  packages=find_packages(),
  install_requires=['requests>=2.25.1'],
  classifiers=[
    'Programming Language :: Python :: 3.12',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='BetFuryBotProject',
  project_urls={
    'Documentation': 'https://github.com/DreamBreakk/SuiBotProject',
    'Source': 'https://github.com/DreamBreakk/SuiBotProject'
  },
  python_requires='>=3.7'
)