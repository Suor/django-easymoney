from setuptools import setup

setup(
    name='django-easymoney',
    version='0.3.5',
    author='Alexander Schepanovski',
    author_email='suor.web@gmail.com',

    description='An easy MoneyField for Django.',
    long_description=open('README.rst').read(),
    url='http://github.com/Suor/django-easymoney',
    license='BSD',

    py_modules=['easymoney'],
    install_requires=[
        'django>=1.6',
        'babel'
    ],

    classifiers=[
        'Development Status :: 4 - Beta',
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
