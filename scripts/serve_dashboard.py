#!/usr/bin/env python3
"""Build and serve the executive dashboard with the standard library."""

from __future__ import annotations

import argparse
import os
import sys
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from build_dashboard import main as build_dashboard  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8000, help="Local port; default 8000")
    parser.add_argument("--bind", default="127.0.0.1", help="Bind address; default 127.0.0.1")
    args = parser.parse_args()

    build_dashboard()
    os.chdir(ROOT)
    server = ThreadingHTTPServer((args.bind, args.port), SimpleHTTPRequestHandler)
    print(f"Dashboard ready: http://{args.bind}:{args.port}/dashboard/")
    print("Press Ctrl-C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nDashboard server stopped.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
