"""Mocha Pro startup script.

This script is used for AYON related functionality.
"""
from ayon_core.pipeline import install_host
from ayon_mocha.api import MochaProHost

install_host(MochaProHost())
