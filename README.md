# Aegis-Auditor

A high-speed, parallel network scanning and vulnerability matching utility built from scratch in Python.

## Core Objective
I wanted to understand what happens if a software developer accidentally leaves a back door or an unpatched, vulnerable application service wide open on a server's network hosting interface. I started by testing a single target IP address, and then scaled the logic to sweep whole subnetwork blocks dynamically to capture open interface vulnerabilities in real-time.

## Engineering Problems Faced & Solved

### 1. The Time Bottleneck (From 15 Minutes to 3 Seconds)
* **The Problem:** Scanning a full Class C subnet range sequentially took upwards of 15 to 20 minutes. The script was hitting a hard block because it was forced to wait for a 2-second timeout gate on every single dead or closed port before moving to the next task.
* **The Solution:** I refactored the architecture by removing the internal loops from the main execution line and splitting the connection checks into atomic, single tasks. I passed these to a `ThreadPoolExecutor` layer using a 100-worker concurrency allocation. Now, dead ports are dropped asynchronously, cutting the subnet sweep runtime down to under 5 seconds flat.

### 2. The Trailing Network Noise Error (\r\n Buffer Bypass)
* **The Problem:** When verifying the script against my physical home router infrastructure, the local definition signature matcher completely failed to flag known vulnerabilities. I inspected the raw logs and realized the router socket appended carriage return network characters (`\r\n`) to its protocol banners (e.g., `SSH-2.0-dropbear_0.48\r\n`), which broke the string equality checks.
* **The Solution:** I injected a text sanitization layer using the `.strip()` method directly onto the network stream decoding line. This scrubs away all trailing protocol whitespace before it touches the threat intelligence lookup engine.

### 3. Asynchronous File Corruption Risks (The Writing Race)
* **The Problem:** Launching 100 threads concurrently meant multiple background workers were trying to open, write data to, and close the output log file at the exact same millisecond. This creates a severe file collision risk that causes runtime `IOError` crashes or log scrambling.
* **The Solution:** I initialized a global `threading.Lock()` to act as a thread bouncer. Now, when a worker discovers an active vulnerability, it must grab the exclusion lock and form an orderly single-file line to serialize its data package safely onto the disk drive.

## Output Serialization Data Format
The tool runs silently on closed ports to keep the console clean and outputs threat telemetry directly into a structured JSON Lines file (`audit_report.json`):

```json
{"timestamp": "2026-09-03 00:53:43", "target_host": "10.0.0.1", "port_door": 22, "service_banner": "SSH-2.0-dropbear_0.48", "threat_intel": {"cve_id": "CVE-2006-1206", "severity": "HIGH", "base_score": "5.0", "Exploit_Details": "Allows remote attackers to cause a denial of service via a large number of unauthenticated connection attempts."}}
```

## How to Replicate and Execute
```bash
python basic_practice.py
```
