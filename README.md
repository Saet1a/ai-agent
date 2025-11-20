# AI Agent 

A lightweight, autonomous coding agent built with Python 3.13 and the **Google Gemini 2.0 Flash** model. This tool functions as a CLI assistant capable of performing local file system operations and code execution based on natural language prompts.

## Features

* **Autonomous Execution Loop**: Uses a ReAct-like loop (Reasoning + Acting) to determine necessary steps, execute them, and evaluate results.
* **File System Operations**:
    * `get_files_info`: List files and check file sizes/types.
    * `get_file_content`: Read file contents (with smart truncation for large files).
    * `write_file`: Create new files or overwrite existing ones (automatically handles directory creation).
* **Code Execution**:
    * `run_python_file`: Executes Python scripts in a subprocess and captures STDOUT/STDERR for the agent to analyze.
* **Sandboxed Environment**: File operations are restricted to a specific working directory (defaulting to `./calculator`) to prevent accidental system-wide changes.
* **Tooling Support**: Built with `uv` for modern Python package management.

## Installation

### Prerequisites
* Python 3.13+
* A Google Cloud Project with the Gemini API enabled.

### Setup

1.  **Clone the repository**
    ```bash
    git clone <repository-url>
    cd ai-agent
    ```

2.  **Install Dependencies**
    This project uses `uv` for dependency locking, but standard pip works via `pyproject.toml`.
    ```bash
    # Using pip
    pip install .

    # OR manually installing requirements
    pip install google-genai python-dotenv
    ```

3.  **Configure Environment**
    Create a `.env` file in the root directory and add your Gemini API key:
    ```bash
    GEMINI_API_KEY=your_actual_api_key_here
    ```

# Warning ⚠️: Experimental Project 
This tool allows an AI to execute code and modify files on your local machine. It is designed for educational purposes and does not implement full production-grade sandboxing (e.g., Docker containers).

Do not run this outside of a controlled directory.

## Usage

Run the agent via the command line by passing your prompt as arguments.

```bash
python main.py "Create a new python script that prints the fibonacci sequence"
