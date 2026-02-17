"""
Configuration settings for the Docstring Generator application.
"""

import os

# API Configuration
GEMINI_API_KEY = os.getenv("set_your_own_api_key",)  # Set your API key here or as environment variable

# Docstring Styles
DOCSTRING_STYLES = {
    "Google": "Google style docstring format",
    "NumPy": "NumPy/SciPy style docstring format",
    "reST": "reStructuredText style docstring format"
}

# Model Configuration
GEMINI_MODEL = "gemini-2.5-flash"

# UI Configuration
WINDOW_TITLE = "Python Docstring Generator"
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 900