# Configuration file for the Sphinx documentation builder.

# -- Project information

project = '华中科技大学课程攻略'
copyright = '2025, yuhang'
author = 'Yuhang Su'

# 如果你删除了 lumache.py，请把含有 'lumache' 的行注释掉或删除
# 比如 extensions 里的 'lumache'
release = '0.1'
version = '0.1.0'

# -- General configuration

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
]

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}
intersphinx_disabled_domains = ['std']

templates_path = ['_templates']

# -- Options for HTML output

html_theme = 'sphinx_rtd_theme'

# -- Options for EPUB output
epub_show_urls = 'footnote'
