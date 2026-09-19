# Security Policy

SENTINAL is defensive security-monitoring software. It should be deployed read-only by default and with the least privilege needed to collect approved telemetry.

## Reporting a vulnerability

Do not post sensitive vulnerability details in public issues. Use the repository's private security-advisory reporting channel when it is enabled. Until then, contact the maintainer through a private channel listed in the repository profile and include affected version, impact, reproduction evidence, and a safe mitigation. Do not include credentials, personal data, or exploit payloads.

## Boundaries

SENTINAL does not authorize scanning, exploitation, persistence, or action against systems without authorization. Review integrations before enabling them, protect secrets in environment-specific stores, and validate any telemetry exported to third parties.
