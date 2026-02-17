# Python Docstring Generator

A Python application that automatically generates, validates, and formats docstrings using Google's Gemini API with PEP 257 compliance checking.

## Table of Contents

  - [Features](#features)
    - [Core Functionality](#core-functionality)
    - [UI Features](#ui-features)
  - [Project Structure](#project-structure)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Technologies Used](#technologies-used)
    - [Backend](#backend)
    - [Frontend](#frontend)
    - [Standards](#standards)
  - [Features in Detail](#features-in-detail)
    - [Parser Accuracy](#parser-accuracy)
    - [Docstring Styles](#docstring-styles)
    - [Validation Results](#validation-results)
  - [Troubleshooting](#troubleshooting)
  - [Example Usage](#example-usage)
  - [Acknowledgments](#acknowledgments)
  - [Additional Resources](#additional-resources)

## Features

### Core Functionality
- **AST-Based Parsing**: Accurately extracts function information from Python code
- **AI-Powered Generation**: Uses Gemini 2.0 Flash API to generate high-quality docstrings
- **Multi-Style Support**: Generates docstrings in Google, NumPy, and reST formats
- **PEP 257 Validation**: Ensures all generated docstrings comply with Python standards
- **Error Detection & Fixing**: Identifies and suggests fixes for code issues

### UI Features
- **Modern PyQt5 Interface**: Clean, intuitive, and production-ready design
- **File Upload & Paste**: Multiple ways to input source code
- **Real-time Parsing**: Live feedback on code structure and coverage
- **Visual Analytics**: Charts and graphs for validation results
- **Progress Tracking**: Real-time progress bars for generation tasks
- **Download Capability**: Export code with generated docstrings

## Project Structure

```
docstring_generator/
│
├── main.py                   # Application entry point
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── sample_code.py            # Sample input code to test the system
│
├── core/                     # Core functionality modules
│   ├── parser.py             # AST-based code parser
│   ├── generator.py          # Gemini API docstring generator
│   └── validator.py          # PEP 257 validator
│
├── ui/                       # User interface modules
│   ├── main_window.py        # Main application window
│   ├── parser_tab.py         # Main application window
│   ├── validator_tab.py      # Main application window
│   └── styles.py             # UI styling and themes
│
└── utils/                    # Utility modules
    ├── helpers.py            # Helper utilities for application
    └── config.py             # Configuration settings
```

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Gemini API key (Get one from [Google AI Studio](https://makersuite.google.com/app/apikey))

### Step-by-Step Installation

1. **Clone or Download the Project**
   ```bash
   cd docstring_generator
   ```

2. **Create a Virtual Environment** (Recommended)
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up API Key**
   
   You have two options:
   
   **Option A: Environment Variable**
   ```bash
   # On Windows
   set GEMINI_API_KEY=your_api_key_here
   
   # On macOS/Linux
   export GEMINI_API_KEY=your_api_key_here
   ```
   
   **Option B: In the Application**
   - You can enter the API key directly in the application UI

## Usage

### Running the Application

```bash
python main.py
```

### Quick Start Guide

1. **Enter API Key**
   - Paste your Gemini API key in the text field at the top
   - Click "Set API Key"

2. **Load Source Code**
   - Click "Upload Python File" to select a .py file, OR
   - Click "Paste Code" to paste code directly

3. **Parse the Code**
   - Click "Parse Code" to analyze the source
   - View detected functions and coverage statistics

4. **Generate Docstrings**
   - Switch to "Synthesis & Validation" tab
   - Select your preferred docstring style (Google/NumPy/reST)
   - Click "Generate Docstrings"
   - Wait for the AI to generate docstrings

5. **Validate Results**
   - Click "Validate PEP 257" to check compliance
   - Review validation results and statistics

6. **Download Output**
   - Click "Download Output" to save the enhanced code

## Workflow

```
Source Code Input
       ↓
AST Parsing (core/parser.py)
       ↓
Function Extraction
       ↓
Gemini API Generation (core/generator.py)
       ↓
Docstring Synthesis
       ↓
PEP 257 Validation (core/validator.py)
       ↓
Results & Download
```

## Technologies Used

### Backend
- **Python 3.8+**: Core programming language
- **AST Module**: Abstract Syntax Tree parsing for code analysis
- **Google Gemini API**: AI-powered docstring generation
- **pydocstyle**: PEP 257 compliance checking

### Frontend
- **PyQt5**: Modern GUI framework
- **Matplotlib**: Data visualization for validation results

### Standards
- **PEP 257**: Docstring conventions
- **Google Style**: Google's Python style guide
- **NumPy Style**: NumPy/SciPy documentation standard
- **reST**: reStructuredText format

## Features in Detail

### Parser Accuracy
- Real-time accuracy metrics
- Visual progress indicators
- Detailed function analysis
- Coverage statistics

### Docstring Styles

**Google Style**
```python
def function(arg1, arg2):
    """Summary line.

    Extended description of function.

    Args:
        arg1 (int): Description of arg1
        arg2 (str): Description of arg2

    Returns:
        bool: Description of return value
    """
```

**NumPy Style**
```python
def function(arg1, arg2):
    """Summary line.

    Extended description of function.

    Parameters
    ----------
    arg1 : int
        Description of arg1
    arg2 : str
        Description of arg2

    Returns
    -------
    bool
        Description of return value
    """
```

**reST Style**
```python
def function(arg1, arg2):
    """Summary line.

    Extended description of function.

    :param arg1: Description of arg1
    :type arg1: int
    :param arg2: Description of arg2
    :type arg2: str
    :returns: Description of return value
    :rtype: bool
    """
```

### Validation Results
- Comprehensive PEP 257 checking
- Visual charts showing compliance status
- Detailed error and warning messages
- File-wise status reporting

## Troubleshooting

### Common Issues

1. **"No API key configured" Error**
   - Solution: Make sure you've entered and set your Gemini API key

2. **Import Errors**
   - Solution: Ensure all dependencies are installed: `pip install -r requirements.txt`

3. **PyQt5 Display Issues**
   - Solution: On Linux, you may need: `sudo apt-get install python3-pyqt5`

4. **API Rate Limits**
   - Solution: Gemini has rate limits. Wait a few minutes between large batches

## Example Usage

Here's an example Python file you can test with:

```python
def calculate_area(length, width):
    return length * width

def greet_user(name, greeting="Hello"):
    return f"{greeting}, {name}!"

class DataProcessor:
    def process_data(self, data):
        result = []
        for item in data:
            result.append(item * 2)
        return result
```

Load this file, generate docstrings, and see the magic happen!

## Acknowledgments

- Google Gemini API for AI-powered generation
- PyQt5 community for excellent documentation
- pydocstyle maintainers for PEP 257 validation

## Additional Resources

- [PEP 257 Documentation](https://peps.python.org/pep-0257/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [NumPy Documentation Guide](https://numpydoc.readthedocs.io/)
- [Gemini API Documentation](https://ai.google.dev/docs)

---

**Made with ❤️ by Prakriti Lohumi**
