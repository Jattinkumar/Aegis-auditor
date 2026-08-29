import socket
target_ip="192.168.56.102"
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(2.0)
response = s.connect_ex((target_ip,21))
if response == 0:
    raw_data=s.recv(1024)
    clean_text=raw_data.decode()
    print(clean_text)
    

    with open("activity.log", "w") as File:
        File.write(f"Target ip: {target_ip} and server version on port 21: {clean_text}\n") 
else:
    print("Port is closed ")
