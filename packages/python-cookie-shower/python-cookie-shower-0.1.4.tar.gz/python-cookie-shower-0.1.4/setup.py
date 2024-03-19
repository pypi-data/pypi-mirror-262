from setuptools import setup 

setup(
    name='python-cookie-shower',
    packages=['CookiesShower'],
    version='0.1.4',
    description='This package for Windows Users those want to know their cookies (Google Chrome)',
    entry_points={
        'console_scripts': [
            'cookiesshower=CookiesShower.main:main'
        ]
    }
)