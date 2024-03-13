# Luminos Python Project

## Overview
Luminos is a Python framework designed for extending the capabilities of language models (LMs) within a Linux shell environment. It focuses on iterative execution, allowing language models to interact with the system's file system and perform tasks until specific objectives are achieved.

## Features
- Core execution loop designed for persistent interaction within a Linux shell.
- Toolset for interfacing directly with filesystem operations (FileIO), HTTP requests, and managing language models (LLMs).

## Installation
To install Luminos, please follow these steps:

1. Clone the Luminos repository.
2. Navigate to the Luminos root directory.
3. Use the command `pip install .` to install the Luminos package.

## Usage
After installation, Luminos can be used within a Python script as follows:

```python
from luminos.core import Core

core_instance = Core()
core_instance.run_llm("Your Task Here")
```

## Requirements
- Python 3.6 or newer
- requests library for HTTP operations

## Contributing
Contributions to Luminos are welcome. Please submit pull requests or issues as needed.