##############################################################
# NOTE!!! This is a Work-In-Progress version (Not yet tested)
##############################################################

# flake8: noqa F841

from setuptools import setup, find_packages

try:  # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError:  # for pip <= 9.0.3
    from pip.req import parse_requirements

reqs = parse_requirements('requirements.txt', session=False)

try:
    requirements = [str(ir.req) for ir in reqs]
except Exception as e:
    requirements = [str(ir.requirement) for ir in reqs]

setup(name='package-statistics',
      version='1.0.1',
      description='Tool to generate package statistics',
      license='Apache 2.0',
      author='Basabjit',
      author_email='basab401@yahoo.co.in',
      python_requires='>=3.6.*',
      packages=find_packages(),
      install_requires=requirements,
      classifiers=[
        'Intended Audience :: Python Developers',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.6',
      ],
      keywords=['Debian'])
