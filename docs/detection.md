# Detection Walkthrough — Web Shell / Command Injection

How this lab detects web-shell and command-injection activity, end to end:
attack -> telemetry -> detection -> triage.

## 1. The attack
DVWA's Command Injection (security: Low) runs `ping -c 4 <input>` via PHP.
Injecting `127.0.0.1; id; uname -a` chains attacker commands onto the ping,
executing arbitrary commands as the web server account.
- ATT&CK: T1190 (Exploit Public-Facing Application), T1059 (Command Execution),
  T1505.003 (Web Shell pattern)

## 2. Telemetry captured
auditd rule: `-a always,exit -F arch=b64 -S execve -k proc_exec`

Representative events from the attack:
Key signals:
- `uid=33` -> www-data, the web server service account
- `comm=sh/dash` -> a shell was spawned by a web process
- parent = apache/php -> web server launching a shell (abnormal)
- `subj=docker-default` -> container attribution (AppArmor profile)
- `auid=4294967295` -> no interactive login behind the process

Web layer: Apache access log (`docker logs dvwa`) shows the request to
`/vulnerabilities/exec/` carrying the injected command.

## 3. Detection rules (Sigma)
- `web_user_spawned_shell.yml`   - shell running as www-data
- `webshell_recon_commands.yml`  - id/whoami/uname/hostname as www-data
- `web_service_spawned_shell.yml`- apache/php parent spawning a shell
All validated with `sigma check` (0 errors).

## 4. Sentinel (KQL)
Converted via the ASIM pipeline (`sigma convert -t kusto -p sentinel_asim`):

## 5. ATT&CK mapping
| Technique | ID |
|---|---|
| Exploit Public-Facing Application | T1190 |
| Command and Scripting Interpreter | T1059 |
| Server Software Component: Web Shell | T1505.003 |
| System Owner/User Discovery | T1033 |
| System Information Discovery | T1082 |

## 6. Analyst triage
1. Confirm the process chain - is the parent a web service (apache/php)?
2. Pull web access logs around the event timestamp; find the request URI and
   the injected command.
3. Identify source IP, affected endpoint, and what commands ran.
4. Hunt for follow-on activity: persistence, new files in the web root,
   outbound connections, lateral movement.
5. Contain: isolate the host/container, kill the shell, preserve logs.
6. Remediate: fix the injection flaw, rotate exposed secrets, review web root
   for dropped web shells.

## 7. Limitations
- execve-only telemetry misses file writes, network connections and in-memory
  execution; pair with file and network monitoring.
- Some applications legitimately shell out as www-data - allowlist those.
- A determined attacker can stop auditd or execute in memory; make audit rules
  immutable (`-e 2`) and ship logs off-box.
