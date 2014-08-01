from setuptools import setup

setup(
    name='django-easymoney',
    version='0.0.1',
    author='Alexander Schepanovski',
    author_email='suor.web@gmail.com',

    description='An easy MoneyField for Django.',
    long_description=open('README.rst').read(),
    url='http://github.com/Suor/django-easymoney',
    license='BSD',

    packages=['simplemoney'],
    install_requires=[
        'django>=1.6',
    ],

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',

        'Framework :: Django',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
