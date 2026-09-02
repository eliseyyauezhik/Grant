import paramiko
import sys

host = "147.45.67.249"
user = "root"
password = "ZaC8tUI0fg302"

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
    client.connect(host, username=user, password=password, timeout=10)
    stdin, stdout, stderr = client.exec_command('cat /root/.openclaw/openclaw.json')
    config_data = stdout.read().decode('utf-8')
    err = stderr.read().decode('utf-8')
    if err:
        print("Error:", err)
    else:
        print(config_data)
        with open('openclaw_vps.json', 'w', encoding='utf-8') as f:
            f.write(config_data)
finally:
    client.close()
