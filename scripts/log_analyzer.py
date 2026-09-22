#!/usr/bin/env python3
"""Summarize common fields from an Apache/Nginx combined access log."""
import argparse
import collections
import re

LOG_PATTERN = re.compile(r'^(\S+) \S+ \S+ \[[^]]+\] "\S+\s+\S+\s+\S+\s+(\d{3})')


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze an access log")
    parser.add_argument("logfile")
    args = parser.parse_args()
    ips = collections.Counter()
    pages = collections.Counter()
    statuses = collections.Counter()
    with open(args.logfile, encoding="utf-8") as log:
        for line in log:
            match = LOG_PATTERN.match(line)
            if not match:
                continue
            ip, status = match.groups()
            ips[ip] += 1
            statuses[status or "unknown"] += 1
            request = re.search(r'"\S+ (\S+)', line)
            if request:
                pages[request.group(1)] += 1
    print(f"Total requests: {sum(ips.values())}")
    print(f"404 errors: {statuses['404']}")
    print("Top requested pages:")
    for page, count in pages.most_common(5):
        print(f"  {count:>5} {page}")
    print("Top client IPs:")
    for ip, count in ips.most_common(5):
        print(f"  {count:>5} {ip}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())