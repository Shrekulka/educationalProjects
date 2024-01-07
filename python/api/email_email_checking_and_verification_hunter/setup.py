from setuptools import setup, find_packages

setup(
    name='email_email_checking_and_verification_hunter',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'requests',
        'prettytable',
        'colorama',
        'logging',
        'typing',
    ],
    entry_points={
        'console_scripts': [
            'hunter-client = email_email_checking_and_verification_hunter.main:main',
        ],
    },
)
