# PDF Organizer

## Purpose

The PDF Organizer is a Python script designed to automatically organize PDF files and shortcuts to PDF files on your Windows desktop. It categorizes the files based on their names, with special handling for AI and ChatGPT-related PDFs, and moves them into appropriately named folders.

## Features

- Organizes both PDF files and shortcuts to PDF files
- Uses OpenAI's GPT model to dynamically categorize files based on their names
- Automatically categorizes AI and ChatGPT-related PDFs into a dedicated folder
- Handles file operations asynchronously for improved performance
- Implements error handling and logging for robust operation

## How It Works

1. **File Detection**: The script scans the desktop for PDF files and shortcuts to PDF files.

2. **Categorization**:
   - Files with "ChatGPT", "AI", or "Open AI" in their names are automatically categorized as "ChatGPT".
   - For other files, the script uses OpenAI's GPT model to suggest a category based on the filename.

3. **Organization**: The script creates category folders within a main "Organized PDFs" folder on the desktop and moves the files into their respective category folders.

4. **Shortcut Handling**: For PDF shortcuts, the script creates a new shortcut in the appropriate category folder and deletes the original from the desktop.

## Technical Implementation

- **Asynchronous Operations**: Uses Python's `asyncio` for concurrent processing of files and API calls.
- **Path Handling**: Utilizes `pathlib` for cross-platform compatibility and easier path manipulations.
- **API Integration**: Integrates with OpenAI's API using the `openai` Python library.
- **Caching**: Implements `functools.lru_cache` to cache API responses and reduce redundant calls.
- **Logging**: Uses Python's `logging` module for informative console output and error tracking.
- **Type Hinting**: Employs type hints for improved code readability and IDE support.

## Requirements

- Python 3.7+
- OpenAI Python library
- pywin32 library (for handling Windows shortcuts)

## Setup and Usage

1. Ensure you have Python installed on your system.
2. Install required libraries:
   ```
   pip install openai pywin32
   ```
3. Clone or download the script to your local machine.
4. Replace `'your_api_key_here'` in the script with your actual OpenAI API key.
5. Run the script:
   ```
   python pdf_organizer.py
   ```

## Note

This script is designed for use on Windows systems and requires access to the OpenAI API. Ensure you have the necessary permissions and API access before running the script.

## Customization

You can customize the script by modifying the constants at the top of the file, such as `DESKTOP_PATH`, `ORGANIZED_FOLDER_NAME`, and `CHATGPT_KEYWORDS`.

## Contributions

Contributions, issues, and feature requests are welcome. Feel free to check [issues page] if you want to contribute.

## License

[MIT](https://choosealicense.com/licenses/mit/)
