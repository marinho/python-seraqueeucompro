'''The setup and build script for the python-seraqueeucompro library.'''

__author__ = 'marinho@gmail.com'
__version__ = '0.1'


# The base package metadata to be used by both distutils and setuptools
METADATA = dict(
  name = "python-seraqueeucompro",
  version = __version__,
  py_modules = ['seraqueeucompro'],
  author='Marinho Brandao',
  author_email='marinho@gmail.com',
  description='A python wrapper around the Sera Que Eu Compro? API',
  license='Lesser Gnu Public License 3.0',
  #url='http://github.com/marinho/python-seraqueeucompro/',
  keywords='api',
)

# Extra package metadata to be used only if setuptools is installed
SETUPTOOLS_METADATA = dict(
  install_requires = ['setuptools', 'simplejson'],
  include_package_data = True,
  classifiers = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: Lesser Gnu Public License',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: Communications :: Chat',
    'Topic :: Internet',
  ],
  test_suite = 'seraqueeucompro_test.suite',
)
