# Security Policy

## Supported Versions

Only the latest stable release receives security fixes.

| Version | Supported          |
| ------- | ------------------ |
| latest  | :white_check_mark: |
| older   | :x:                |

## Reporting a Vulnerability

**Please do not open a public GitHub issue for security vulnerabilities.**

Use GitHub's private [Report a vulnerability](https://github.com/fabiocaccamo/python-benedict/security/advisories/new) feature. You will receive a response within 7 days, and a fix will be released as soon as possible depending on severity.

## Supply Chain Security

- **SBOM** — a Software Bill of Materials in [CycloneDX](https://cyclonedx.org/) format (JSON and XML) is attached to every [release](https://github.com/fabiocaccamo/python-benedict/releases/latest) as `sbom.cyclonedx.json` / `sbom.cyclonedx.xml`.
- **License report** — a full dependency license inventory (`licenses.csv` / `licenses.md`) is also attached to every release.
- **Trusted Publishing** — packages are published to PyPI via [OIDC Trusted Publishing](https://docs.pypi.org/trusted-publishers/), without storing long-lived API tokens.
