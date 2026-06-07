"""Pytest configuration: add project root to sys.path so tests can import modules."""
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
