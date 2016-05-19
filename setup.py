#!/usr/bin/env python

from setuptools import setup


conf = dict(name='query-selector',
            version='0.99.4',
            author='Jason Dusek',
            author_email='jason.dusek@gmail.com',
            url='https://github.com/solidsnack/query-selector',
            install_requires=['oset',
                              'six',
                              'sqlparse',
                              'stackclimber'],
            setup_requires=['pytest-runner', 'setuptools'],
            tests_require=['flake8', 'pytest', 'tox'],
            description='Organize app queries in an annotated SQL file.',
            packages=['query_selector'],
            package_data={'query_selector': ['example.sql']},
            classifiers=['Environment :: Console',
                         'Intended Audience :: Developers',
                         'License :: OSI Approved :: MIT License',
                         'Operating System :: Unix',
                         'Operating System :: POSIX',
                         'Programming Language :: Python',
                         'Programming Language :: Python :: 2.6',
                         'Programming Language :: Python :: 2.7',
                         'Programming Language :: Python :: 3.5',
                         'Topic :: Software Development',
                         'Development Status :: 4 - Beta'])


if __name__ == '__main__':
    setup(**conf)
