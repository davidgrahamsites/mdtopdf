"""
Main GUI application for MD to PDF Converter
"""

import sys
import os
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFileDialog, QSplitter, QTextEdit, QMessageBox,
    QProgressBar, QMenuBar, QMenu, QStatusBar, QSlider
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QMimeData, QUrl
from PyQt6.QtGui import QDragEnterEvent, QDropEvent, QAction, QFont
from PyQt6.QtWebEngineWidgets import QWebEngineView
from .converter import MarkdownConverter


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
        
        # Create container for page-like appearance
        preview_container = QWidget()
        preview_container.setStyleSheet("""
            QWidget {
                background: #e9ecef;
                padding: 20px;
            }
        """)
        preview_container_layout = QVBoxLayout()
        preview_container.setLayout(preview_container_layout)
        
        self.html_preview = QWebEngineView()
        self.html_preview.setStyleSheet("""
            QWebEngineView {
                background: white;
                border: 2px solid #dee2e6;
                border-radius: 4px;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            }
        """)
        preview_container_layout.addWidget(self.html_preview)
        
        right_layout.addWidget(preview_container)
        
        self.splitter.addWidget(left_panel)
        self.splitter.addWidget(right_panel)
        self.splitter.setVisible(False)
        
        main_layout.addWidget(self.splitter)
        
        # Margin control
        margin_panel = QWidget()
        margin_panel.setVisible(False)
        margin_layout = QHBoxLayout()
        margin_panel.setLayout(margin_layout)
        
        margin_label = QLabel("📏 PDF Margins:")
        margin_label.setStyleSheet("font-weight: 500; font-size: 13px; color: #1a1a1a;")
        margin_layout.addWidget(margin_label)
        
        self.margin_slider = QSlider(Qt.Orientation.Horizontal)
        self.margin_slider.setMinimum(10)  # 10mm
        self.margin_slider.setMaximum(50)  # 50mm
        self.margin_slider.setValue(25)    # 25mm default
        self.margin_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.margin_slider.setTickInterval(10)
        self.margin_slider.valueChanged.connect(self.on_margin_changed)
        margin_layout.addWidget(self.margin_slider)
        
        self.margin_value_label = QLabel("25mm")
        self.margin_value_label.setStyleSheet("font-weight: bold; color: #0969da; min-width: 50px;")
        margin_layout.addWidget(self.margin_value_label)
        
        self.margin_panel = margin_panel
        main_layout.addWidget(margin_panel)
        
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
            self.margin_panel.setVisible(True)
            self.convert_btn.setEnabled(True)
            
            # Update status
            self.status_bar.showMessage(f"Loaded: {Path(file_path).name}")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load file:\n{str(e)}")
    
    def on_margin_changed(self, value):
        """Handle margin slider changes"""
        # Update label
        self.margin_value_label.setText(f"{value}mm")
        
        # Update preview with new margins
        if self.current_markdown:
            html = self.converter.markdown_to_html(self.current_markdown)
            from .styles import get_css
            # Add CSS with updated body padding
            styled_html = f"""
            <style>
            {get_css()}
            body {{
                padding: {value}mm !important;
            }}
            </style>
            {html}
            """
            self.html_preview.setHtml(styled_html)
    
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
        
        # Show progress and disable button
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Indeterminate progress
        self.convert_btn.setEnabled(False)
        self.status_bar.showMessage("Converting...")
        
        # Store output path for later
        self.output_path = output_path
        
        # Use QTimer to do conversion after UI updates
        from PyQt6.QtCore import QTimer
        QTimer.singleShot(100, self.do_conversion)
    
    def do_conversion(self):
        """Actually perform the conversion (in main thread)"""
        try:
            # Get margin value from slider
            margin_mm = self.margin_slider.value()
            
            converter = MarkdownConverter()
            converter.markdown_file_to_pdf(self.current_file, self.output_path, margin_mm)
            self.on_conversion_finished(self.output_path)
        except Exception as e:
            self.on_conversion_error(str(e))
    
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
