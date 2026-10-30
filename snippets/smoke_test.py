#!/usr/bin/env python3
"""
Universal HTTP Endpoint & Edge-Case Smoke Tester for Cofa-Probe
Usage: python3 /tmp/cofa-kit/snippets/smoke_test.py http://127.0.0.1:3000/api/health
"""
import sys
import time
import urllib.request
import urllib.error
import json

def test_endpoint(url, method="GET", payload=None, expect_status=None):
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    headers = {"Content-Type": "application/json"} if payload is not None else {}
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            status = resp.getcode()
            body = resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        status = e.code
        body = e.read().decode("utf-8", errors="replace")
    except Exception as e:
        print(f"  ❌ [{method} {url}] Connection Failed: {e}")
        return False
    dt = (time.time() - t0) * 1000
    ok = (expect_status is None and 200 <= status < 300) or (status == expect_status)
    mark = "✅" if ok else "⚠️"
    print(f"  {mark} [{method} {url}] -> HTTP {status} ({dt:.1f}ms) | Body: {body[:120]}")
    return ok

if __name__ == "__main__":
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:3000/"
    print(f"=== 🔍 SMOKE TESTING: {base_url} ===")
    test_endpoint(base_url, "GET")
