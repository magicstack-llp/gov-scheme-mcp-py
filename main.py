#!/usr/bin/env python3
"""Compatibility wrapper for the old main.py location.

Use 'gov-scheme-mcp' command or 'python -m gov_scheme_mcp' instead.
"""

import warnings
from src.gov_scheme_mcp.main import main

if __name__ == "__main__":
    warnings.warn(
        "Running main.py directly is deprecated. "
        "Use 'gov-scheme-mcp' command or 'python -m gov_scheme_mcp' instead.",
        DeprecationWarning,
        stacklevel=2
    )
    main()