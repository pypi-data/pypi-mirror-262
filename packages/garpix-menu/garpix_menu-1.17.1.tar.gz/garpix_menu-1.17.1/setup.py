from setuptools import setup, find_packages
from os import path

here = path.join(path.abspath(path.dirname(__file__)), 'garpix_menu')

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='garpix_menu',
    version='1.17.1',
    description='',
    long_description=long_description,
    long_description_content_type='text/markdown',
    project_urls={
        'Documentation': 'https://docs.garpixcms.ru/packages/garpix_menu/',
        'GitHub': 'https://github.com/garpixcms/garpix_menu/',
        'Changelog': 'https://github.com/garpixcms/garpix_menu/blob/master/CHANGELOG.md/',
    },
    author='Garpix LTD',
    author_email='info@garpix.com',
    license='MIT',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Django >= 1.11, < 5',
        'django-mptt >= 0.9.1',
        'django-modeltranslation >= 0.16.2',
        'garpix_page >= 2.42.0-rc2',
        'garpix_utils >= 1.8.0'
    ],
)
