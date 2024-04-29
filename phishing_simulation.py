import os
import subprocess

def simulate_phishing_attack():
    print("Simulating a phishing attack scenario...")
    # Path to the ransomware encryption script
    encrypt_script_path = './encrypt.py'

    try:
        print("Victim executes the malicious attachment (simulation)...")
        # Simulate the execution of the encrypt.py script as if it were a payload
        subprocess.run(['python3', encrypt_script_path], check=True)
        print("Encryption script executed successfully. Files are now encrypted.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred during the simulated attack: {e}")

if __name__ == "__main__":
    simulate_phishing_attack()
