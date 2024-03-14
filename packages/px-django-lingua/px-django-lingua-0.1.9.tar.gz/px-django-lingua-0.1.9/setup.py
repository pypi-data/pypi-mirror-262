import os
import re
import setuptools


with open('README.md', 'r') as fh:
    long_description = fh.read()


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(package, '__init__.py')).read()

    return re.search('__version__ = [\'"]([^\'"]+)[\'"]', init_py).group(1)


version = get_version('pxd_lingua')


setuptools.setup(
    name='px-django-lingua',
    version=version,
    author='Alex Tkachenko',
    author_email='preusx.dev@gmail.com',
    license='MIT License',
    description='Simple translations implementation for django models.',
    install_requires=[
        'px-settings>=0.1.2,<0.2.0',
        'django>=2.2,<6',
    ],
    extras_require={
        'dev': [
            'pytest',
            'pytest-watch>=4.2,<5.0',
            'pytest-django>=4.8,<5.0',
            'setuptools',
            'django-environ',
            'psycopg2-binary',
            'twine',
        ],
    },
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(exclude=(
        'tests', 'tests.*', 'pilot', 'pilot.*'
    )),
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',

        'Programming Language :: Python :: 3',

        'Intended Audience :: Developers',
        'Topic :: Utilities',

        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
