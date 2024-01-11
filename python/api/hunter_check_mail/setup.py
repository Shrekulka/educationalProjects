from setuptools import setup, find_packages

setup(
    name='hunter_check_mail',
    version='0.2',
    author="Shrekulka",
    description="A package for email verification via Hunter API",
    packages=find_packages(where="hunter_check_mail"),
    install_requires=[
        "certifi==2023.11.17",
        "charset-normalizer==3.3.2",
        "colorama==0.4.6",
        "idna==3.6",
        "numpy==1.26.3",
        "pandas==2.1.4",
        "prettytable==3.9.0",
        "python-dateutil==2.8.2",
        "pytz==2023.3.post1",
        "requests==2.31.0",
        "six==1.16.0",
        "tzdata==2023.4",
        "urllib3==2.1.0",
        "wcwidth==0.2.13",
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    entry_points={
        'console_scripts': [
            'hunter_check_mail = app:main',
        ],
    }
)
