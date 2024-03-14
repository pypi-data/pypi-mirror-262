from setuptools import setup, find_packages
from os import path


here = path.join(path.abspath(path.dirname(__file__)), 'tabbed_admin')

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='django-tabbed-admin-for-garpixcms',
    version='1.1.0',
    description='',
    long_description=long_description,
    url='https://github.com/garpixcms/django-tabbed-admin',
    author='Garpix LTD',
    author_email='info@garpix.com',
    license='MIT',
    packages=find_packages(exclude=['testproject', 'testproject.*']),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
        'Programming Language :: Python :: 3.8',
    ],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'garpixcms >= 1.7.0',
        'Django >= 3.1, < 5'
    ],
)

