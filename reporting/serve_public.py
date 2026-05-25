"""Serve public/ locally with vercel.json-style rewrites (e.g. /email-machine)."""

from __future__ import annotations

import argparse
import sys
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"

# Keep in sync with vercel.json rewrites.
REWRITES: dict[str, str] = {
    "/email-machine": "/email-machine.html",
}


class PublicHandler(SimpleHTTPRequestHandler):
    def do_GET(self) -> None:
        path = self.path.split("?", 1)[0]
        if path in REWRITES:
            suffix = self.path[len(path) :]
            self.path = REWRITES[path] + suffix
        super().do_GET()


def main() -> int:
    parser = argparse.ArgumentParser(description="Serve public/ with local URL rewrites")
    parser.add_argument("--port", type=int, default=3456)
    parser.add_argument("--host", default="127.0.0.1")
    args = parser.parse_args()

    if not PUBLIC.is_dir():
        print(f"Missing {PUBLIC}", file=sys.stderr)
        return 1

    handler = partial(PublicHandler, directory=str(PUBLIC))
    server = ThreadingHTTPServer((args.host, args.port), handler)
    print(f"Serving {PUBLIC} at http://{args.host}:{args.port}/")
    print("Rewrites:", ", ".join(f"{k} -> {v}" for k, v in REWRITES.items()))
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
