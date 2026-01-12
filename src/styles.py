"""
Beautiful CSS styling for PDF output, matching Antigravity's aesthetics
"""

ANTIGRAVITY_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

:root {
    /* Color Palette */
    --primary-bg: #ffffff;
    --secondary-bg: #f8f9fa;
    --text-primary: #1a1a1a;
    --text-secondary: #6c757d;
    --border-color: #e9ecef;
    --code-bg: #f6f8fa;
    --link-color: #0969da;
    --link-hover: #0550ae;
    
    /* Alert Colors */
    --alert-note: #0969da;
    --alert-note-bg: #ddf4ff;
    --alert-tip: #1a7f37;
    --alert-tip-bg: #dafbe1;
    --alert-important: #8250df;
    --alert-important-bg: #fbefff;
    --alert-warning: #9a6700;
    --alert-warning-bg: #fff8c5;
    --alert-caution: #cf222e;
    --alert-caution-bg: #ffebe9;
}

* {
    box-sizing: border-box;
}

@page {
    size: A4;
    margin: 2.5cm;
}

body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif;
    font-size: 11pt;
    line-height: 1.6;
    color: var(--text-primary);
    background: var(--primary-bg);
    max-width: 800px;
    margin: 0 auto;
}

/* Typography */
h1, h2, h3, h4, h5, h6 {
    font-weight: 600;
    line-height: 1.3;
    margin-top: 1.5em;
    margin-bottom: 0.5em;
    color: var(--text-primary);
    page-break-after: avoid;
}

h1 {
    font-size: 2em;
    border-bottom: 2px solid var(--border-color);
    padding-bottom: 0.3em;
    margin-top: 0;
}

h2 {
    font-size: 1.5em;
    border-bottom: 1px solid var(--border-color);
    padding-bottom: 0.3em;
}

h3 { font-size: 1.25em; }
h4 { font-size: 1.1em; }
h5 { font-size: 1em; }
h6 { font-size: 0.9em; color: var(--text-secondary); }

p {
    margin: 1em 0;
}

/* Links */
a {
    color: var(--link-color);
    text-decoration: none;
}

a:hover {
    color: var(--link-hover);
    text-decoration: underline;
}

/* Code Blocks */
code {
    font-family: 'JetBrains Mono', 'SF Mono', Monaco, 'Cascadia Code', 'Roboto Mono', Consolas, 'Courier New', monospace;
    font-size: 0.9em;
    background: var(--code-bg);
    padding: 0.2em 0.4em;
    border-radius: 3px;
    color: #e01e5a;
}

pre {
    background: var(--code-bg);
    border: 1px solid var(--border-color);
    border-radius: 6px;
    padding: 1em;
    overflow-x: auto;
    page-break-inside: avoid;
    margin: 1em 0;
}

pre code {
    background: none;
    padding: 0;
    color: var(--text-primary);
    font-size: 0.85em;
    line-height: 1.5;
}

/* Tables */
table {
    border-collapse: collapse;
    width: 100%;
    margin: 1em 0;
    page-break-inside: avoid;
}

th, td {
    border: 1px solid var(--border-color);
    padding: 0.6em 1em;
    text-align: left;
}

th {
    background: var(--secondary-bg);
    font-weight: 600;
}

tr:nth-child(even) {
    background: var(--secondary-bg);
}

/* Lists */
ul, ol {
    margin: 1em 0;
    padding-left: 2em;
}

li {
    margin: 0.5em 0;
}

/* Blockquotes - Used for Alerts */
blockquote {
    margin: 1em 0;
    padding: 0.8em 1em;
    border-left: 4px solid var(--alert-note);
    background: var(--alert-note-bg);
    border-radius: 6px;
    page-break-inside: avoid;
}

blockquote p {
    margin: 0.5em 0;
}

blockquote p:first-child {
    margin-top: 0;
}

blockquote p:last-child {
    margin-bottom: 0;
}

/* Alert Variations */
.alert-note {
    border-left-color: var(--alert-note);
    background: var(--alert-note-bg);
}

.alert-note::before {
    content: "📘 NOTE";
    display: block;
    font-weight: 600;
    color: var(--alert-note);
    margin-bottom: 0.5em;
}

.alert-tip {
    border-left-color: var(--alert-tip);
    background: var(--alert-tip-bg);
}

.alert-tip::before {
    content: "💡 TIP";
    display: block;
    font-weight: 600;
    color: var(--alert-tip);
    margin-bottom: 0.5em;
}

.alert-important {
    border-left-color: var(--alert-important);
    background: var(--alert-important-bg);
}

.alert-important::before {
    content: "❗ IMPORTANT";
    display: block;
    font-weight: 600;
    color: var(--alert-important);
    margin-bottom: 0.5em;
}

.alert-warning {
    border-left-color: var(--alert-warning);
    background: var(--alert-warning-bg);
}

.alert-warning::before {
    content: "⚠️ WARNING";
    display: block;
    font-weight: 600;
    color: var(--alert-warning);
    margin-bottom: 0.5em;
}

.alert-caution {
    border-left-color: var(--alert-caution);
    background: var(--alert-caution-bg);
}

.alert-caution::before {
    content: "🚨 CAUTION";
    display: block;
    font-weight: 600;
    color: var(--alert-caution);
    margin-bottom: 0.5em;
}

