#!/usr/bin/env python3
"""Backward-compatible wrapper for the Berth-1-Conflict CLI.

Prefer: python -m os_cmasp.berth1_conflict
"""
from os_cmasp.berth1_conflict import main

if __name__ == "__main__":
    main()
