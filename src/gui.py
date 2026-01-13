"""
Main GUI application for MD to PDF Converter
"""

import sys
import os
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFileDialog, QSplitter, QTextEdit, QMessageBox,
    QProgressBar, QMenuBar, QMenu, QStatusBar
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QMimeData, QUrl
from PyQt6.QtGui import QDragEnterEvent, QDropEvent, QAction, QFont
from PyQt6.QtWebEngineWidgets import QWebEngineView
from .converter import MarkdownConverter


class ConversionThread(QThread):
    """Background thread for PDF conversion"""
    finished = pyqtSignal(str)
    error = pyqtSignal(str)
    
    def __init__(self, input_file, output_file, theme='antigravity'):
        super().__init__()
        self.input_file = input_file
        self.output_file = output_file
        self.theme = theme
    
    def run(self):
        try:
            converter = MarkdownConverter(theme=self.theme)
            converter.markdown_file_to_pdf(self.input_file, self.output_file)
            self.finished.emit(self.output_file)
        except Exception as e:
            self.error.emit(str(e))


class DropWidget(QWidget):
    """Widget that accepts drag and drop of markdown files"""
    file_dropped = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Create a container widget for the drop zone
        self.drop_container = QWidget()
        self.drop_container.setStyleSheet("""
            QWidget {
                border: 3px dashed #0969da;
                border-radius: 12px;
                background: #f8f9fa;
            }
            QWidget:hover {
                background: #e9ecef;
                border-color: #0550ae;
            }
        """)
        self.drop_container.setMinimumHeight(200)
        
        container_layout = QVBoxLayout()
        self.drop_container.setLayout(container_layout)
        
        # Icon label
        icon_label = QLabel("📄")
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setStyleSheet("font-size: 48px; border: none; background: transparent;")
        container_layout.addWidget(icon_label)
        
        # Text label
        text_label = QLabel("Drag & Drop Markdown File Here")
        text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        text_label.setStyleSheet("font-size: 16px; color: #6c757d; border: none; background: transparent;")
        container_layout.addWidget(text_label)
        
        # Browse button
        self.browse_btn = QPushButton("📁 Click to Browse")
        self.browse_btn.clicked.connect(self.open_file_dialog)
        self.browse_btn.setStyleSheet("""
            QPushButton {
                background: #0969da;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: 500;
                margin: 10px 40px;
            }
            QPushButton:hover {
                background: #0550ae;
            }
        """)
        container_layout.addWidget(self.browse_btn)
        
        layout.addWidget(self.drop_container)
        self.setLayout(layout)
    
    def open_file_dialog(self):
        """Open file selection dialog"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Markdown File",
            "",
            "Markdown Files (*.md *.markdown);;All Files (*.*)"
        )
        if file_path:
            self.file_dropped.emit(file_path)
    
    def dragEnterEvent(self, event: QDragEnterEvent):
        """Handle drag enter event"""
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if urls and urls[0].toLocalFile().endswith(('.md', '.markdown')):
                event.acceptProposedAction()
    
    def dropEvent(self, event: QDropEvent):
        """Handle drop event"""
        urls = event.mimeData().urls()
        if urls:
            file_path = urls[0].toLocalFile()
            if file_path.endswith(('.md', '.markdown')):
                self.file_dropped.emit(file_path)


class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.current_file = None
        self.current_markdown = None
        self.converter = MarkdownConverter()
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the user interface"""
        self.setWindowTitle("MD to PDF Converter")
        self.setMinimumSize(1200, 800)
        
        # Apply modern styling
        self.setStyleSheet("""
            QMainWindow {
                background: #ffffff;
            }
            QPushButton {
                background: #0969da;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: 500;
            }
            QPushButton:hover {
                background: #0550ae;
            }
            QPushButton:disabled {
                background: #e9ecef;
                color: #6c757d;
            }
            QTextEdit {
                border: 1px solid #e9ecef;
                border-radius: 6px;
                padding: 10px;
                font-family: 'JetBrains Mono', monospace;
                font-size: 12px;
            }
        """)
        
        # Create menu bar
        self.create_menu_bar()
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Title
        title = QLabel("MD to PDF Converter")
        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #1a1a1a; margin: 20px;")
        main_layout.addWidget(title)
        
        # Drop widget
        self.drop_widget = DropWidget()
        self.drop_widget.file_dropped.connect(self.load_file)
        main_layout.addWidget(self.drop_widget)
        
        # Preview splitter
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left: Markdown preview
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        left_panel.setLayout(left_layout)
        
        left_label = QLabel("Markdown Source")
        left_label.setStyleSheet("font-weight: bold; font-size: 14px; color: #1a1a1a;")
        left_layout.addWidget(left_label)
        
        self.markdown_preview = QTextEdit()
        self.markdown_preview.setReadOnly(True)
        left_layout.addWidget(self.markdown_preview)
        
        # Right: HTML preview
        right_panel = QWidget()
        right_layout = QVBoxLayout()
        right_panel.setLayout(right_layout)
        
        right_label = QLabel("PDF Preview")
        right_label.setStyleSheet("font-weight: bold; font-size: 14px; color: #1a1a1a;")
        right_layout.addWidget(right_label)
        
        self.html_preview = QWebEngineView()
        right_layout.addWidget(self.html_preview)
        
        self.splitter.addWidget(left_panel)
        self.splitter.addWidget(right_panel)
        self.splitter.setVisible(False)
        
        main_layout.addWidget(self.splitter)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.convert_btn = QPushButton("📄 Convert to PDF")
        self.convert_btn.clicked.connect(self.convert_to_pdf)
        self.convert_btn.setEnabled(False)
        button_layout.addWidget(self.convert_btn)
        
        self.open_btn = QPushButton("📂 Open Another File")
        self.open_btn.clicked.connect(self.open_file_dialog)
        button_layout.addWidget(self.open_btn)
        
        button_layout.addStretch()
        main_layout.addLayout(button_layout)
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        main_layout.addWidget(self.progress_bar)
    
    def create_menu_bar(self):
        """Create the menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        
        open_action = QAction("Open Markdown File", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_file_dialog)
        file_menu.addAction(open_action)
        
        convert_action = QAction("Convert to PDF", self)
        convert_action.setShortcut("Ctrl+P")
        convert_action.triggered.connect(self.convert_to_pdf)
        file_menu.addAction(convert_action)
        
        file_menu.addSeparator()
        
        quit_action = QAction("Quit", self)
        quit_action.setShortcut("Ctrl+Q")
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)
        
        # Help menu
        help_menu = menubar.addMenu("Help")
        
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def open_file_dialog(self):
        """Open file selection dialog"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Markdown File",
            "",
            "Markdown Files (*.md *.markdown);;All Files (*.*)"
        )
        if file_path:
            self.load_file(file_path)
    
    def load_file(self, file_path):
        """Load a markdown file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                self.current_markdown = f.read()
            
            self.current_file = file_path
            self.markdown_preview.setPlainText(self.current_markdown)
            
            # Generate HTML preview
            html = self.converter.markdown_to_html(self.current_markdown)
            from .styles import get_css
            styled_html = f"<style>{get_css()}</style>{html}"
            self.html_preview.setHtml(styled_html)
            
            # Show preview panels
            self.drop_widget.setVisible(False)
            self.splitter.setVisible(True)
            self.convert_btn.setEnabled(True)
            
            # Update status
            self.status_bar.showMessage(f"Loaded: {Path(file_path).name}")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load file:\n{str(e)}")
    
    def convert_to_pdf(self):
        """Convert the current markdown to PDF"""
        if not self.current_file:
            QMessageBox.warning(self, "No File", "Please load a markdown file first.")
            return
        
        # Ask for output location
        default_name = Path(self.current_file).stem + ".pdf"
        output_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save PDF As",
            default_name,
            "PDF Files (*.pdf)"
        )
        
        if not output_path:
            return
        
        # Start conversion in background thread
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Indeterminate progress
        self.convert_btn.setEnabled(False)
        self.status_bar.showMessage("Converting...")
        
        self.conversion_thread = ConversionThread(
            self.current_file,
            output_path
        )
        self.conversion_thread.finished.connect(self.on_conversion_finished)
        self.conversion_thread.error.connect(self.on_conversion_error)
        self.conversion_thread.start()
    
    def on_conversion_finished(self, output_path):
        """Handle successful conversion"""
        self.progress_bar.setVisible(False)
        self.convert_btn.setEnabled(True)
        self.status_bar.showMessage(f"PDF saved: {Path(output_path).name}")
        
        # Ask if user wants to open the PDF
        reply = QMessageBox.question(
            self,
            "Success",
            "PDF created successfully!\n\nWould you like to open it?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            os.system(f'open "{output_path}"')
    
    def on_conversion_error(self, error_msg):
        """Handle conversion error"""
        self.progress_bar.setVisible(False)
        self.convert_btn.setEnabled(True)
        self.status_bar.showMessage("Conversion failed")
        QMessageBox.critical(self, "Conversion Error", f"Failed to convert:\n{error_msg}")
    
    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(
            self,
            "About MD to PDF Converter",
            "<h3>MD to PDF Converter v1.0.0</h3>"
            "<p>Convert Markdown files to beautifully styled PDFs</p>"
            "<p>Matching Antigravity's aesthetics</p>"
            "<p><b>Features:</b></p>"
            "<ul>"
            "<li>GitHub Flavored Markdown support</li>"
            "<li>Syntax highlighting</li>"
            "<li>Tables and alerts</li>"
            "<li>Beautiful typography</li>"
            "</ul>"
        )


def main():
    """Application entry point"""
    # Set up global exception handler to prevent crashes
    def exception_handler(exc_type, exc_value, exc_traceback):
        """Handle uncaught exceptions"""
        import traceback
        print("Uncaught exception:", exc_type, exc_value)
        traceback.print_exception(exc_type, exc_value, exc_traceback)
    
    sys.excepthook = exception_handler
    
    app = QApplication(sys.argv)
    app.setApplicationName("MD to PDF Converter")
    app.setOrganizationName("Antigravity")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