/* Horizontal Rules */
hr {
    border: none;
    border-top: 2px solid var(--border-color);
    margin: 2em 0;
}

/* Images */
img {
    max-width: 100%;
    height: auto;
    display: block;
    margin: 1em auto;
    border-radius: 6px;
}

/* Page Breaks */
.page-break {
    page-break-after: always;
}

/* Syntax Highlighting for Code */
.codehilite .hll { background-color: #ffffcc }
.codehilite .c { color: #8e908c; font-style: italic } /* Comment */
.codehilite .err { color: #c82829 } /* Error */
.codehilite .k { color: #8959a8; font-weight: bold } /* Keyword */
.codehilite .o { color: #3e999f } /* Operator */
.codehilite .cm { color: #8e908c; font-style: italic } /* Comment.Multiline */
.codehilite .cp { color: #8e908c; font-weight: bold } /* Comment.Preproc */
.codehilite .c1 { color: #8e908c; font-style: italic } /* Comment.Single */
.codehilite .cs { color: #8e908c; font-weight: bold; font-style: italic } /* Comment.Special */
.codehilite .gd { color: #c82829 } /* Generic.Deleted */
.codehilite .ge { font-style: italic } /* Generic.Emph */
.codehilite .gh { color: #4d4d4c; font-weight: bold } /* Generic.Heading */
.codehilite .gi { color: #718c00 } /* Generic.Inserted */
.codehilite .gp { color: #8e908c; font-weight: bold } /* Generic.Prompt */
.codehilite .gs { font-weight: bold } /* Generic.Strong */
.codehilite .gu { color: #3e999f; font-weight: bold } /* Generic.Subheading */
.codehilite .kc { color: #8959a8; font-weight: bold } /* Keyword.Constant */
.codehilite .kd { color: #8959a8; font-weight: bold } /* Keyword.Declaration */
.codehilite .kn { color: #3e999f; font-weight: bold } /* Keyword.Namespace */
.codehilite .kp { color: #8959a8; font-weight: bold } /* Keyword.Pseudo */
.codehilite .kr { color: #8959a8; font-weight: bold } /* Keyword.Reserved */
.codehilite .kt { color: #eab700 } /* Keyword.Type */
.codehilite .ld { color: #718c00 } /* Literal.Date */
.codehilite .m { color: #f5871f } /* Literal.Number */
.codehilite .s { color: #718c00 } /* Literal.String */
.codehilite .na { color: #4271ae } /* Name.Attribute */
.codehilite .nb { color: #4d4d4c } /* Name.Builtin */
.codehilite .nc { color: #eab700 } /* Name.Class */
.codehilite .no { color: #c82829 } /* Name.Constant */
.codehilite .nd { color: #3e999f } /* Name.Decorator */
.codehilite .ni { color: #4d4d4c } /* Name.Entity */
.codehilite .ne { color: #c82829 } /* Name.Exception */
.codehilite .nf { color: #4271ae } /* Name.Function */
.codehilite .nl { color: #4d4d4c } /* Name.Label */
.codehilite .nn { color: #eab700 } /* Name.Namespace */
.codehilite .nx { color: #4271ae } /* Name.Other */
.codehilite .py { color: #4d4d4c } /* Name.Property */
.codehilite .nt { color: #c82829 } /* Name.Tag */
.codehilite .nv { color: #c82829 } /* Name.Variable */
.codehilite .ow { color: #3e999f; font-weight: bold } /* Operator.Word */
.codehilite .w { color: #4d4d4c } /* Text.Whitespace */
.codehilite .mf { color: #f5871f } /* Literal.Number.Float */
.codehilite .mh { color: #f5871f } /* Literal.Number.Hex */
.codehilite .mi { color: #f5871f } /* Literal.Number.Integer */
.codehilite .mo { color: #f5871f } /* Literal.Number.Oct */
.codehilite .sb { color: #718c00 } /* Literal.String.Backtick */
.codehilite .sc { color: #4d4d4c } /* Literal.String.Char */
.codehilite .sd { color: #8e908c } /* Literal.String.Doc */
.codehilite .s2 { color: #718c00 } /* Literal.String.Double */
.codehilite .se { color: #f5871f } /* Literal.String.Escape */
.codehilite .sh { color: #718c00 } /* Literal.String.Heredoc */
.codehilite .si { color: #f5871f } /* Literal.String.Interpol */
.codehilite .sx { color: #718c00 } /* Literal.String.Other */
.codehilite .sr { color: #718c00 } /* Literal.String.Regex */
.codehilite .s1 { color: #718c00 } /* Literal.String.Single */
.codehilite .ss { color: #718c00 } /* Literal.String.Symbol */
.codehilite .bp { color: #4d4d4c } /* Name.Builtin.Pseudo */
.codehilite .vc { color: #c82829 } /* Name.Variable.Class */
.codehilite .vg { color: #c82829 } /* Name.Variable.Global */
.codehilite .vi { color: #c82829 } /* Name.Variable.Instance */
.codehilite .il { color: #f5871f } /* Literal.Number.Integer.Long */
"""

def get_css(theme='antigravity'):
    """
    Get CSS stylesheet for PDF generation
    
    Args:
        theme: The theme name (currently only 'antigravity' is supported)
        
    Returns:
        CSS string
    """
    if theme == 'antigravity':
        return ANTIGRAVITY_CSS
    return ANTIGRAVITY_CSS
