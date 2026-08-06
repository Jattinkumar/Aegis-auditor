# Network Labs & Experiments

This repository is my personal engineering log. Instead of accepting surface-level textbook theories, I use this space to test, analyze, and verify how data actually moves across a network using live diagnostic tools.

### My Learning & Verification Process
1. Read the network layer theory in Kurose's Top-Down Approach.
2. Replicate the protocol behavior live on my own machine.
3. Capture the traffic using Wireshark and Nmap to dissect the raw packets.
4. Document the failures, edge cases, and logical takeaways here.

### Active Experiments Log
* **Lab 1: HTTP vs HTTPS Payload Analysis** (Status: Analyzing plain-text GET/POST requests vs TLS encrypted payloads in Wireshark)
* **Lab 2: Nmap Port State Verifications** (Status: Mapping how different firewalls react to stealth SYN scans vs full TCP connect handshakes)
* **Lab 3: Custom Python Log Parsing Script** (Status: Building a script to automatically flag high-frequency 404/401 errors from log streams)
