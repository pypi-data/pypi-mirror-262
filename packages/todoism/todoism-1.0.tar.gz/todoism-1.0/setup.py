from setuptools import setup, find_packages

setup(
    name='todoism',
    version='1.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'todoism=todoism.main:main',
        ],
    },
    install_requires=[],
    author='Qichen Liu',
    author_email='liuqichne@email.com',
    description='A simple but interactive and intuitive todo CLI',
    url='https://github.com/Q1CHENL/todoism',
)
