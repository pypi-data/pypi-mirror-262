from setuptools import setup

setup(
    name='kswutils',
    version='0.3.2',
    description='Justin utils at work',
    packages=['kswutils'],
    author_email='shuwa108@gmail.com',
    zip_safe=False,

    install_requires=[
        'numpy>=1.20.3',
        'scipy>=1.10.0',
        'matplotlib>=3.5.0',
        'natsort>=8.4.0',
        'pandas>=1.3.5',
    ],
)
