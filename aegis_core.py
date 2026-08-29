import socket
target_ip="192.168.56.102"
ports=[21, 22, 23, 80]
for port in ports:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2.0)
    response = s.connect_ex((target_ip,port))
    if response == 0:
        try:
            raw_data=s.recv(1024)
            clean_text=raw_data.decode('utf-8', errors='ignore')
        except socket.timeout:
            clean_text="Service open but timed out (no banner sent natively)"
        print(clean_text)
    

        with open("activity.log", "a") as File:
            File.write(f"Target ip: {target_ip} and server version on port {port}: {clean_text}\n") 
    else:
        print("Port is closed ")
