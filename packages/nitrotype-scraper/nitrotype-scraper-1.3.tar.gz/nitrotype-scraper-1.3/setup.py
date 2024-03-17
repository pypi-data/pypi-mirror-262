from setuptools import setup, find_packages
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='nitrotype-scraper',
    version='1.3',
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        'cloudscraper',
        'beautifulsoup4',
    ],
    author='Malakai',
    author_email='Almightyslider2@gmail.com',
    description="A package to use the nitrotype api and get player or team stats along with accessing the Nitrotype bootstrap",
    url='https://github.com/yourusername/nitrotype-scraper',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
