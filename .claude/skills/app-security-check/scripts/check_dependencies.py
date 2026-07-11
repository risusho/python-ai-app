"""Check this project's requirements files for known vulnerable dependency versions.

Prefers `pip-audit` if it is installed in the active environment; otherwise falls
back to querying the OSV.dev API directly, using the versions actually installed
in the current Python environment (so it reflects what's really running, not just
what the `>=` specifiers in requirements.txt allow).
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
import urllib.request
from importlib import metadata
from pathlib import Path

DEFAULT_REQUIREMENTS = ["requirements.txt", "requirements-dev.txt"]
OSV_BATCH_URL = "https://api.osv.dev/v1/querybatch"
OSV_VULN_URL = "https://api.osv.dev/v1/vulns/{id}"
PACKAGE_NAME_RE = re.compile(r"^([A-Za-z0-9._-]+)")


def parse_requirements(paths: list[Path]) -> list[str]:
    packages = []
    for path in paths:
        if not path.exists():
            continue
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            match = PACKAGE_NAME_RE.match(line)
            if match:
                packages.append(match.group(1))
    return packages


def try_pip_audit(paths: list[Path]) -> str | None:
    args = ["pip-audit"]
    for path in paths:
        if path.exists():
            args += ["-r", str(path)]
    try:
        result = subprocess.run(args, capture_output=True, text=True, timeout=120)
    except FileNotFoundError:
        return None
    if result.returncode not in (0, 1):  # pip-audit exits 1 when vulnerabilities are found
        return None
    return result.stdout + result.stderr


def fetch_vuln_detail(vuln_id: str) -> dict:
    req = urllib.request.Request(OSV_VULN_URL.format(id=vuln_id))
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def query_osv(packages: list[str]) -> dict:
    queries = []
    resolved = []
    for pkg in packages:
        try:
            version = metadata.version(pkg)
        except metadata.PackageNotFoundError:
            continue
        resolved.append((pkg, version))
        queries.append({"version": version, "package": {"name": pkg, "ecosystem": "PyPI"}})

    if not queries:
        return {}

    body = json.dumps({"queries": queries}).encode("utf-8")
    req = urllib.request.Request(OSV_BATCH_URL, data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode("utf-8"))

    findings = {}
    for (pkg, version), result in zip(resolved, data.get("results", [])):
        vulns = result.get("vulns", [])
        if not vulns:
            continue
        # The batch endpoint only returns {id, modified}; fetch full records for the summary/details.
        details = [fetch_vuln_detail(v["id"]) for v in vulns]
        findings[pkg] = {"version": version, "vulns": details}
    return findings


def main() -> None:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    paths = [root / name for name in DEFAULT_REQUIREMENTS]

    audit_output = try_pip_audit(paths)
    if audit_output is not None:
        print("=== pip-audit ===")
        print(audit_output)
        return

    print("pip-audit not available; falling back to OSV.dev lookup for installed versions.\n")
    packages = parse_requirements(paths)
    if not packages:
        print("No requirements files found at:", ", ".join(str(p) for p in paths))
        return

    findings = query_osv(packages)
    if not findings:
        print("No known vulnerabilities found in installed versions of:", ", ".join(packages))
        return

    for pkg, info in findings.items():
        print(f"\n{pkg} {info['version']} - {len(info['vulns'])} known advisory(ies):")
        for vuln in info["vulns"]:
            summary = vuln.get("summary") or (vuln.get("details", "")[:200] + "...")
            print(f"  - {vuln.get('id')}: {summary}")
            for affected in vuln.get("affected", []):
                if affected.get("package", {}).get("name", "").lower() != pkg.lower():
                    continue
                for rng in affected.get("ranges", []):
                    fixed = [e["fixed"] for e in rng.get("events", []) if "fixed" in e]
                    if fixed:
                        print(f"    fixed in: {', '.join(fixed)}")


if __name__ == "__main__":
    main()
