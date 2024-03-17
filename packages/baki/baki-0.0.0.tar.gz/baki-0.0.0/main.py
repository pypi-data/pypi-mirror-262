#!/usr/bin/env python

import os
import sys

# Add the root directory of your project to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))


from src.baki.app import app

if __name__ == "__main__":
    app()
