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
    entry_points={
        'console_scripts': [
            'luminos = luminos.__main__:main',
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries",
        "Operating System :: POSIX :: Linux",
    ],
)