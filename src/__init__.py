"""
MD to PDF Converter - A beautiful markdown to PDF converter for macOS
"""

__version__ = "1.0.0"

from .converter import MarkdownConverter, convert_file
from .styles import get_css

__all__ = ['MarkdownConverter', 'convert_file', 'get_css']
