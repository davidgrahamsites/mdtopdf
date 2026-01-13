"""
Markdown to PDF converter using PyQt6's built-in PDF printer
"""

import re
import sys
import markdown
from markdown.extensions import fenced_code, tables, codehilite, toc
from pygments.formatters import HtmlFormatter

# Must set this before importing QtWebEngine
from PyQt6.QtCore import Qt, QUrl, QMarginsF, QSizeF
from PyQt6.QtWidgets import QApplication
QApplication.setAttribute(Qt.ApplicationAttribute.AA_ShareOpenGLContexts)

from PyQt6.QtGui import QPageSize, QPageLayout
from PyQt6.QtWebEngineCore import QWebEngineSettings
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtPrintSupport import QPrinter
from .styles import get_css


class MarkdownConverter:
    """Convert Markdown files to beautifully styled PDFs"""
    
    def __init__(self, theme='antigravity'):
        """
        Initialize the converter
        
        Args:
            theme: CSS theme to use for PDF generation
        """
        self.theme = theme
        self.md = markdown.Markdown(
            extensions=[
                'fenced_code',
                'tables',
                'codehilite',
                'toc',
                'pymdownx.superfences',
                'pymdownx.emoji',
                'pymdownx.highlight',
                'pymdownx.inlinehilite',
                'pymdownx.keys',
                'pymdownx.magiclink',
                'pymdownx.mark',
                'pymdownx.smartsymbols',
                'pymdownx.tasklist',
                'pymdownx.tilde',
            ],
            extension_configs={
                'codehilite': {
                    'css_class': 'codehilite',
                    'linenums': False,
                    'guess_lang': False,
                },
                'pymdownx.highlight': {
                    'css_class': 'codehilite',
                    'linenums': False,
                    'guess_lang': False,
                },
                'pymdownx.superfences': {
                    'custom_fences': [],
                },
                'pymdownx.emoji': {
                    'emoji_index': lambda: {},
                    'emoji_generator': lambda x, y: y,
                },
            }
        )
    
    
    def _process_mermaid_diagrams(self, markdown_text):
        """
        Process mermaid code blocks and convert them to mermaid div elements
        
        Args:
            markdown_text: Raw markdown text
            
        Returns:
            Processed markdown with mermaid divs
        """
        # Pattern to match mermaid code blocks
        mermaid_pattern = r'```mermaid\s*\n(.*?)\n```'
        
        def replace_mermaid(match):
            mermaid_code = match.group(1)
            # Convert to a div that mermaid.js will render
            return f'<div class="mermaid">\n{mermaid_code}\n</div>\n'
        
        return re.sub(mermaid_pattern, replace_mermaid, markdown_text, flags=re.DOTALL)
    
    def _process_github_alerts(self, markdown_text):
        """
        Process GitHub-style alerts like > [!NOTE]
        
        Args:
            markdown_text: Raw markdown text
            
        Returns:
            Processed markdown with alert classes
        """
        # Pattern to match GitHub-style alerts
        alert_pattern = r'> \[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]\s*\n((?:> .*\n?)*)'
        
        def replace_alert(match):
            alert_type = match.group(1).lower()
            content = match.group(2)
            # Remove the '> ' prefix from each line
            content = re.sub(r'^> ', '', content, flags=re.MULTILINE)
            # Create a blockquote with the appropriate class
            return f'<blockquote class="alert-{alert_type}">\n{content}\n</blockquote>\n'
        
        return re.sub(alert_pattern, replace_alert, markdown_text, flags=re.MULTILINE)
    
    def _wrap_html(self, html_content):
        """
        Wrap HTML content in a complete HTML document
        
        Args:
            html_content: The converted HTML content
            
        Returns:
            Complete HTML document string
        """
        css = get_css(self.theme)
        return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Markdown Document</title>
    <style>
    {css}
    </style>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
    <script>
        mermaid.initialize({{ 
            startOnLoad: true,
            theme: 'default',
            securityLevel: 'loose'
        }});
    </script>
</head>
<body>
{html_content}
</body>
</html>
"""
    
    def markdown_to_html(self, markdown_text):
        """
        Convert markdown text to HTML
        
        Args:
            markdown_text: Raw markdown content
            
        Returns:
            HTML string
        """
        # Process mermaid diagrams first (before markdown conversion)
        processed_md = self._process_mermaid_diagrams(markdown_text)
        
        # Process GitHub-style alerts
        processed_md = self._process_github_alerts(processed_md)
        
        # Convert to HTML
        html = self.md.convert(processed_md)
        
        # Wrap in complete HTML document
        return self._wrap_html(html)
    
    def markdown_to_pdf(self, markdown_text, output_path, margin_mm=25):
        """
        Convert markdown text to PDF using PyQt6's PDF printer
        
        Args:
            markdown_text: Raw markdown content
            output_path: Path to save the PDF
            margin_mm: Margin size in millimeters (default: 25)
        """
        # Ensure QApplication exists
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        
        # Convert markdown to HTML
        html_content = self.markdown_to_html(markdown_text)
        
        # Create web view for rendering
        web_view = QWebEngineView()
        web_view.settings().setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
        
        # Set HTML content
        web_view.setHtml(html_content)
        
        # Create PDF printer
        printer = QPrinter(QPrinter.PrinterMode.HighResolution)
        printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
        printer.setOutputFileName(output_path)
        
        # Set page size and margins
        page_layout = QPageLayout()
        page_layout.setPageSize(QPageSize(QPageSize.PageSizeId.A4))
        page_layout.setOrientation(QPageLayout.Orientation.Portrait)
        page_layout.setUnits(QPageLayout.Unit.Millimeter)
        page_layout.setMargins(QMarginsF(margin_mm, margin_mm, margin_mm, margin_mm))
        printer.setPageLayout(page_layout)
        
        # Function to handle PDF printing after page load
        pdf_written = [False]  # Use list to allow modification in closure
        
        def on_pdf_written(pdf_bytes):
            """Callback when PDF is ready"""
            with open(output_path, 'wb') as f:
                f.write(pdf_bytes)
            pdf_written[0] = True
            app.quit()
        
        def on_load_finished(ok):
            """Callback when page loading is finished"""
            if ok:
                # Wait for mermaid diagrams to render (JavaScript needs time)
                from PyQt6.QtCore import QTimer
                def print_after_render():
                    web_view.page().printToPdf(on_pdf_written)
                
                # Wait 2 seconds for mermaid to render diagrams
                QTimer.singleShot(2000, print_after_render)
            else:
                print("Failed to load HTML content")
                app.quit()
        
        web_view.loadFinished.connect(on_load_finished)
        
        # Process events to allow loading
        app.exec()
    
    def markdown_file_to_pdf(self, input_file, output_file, margin_mm=25):
        """
        Convert a markdown file to PDF
        
        Args:
            input_file: Path to input .md file
            output_file: Path to output .pdf file
            margin_mm: Margin size in millimeters (default: 25)
        """
        with open(input_file, 'r', encoding='utf-8') as f:
            markdown_text = f.read()
        
        self.markdown_to_pdf(markdown_text, output_file, margin_mm)
        return output_file


def convert_file(input_path, output_path, theme='antigravity'):
    """
    Convenience function to convert a markdown file to PDF
    
    Args:
        input_path: Path to input .md file
        output_path: Path to output .pdf file
        theme: CSS theme to use
        
    Returns:
        Path to the generated PDF
    """
    converter = MarkdownConverter(theme=theme)
    return converter.markdown_file_to_pdf(input_path, output_path)
