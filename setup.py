from setuptools import find_packages, setup

__version__ = "0.0.1"


setup(
    # package name in pypi
    name='spyne-delegate',
    # extract version from module.
    version=__version__,
    description="",
    long_description=open('README.rst').read(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Spyne',
        'Framework :: Spyne :: 2.12',
        'Framework :: Spyne :: 2.13',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],
    keywords='spyne delegate',
    author='Lars van de Kerkhof, Martijn Jacobs',
    author_email='lars@devopsconsulting.nl, martijn@devopsconsulting.nl',
    url='https://github.com/devopsconsulting/python-spynedelegate',
    license='BSD',
    packages=find_packages(
        exclude=['ez_setup', '*tests']),
    namespace_packages=[],
    include_package_data=True,
    zip_safe=False,
    # specify dependencies
    install_requires=[
        'setuptools',
        'spyne>=2.12',
        'lxml',
        'six'
    ],
    # mark test target to require extras.
    extras_require={
        'test': ['nose', 'coverage<4', 'suds-jurko'],
    },
)
