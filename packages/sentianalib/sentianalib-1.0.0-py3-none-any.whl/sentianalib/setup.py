from setuptools import setup

setup(
    name='sentianalib',
    version='1.0.0',
    packages=['sentianalib'],
    install_requires=[
        'beautifulsoup4>=4.12.3',
        'textblob>=0.18.0',
        'selenium>=4.18.1',
        'webdriver_manager>=4.0.1',
        # Add more dependencies as needed
    ],
    # other metadata...
)