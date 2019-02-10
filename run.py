#!/usr/bin/env python
from argparse import ArgumentParser

from app import app

if __name__ == "__main__":
    parser = ArgumentParser(
        description="Run a web server to analyze Python applications and report results."
    )
    parser.add_argument(
        "--host", "-H", type=str, default="127.0.0.1", help="The interface to bind to."
    )
    parser.add_argument(
        "--port", "-p", type=int, default=5000, help="The port to bind to."
    )
    parser.add_argument(
        "--debug",
        "-d",
        action="store_true",
        default=False,
        help="Enable the debugger.",
    )
    parser.add_argument(
        "--threaded",
        "-t",
        action="store_true",
        default=False,
        help="Enable multi threading.",
    )
    arguments = parser.parse_args()
    app.run(**vars(arguments))
