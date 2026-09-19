# Threat Model

## Scope

This document covers the repository foundation and establishes constraints for future collectors, APIs, storage, dashboard, and optional AI integrations.

## Assets

System telemetry, configuration, credentials, API access, event history, and the integrity of monitoring results are sensitive assets.

## Primary risks and controls

| Risk | Baseline control |
| --- | --- |
| Excessive collection or privilege | Read-only by default; least privilege; opt-in capabilities |
| Secret disclosure | `.env` ignored; placeholders only; no secrets in issues or logs |
| Telemetry leakage | Local-first design; explicit configuration and provider disclosure |
| Untrusted input or events | Validate, normalize, and preserve provenance before analysis |
| Supply-chain compromise | Minimal dependencies, license review, CI checks, recorded attribution |
| Misleading automation | AI provides explanation and recommendations; user retains sensitive actions |

## Open decisions

Threat modeling must be expanded before each new component is released, including its data flows, trust boundaries, authentication model, retention policy, and abuse cases.
