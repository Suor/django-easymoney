from setuptools import setup

setup(
    name='django-easymoney',
    version='0.6',
    author='Alexander Schepanovski',
    author_email='suor.web@gmail.com',

    description='An easy MoneyField for Django.',
    long_description=open('README.rst').read(),
    url='http://github.com/Suor/django-easymoney',
    license='BSD',

    py_modules=['easymoney'],
    install_requires=[
        'django>=1.6',
        'babel>=2.2.0',
        'six',
    ],

    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',

        'Framework :: Django',
        'Framework :: Django :: 1.6',
        'Framework :: Django :: 1.7',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
