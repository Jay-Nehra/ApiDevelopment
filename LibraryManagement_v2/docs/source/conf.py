import os
import sys
sys.path.insert(0, os.path.abspath('../../')) 


project = 'LibraryManagement_v2'
copyright = '2024, Jayant Nehra'
author = 'Jayant Nehra'
release = '0.9'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx_rtd_theme'  
]

templates_path = ['_templates']
exclude_patterns = []


html_theme = "sphinx_rtd_theme"
# html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

# html_theme = 'alabaster'
html_static_path = ['_static']
