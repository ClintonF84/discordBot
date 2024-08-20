import os
import subprocess

def deploy():
    # Pull the latest code from the repository
    subprocess.run(["git", "pull", "origin", "main"], check=True)
    
    # Install/Update required packages
    subprocess.run(["pip", "install", "-r", "requirements.txt"], check=True)
    
    # Restart your Python bot (replace with your process management method)
    # os.system("pkill -f bot.py")  # Stop any running instances
    # subprocess.run(["python3", "bot.py"])  # Restart the bot

if __name__ == "__main__":
    deploy()
