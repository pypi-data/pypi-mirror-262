from setuptools import setup

setup(
    name='sentianaylib',
    version='1.0.2',
    description='A Python package for sentiment analysis',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/chameleonlabs2021/sentianaylib',
    author_email='chameleonlabs2021@gmail.com',
    packages=['sentianaylib'],
    install_requires=[
        'beautifulsoup4>=4.12.3',
        'textblob>=0.18.0',
        'selenium>=4.18.1',
        'webdriver_manager>=4.0.1',
        # Add more dependencies as needed
    ],
    # other metadata...
)