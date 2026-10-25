# php2shell

> **Authorised testing / lab use only.** Built and run in a self-contained,
> isolated lab (DVWA in Docker, bound to localhost). Never run against systems
> you don't own or have explicit written permission to test.

A web-shell attack **and its detection**, end to end. The offensive tooling is
deliberately minimal and sourced from standard public references — the focus and
the value is the **blue-team side**: capturing the telemetry a web shell
generates and writing portable **Sigma detection rules** for it, compiled to
Microsoft Sentinel KQL.

## What it demonstrates
- A reverse-shell **listener** (Python, standard library)
- A payload **generator** wrapping standard reference web shells
- A live **command-injection attack** against DVWA
- **Telemetry capture** with auditd (process execution)
-
A web server account running a shell is the signal. Sentinel KQL:
```kql
imProcessCreate
| where (TargetProcessName endswith "/sh" or TargetProcessName endswith "/bash"
         or TargetProcessName endswith "/dash") and TargetUsername =~ "www-data"
```

## Structure

## MITRE ATT&CK
| Technique | ID |
|---|---|
| Exploit Public-Facing Application | T1190 |
| Command and Scripting Interpreter | T1059 |
| Server Software Component: Web Shell | T1505.003 |
| System Owner/User Discovery | T1033 |
| System Information Discovery | T1082 |

## Detections
Three Sigma rules in `detections/`, validated with `sigma check` (0 errors) and
convertible to Sentinel, Elastic, Splunk, etc. Full walkthrough in
`docs/detection.md`.

## Disclaimer
For education and authorised testing only. The author is not responsible for
misuse.
