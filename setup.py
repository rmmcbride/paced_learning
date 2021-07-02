from setuptools import setup, find_packages

requires = [
    'flask',
    'flask-sqlalchemy',
    'psycopg2',
]

setup(
    name='paced_learning',
    version='0.0',
    description='A paced learning app built with Flask',
    author='Rachael McBride',
    author_email='mcbride.r@gmail.com',
    keywords='web flask',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires
)