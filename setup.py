from setuptools import setup, find_packages

setup(
    name='luminos',
    version='0.3',
    packages=find_packages(),
    install_requires=[
        'requests',
        'docstring_parser'
    ],
    python_requires='>=3.6',
    author='Ben Baptist',
    description='Luminos: CLI Utility for Integrating LLMs into the Shell',
    license='MIT',
    keywords='languagemodel tools shell',
    url='https://github.com/benbaptist/luminos',
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
