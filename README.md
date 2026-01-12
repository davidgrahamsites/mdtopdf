# MD to PDF Converter

A beautiful macOS application that converts Markdown files to professionally styled PDFs, matching Antigravity's visual aesthetics.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Platform](https://img.shields.io/badge/platform-macOS%20M1-lightgrey)
![Python](https://img.shields.io/badge/python-3.11-green)

## Features

- **Beautiful PDFs**: Antigravity-style design with modern typography
- **GitHub Flavored Markdown**: Full GFM support including tables, alerts, task lists
- **Mermaid Diagrams**: Renders flowcharts, Gantt charts, and other diagrams
- **Syntax Highlighting**: Code blocks with Pygments highlighting
- **Drag & Drop GUI**: Easy-to-use interface with live preview
- **Command Line**: Programmatic conversion support

## Known Issues

⚠️ **GUI .app bundle has stability issues** - The standalone .app may crash when clicking. 

**Workaround:** Use the command line interface instead:
```bash
conda activate mdtopdf-env
python -c "from src.converter import convert_file; convert_file('input.md', 'output.pdf')"
```

This works perfectly and is more reliable for batch processing. for markdown files
- Live split-view preview (markdown source + styled HTML)
- Clean, native macOS interface
- Progress indication during conversion

📦 **Comprehensive Markdown Support**
- GitHub Flavored Markdown
- Fenced code blocks with syntax highlighting
- Tables
- Task lists
- Emoji support
- And much more!

## Installation

### Prerequisites

- macOS 11.0 or later (Apple Silicon M1)
- Conda package manager

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/davidgrahamsites/mdtopdf.git
   cd mdtopdf
   ```

2. **Create conda environment**
   ```bash
   conda env create -f environment.yml
   conda activate mdtopdf-env
   ```

3. **Run the application**
   ```bash
   python src/main.py
   ```

## Building the .app

To create a standalone macOS application bundle:

```bash
# Activate the environment
conda activate mdtopdf-env

# Run the build script
python build_app.py
```

The `.app` will be created in the `dist/` directory. You can then:

```bash
# Run directly
open "dist/MD to PDF.app"

# Or install to Applications
cp -r "dist/MD to PDF.app" /Applications/
```

## Usage

### GUI Application

1. Launch the app
2. Drag & drop a `.md` file onto the drop zone (or click to browse)
3. Review the preview
4. Click "Convert to PDF"
5. Choose where to save your PDF

### Command Line (for developers)

```python
from src.converter import convert_file

# Convert a markdown file to PDF
convert_file('input.md', 'output.pdf')
```

## Sample Markdown Features

The converter supports all these markdown features:

```markdown
# Headers

## Subheaders with **bold** and *italic*

> [!NOTE]
> This is a note alert

> [!IMPORTANT]
> This is important information

### Code Blocks

​```python
def hello_world():
    print("Hello, World!")
​```

### Tables

| Feature | Supported |
|---------|-----------|
| Tables  | ✓         |
| Alerts  | ✓         |

### Lists

- [x] Completed task
- [ ] Pending task
```

## Project Structure

```
mdtopdf/
├── src/
│   ├── __init__.py       # Package initialization
│   ├── converter.py      # Core conversion logic
│   ├── styles.py         # CSS styling
│   ├── gui.py           # PyQt6 GUI application
│   └── main.py          # Entry point
├── tests/               # Unit and integration tests
├── environment.yml      # Conda environment
├── mdtopdf.spec        # PyInstaller configuration
├── build_app.py        # Build script
└── README.md           # This file
```

## Development

### Running Tests

```bash
conda activate mdtopdf-env
pytest tests/ -v
```

### Adding New Features

1. Core conversion logic: Edit `src/converter.py`
2. Styling: Edit `src/styles.py`
3. GUI: Edit `src/gui.py`

## Version Control

All changes are versioned locally with Git and synced to GitHub:

```bash
# Commit changes
git add .
git commit -m "Description of changes"

# Push to GitHub
git push origin main
```

## Technology Stack

- **Python 3.11** - Core language
- **PyQt6** - GUI framework
- **WeasyPrint** - PDF generation
- **Python-Markdown** - Markdown parsing
- **Pygments** - Syntax highlighting
- **PyInstaller** - App bundling

## License

MIT License - see LICENSE file for details

## Credits

Built with ❤️ using Antigravity

---

**Repository:** https://github.com/davidgrahamsites/mdtopdf
