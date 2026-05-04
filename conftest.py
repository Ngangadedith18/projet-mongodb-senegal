"""
conftest.py — Configuration pytest.
Ajoute la racine du projet au sys.path pour que
les tests dans tests/ puissent importer db.py.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))