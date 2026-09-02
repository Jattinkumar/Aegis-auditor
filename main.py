import socket
import threading
import json
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

VULNERABILITY_DB={
    "vsFTPd 2.3.4":{"CVE":"CVE-2011-2523","Severity":"CRITICAL","Base score":"9.8","Description":"CVE-2011-2523 describes a deliberately introduced backdoor in the software vsftpd 2.3.4 ,"
    " which is activated by certain characters in the username."
    " The threat is critical because it allows attackers to gain immediate root access to the entire system via a hidden network port without a password."},

    "dropbear_0.48":{"CVE":"CVE-2006-1206","Severity":"HIGH","Base score":"5.0","Description":"Allows remote attackers to cause a denial of service (connection slot exhaustion) via a large number of unauthenticated connection attempts."},

    "GNU inetutils 1.9.4":{"CVE":"CVE-2026-24061","Severity":"Critical","Base score":"9.8","Description":"Allows remote attackers to bypass authentication in the telnetd daemon by passing an unsanitized USER environment variable containing command arguments like '-f root'."}
}

file_lock=threading.Lock()
#take base subnet 
base_subnet= input("Enter the subnet eg:- (192.168.1.) : ")

#now we want to get the range 
startingR = int(input("Enter Start Host ID: "))
endingR = int(input("Enter End Host ID: "))

ports=[21, 22, 23, 80, 135, 443, 1025, 1194] # we already have ports
def scan_task(target_ip,port):
     if port==80:
        timeout_limit=2.0
     else:
         timeout_limit=1.0
     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
     s.settimeout(timeout_limit)
     response = s.connect_ex((target_ip,port))
     if response == 0:
        try:
            raw_data=s.recv(1024)
            clean_text=raw_data.decode('utf-8', errors='ignore').strip()
            cve_id= "N/A"
            base_score=0
            severity="LOW/UNKNOWN"
            Exploit_details="No known public exploit signatures found in local defination matrix"
            for signature in VULNERABILITY_DB:
                if signature in clean_text:
                    cve_id = VULNERABILITY_DB[signature]["CVE"]
                    severity=VULNERABILITY_DB[signature]["Severity"]
                    base_score=VULNERABILITY_DB[signature]["Base score"]
                    Exploit_details=VULNERABILITY_DB[signature]["Description"]
                    break
        except socket.timeout:
            clean_text="Service open but timed out (no banner sent natively)"
            print(clean_text)
            
        current_time=datetime.now().strftime("%Y-%m-%d %H:%M%S")
        audit_data={"timestamp":current_time,"target_host":target_ip,"port_door":port,"service-banner":clean_text,"threat_intel":{"cve_id":cve_id,"severity":severity,"base_score":base_score,"Exploit_Details":Exploit_details}}

        with file_lock:
            with open("audit_report.json","a") as file:
                file.write(json.dumps(audit_data)+"\n")
    

with ThreadPoolExecutor(max_workers=100) as executor:

    for host in range(startingR,endingR+1):
        #combining both strings 
        target_ip=base_subnet+str(host)
        print(f"\n[*]  parallel execution payload at: {target_ip}")

        for port in ports:
            executor.submit(scan_task,target_ip,port)
            

 