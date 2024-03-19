from setuptools import setup, find_packages

setup(
    name='dergipark_article_search',
    version='0.1.0',
    author= 'alistnel',
    author_email= 'aliustunelin@gmail.com',
    packages=find_packages(),
    install_requires=[
        'requests',
        'beautifulsoup4'
    ],
)
