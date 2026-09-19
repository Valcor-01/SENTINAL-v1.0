# Privacy and Data Handling

SENTINAL may eventually collect local system metrics, process metadata, network metadata, security events, application logs, and configuration information. The present scaffold does not collect telemetry.

## Local telemetry

Future collectors should store only the telemetry necessary for their configured purpose, use least privilege, support retention controls, and document data locations before release.

## Optional external AI/API data

An external AI/API provider receives only data that a configured integration sends to it. Such data is subject to that provider's terms and privacy practices. Do not enable an external integration for sensitive telemetry unless its data handling is acceptable for your environment.
