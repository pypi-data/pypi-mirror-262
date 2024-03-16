from setuptools import setup, find_packages
from distutils.core import setup
setup(
  name = 'myjive',         # How you named your package folder (MyLib)
  packages = find_packages(),   # Chose the same as "name"
  version = '0.1.1-5',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Personal implementation of jive C++ library in Python',   # Give a short description about your library
  author = 'Anne Poot',                   # Type in your name
  author_email = 'a.poot-1@tudelft.nl',      # Type in your E-Mail
  url = 'https://gitlab.tudelft.nl/apoot1/myjive',   # Provide either the link to your github or to your website
  download_url = 'https://gitlab.tudelft.nl/apoot1/myjive/-/archive/v0.1.1/myjive-v0.1.1.tar.gz',    # I explain this later on
  keywords = [],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
    'matplotlib==3.5.2',
    'numba==0.56.4',
    'numpy==1.23.5',
    'pytest==7.1.2',
    'scikit-sparse==0.4.12',
    'scipy==1.8.1',
  ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Scientific/Engineering :: Mathematics',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.10',      #Specify which pyhton versions that you want to support
  ],
)
