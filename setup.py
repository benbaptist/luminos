from setuptools import setup, find_packages

setup(
    name='luminos',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    python_requires='>=3.6',
    author='Luminos Team',
    author_email='info@luminos.example.com',
    description='Luminos: A Python framework designed for extending the capabilities of language models (LMs) within a Linux shell environment.',
    license='MIT',
    keywords='languagemodel tools shell',
    url='https://github.com/luminos',
)