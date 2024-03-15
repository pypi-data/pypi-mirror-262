'''
Use of this source code is governed by a MIT-style license that can be found in the LICENSE file.
Created on July 06, 2017
@author: Niels Lubbes


For upgrading we use the following commands:

sage -python setup.py pytest            # make sure everything works
sage -python setup.py sdist upload      # increase version number in setup.py before upload!


For more information see:

https://xebia.com/blog/a-practical-guide-to-using-setup-py/
https://python-packaging.readthedocs.io/en/latest/minimal.html
https://pypi.python.org/pypi?%3Aaction=list_classifiers
'''

from setuptools import setup

setup( name='linear_series',
       version='8',
       description='Base point analysis for linear series of curves in the plane.',
       classifiers=[
           'Development Status :: 3 - Alpha',
           'License :: OSI Approved :: MIT License',
           'Programming Language :: Python :: 3',
           'Topic :: Scientific/Engineering :: Mathematics',
           ],
      keywords='linear series',
      url='http://github.com/niels-lubbes/linear_series',
      author='Niels Lubbes',
      license='MIT',
      package_dir={'linear_series': 'src/linear_series', 'tests':'src/tests'},
      packages=['linear_series', 'tests'],
      setup_requires=['pytest-runner'],
      tests_require=['pytest'],
      entry_points={
          'console_scripts': ['run-linear-series=linear_series.__main__:main'],
      },
      include_package_data=True,
      zip_safe=False )

