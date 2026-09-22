#!/usr/bin/env python3
"""Check an HTTP endpoint and return a CI-friendly status."""
import argparse
import sys
import urllib.error
import urllib.request


def main() -> int:
    parser = argparse.ArgumentParser(description="Check application HTTP health")
    parser.add_argument("url", help="URL to check")
    parser.add_argument("--timeout", type=float, default=10.0)
    parser.add_argument("--expected", type=int, default=200)
    args = parser.parse_args()
    request = urllib.request.Request(args.url, headers={"User-Agent": "wisecow-health-checker/1.0"})
    try:
        with urllib.request.urlopen(request, timeout=args.timeout) as response:
            status = response.status
            print(f"UP: {args.url} returned HTTP {status}")
            return 0 if status == args.expected else 1
    except (urllib.error.URLError, TimeoutError) as error:
        print(f"DOWN: {args.url} is unavailable: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())