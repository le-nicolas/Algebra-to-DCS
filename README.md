# Algebra-to-DCS
Monitoring and controlling water levels in tanks often draws on fundamental algebra and concepts from fluid dynamics. The "water exit flow problem" typically involves balancing inflow and outflow rates to achieve or maintain a desired water level, and it forms the mathematical backbone of many control systems.

CORE PROBLEM:
Tank Dynamics: dL/dt = Qin - Qout
where:
      L = water level(height of liquid in the tank)
      Qin = inflow rate(liters/second)
      Qout = Outflow rate(liters/second)

in many industrial scenarios, Qin and Qout are controlled or measured to stabilize L within desired thresholds.
![Alg](https://github.com/user-attachments/assets/5c99c50d-69b5-48df-88e3-2d8b9429fe95)


#Connection to DCS:
To appreciate this, we almost always tend to start with a problem


PROBLEM:
Monitor and control a multi-tank system where tanks are distributed across a plant, each with its own controller. each controller maintains the tank's water level between defined thresholds.
>Distributed controllers: each tank has its own logic for level control
>central monitoring: central server collects data from controllers and displays system-wide status
>interactions: Users can adjust thresholds and simulate disturbances(e.g. water inflow/outflow)

Basic code will be:
Tank logic
>import socket
import threading
import random
import time

def tank_controller(tank_id, host, port, min_level=30, max_level=70):
    level = random.randint(min_level, max_level)  # Initial water level
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))

    while True:
        # Simulate inflow/outflow
        level += random.randint(-5, 5)
        level = max(0, min(100, level))  # Keep level between 0 and 100
        
        # Control logic: maintain within thresholds
        if level < min_level:
            level += 10  # Simulate adding water
        elif level > max_level:
            level -= 10  # Simulate draining water

        # Send status to central server
        sock.sendall(f"TANK-{tank_id}: Level={level}".encode())
        time.sleep(2)  # Update interval

and for the central monitoring server
>def monitoring_server(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen(5)
    print("Monitoring server started. Awaiting controllers...")
    
    def handle_connection(conn, addr):
        print(f"Connected to {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            print(data.decode())  # Display tank status
            
    while True:
        conn, addr = sock.accept()
        threading.Thread(target=handle_connection, args=(conn, addr)).start()



