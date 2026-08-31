import socket
#take base subnet 
base_subnet= input("Enter the subnet eg:- (192.168.1.) : ")

#now we want to get the range 
startingR = int(input("Enter Start Host ID: "))
endingR = int(input("Enter End Host ID: "))

ports=[21, 22, 23, 80] # we already have ports

for host in range(startingR,endingR+1):
    #combining both strings 
    target_ip=base_subnet+str(host)
    print(f"\n[*] Shifting scan target interface to: {target_ip}")
    
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
        

            with open("activity.log", "w") as File:
                File.write(f"Target ip: {target_ip} and server version on port {port}: {clean_text}\n") 
        else:
            print("Port is closed ")
