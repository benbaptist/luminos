# Luminos - Large Language Models in the Shell

## Overview

Luminos is a CLI utility that facilitates the integration of Large Language Models (LLMs) into the shell environment. By bridging the gap between traditional command-line tools and advanced language models, Luminos offers a unique and powerful way to interact with LLMs directly within the terminal.

## Features

- **Direct Filesystem Access:** Luminos provides LLMs with direct access to the filesystem, enabling tasks such as file manipulation and data processing.
- **Interactive Shell Integration:** Seamlessly integrate LLM capabilities into the command-line interface for an interactive experience.
- **Versatile Task Handling:** Perform a variety of tasks, from file operations to HTTP requests, with the assistance of LLMs.

## Installation
To install Luminos from the Git repository, use the following commands:

```
pip3 install wheel
pip3 install -r https://raw.githubusercontent.com/benbaptist/luminos/main/requirements.txt
pip3 install git+https://github.com/benbaptist/luminos
```

## Getting Started

Once installed, run `luminos` once to create your configuration in `~/.config/luminos`. Edit the configuration to specify your default LLM and, if applicable, API keys. Run `luminos` again to try it out.

Luminos currently supports OpenAI and Anthropic, with support for more providers (including Ollama) coming soon. 

For working within a specific directory, provide the path like so:

```
luminos path_to_dir
```

Upon starting Luminos, an interactive session is initiated, allowing the LLM to interact with the directory specified. Utilize the LLM's capabilities to manage tasks, ask questions, or perform actions within the shell environment.

## Examples

Explore a few examples of how Luminos can enhance your daily tasks:

- **File Management:** Instruct the LLM to rename, move, or modify files based on specific criteria.
- **Software Development:** Start Luminos within a project's directory, and ask it to make code revisions. Most of Luminos itself was written this way.
- **Data Analysis:** Leverage the LLM for data analysis, sorting, and summarization tasks.
- **Terminal Operations:** Get assistance and guidance from the LLM for executing commands and complex operations in the shell.

## Project Background

Luminos is an AI-driven project that showcases the capabilities of AI-generated content. The tool itself was utilized to develop most of the content within this project. This demonstrates the potential of AI-driven development and the seamless integration of AI-generated content to suit user needs.
