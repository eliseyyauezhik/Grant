import paramiko
import json

host = "147.45.67.249"
user = "root"
password = "ZaC8tUI0fg302"

try:
    with open('openclaw_vps.json', 'r', encoding='utf-8') as f:
        config = json.load(f)

    # Enable group mode globally
    config['channels']['telegram']['groupPolicy'] = "enabled"

    with open('openclaw_vps_modified.json', 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2)

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host, username=user, password=password, timeout=10)

    # Backup existing
    client.exec_command('cp /root/.openclaw/openclaw.json /root/.openclaw/openclaw.json.bak')

    # Upload new config
    sftp = client.open_sftp()
    sftp.put('openclaw_vps_modified.json', '/root/.openclaw/openclaw.json')
    sftp.close()

    # Restart service
    print("Restarting service...")
    stdin, stdout, stderr = client.exec_command('systemctl restart openclaw-gateway.service')
    status = stdout.channel.recv_exit_status()
    print("Restart exit status:", status)
    
    # Very quick check if it's active
    stdin, stdout, stderr = client.exec_command('systemctl is-active openclaw-gateway.service')
    print("Service status:", stdout.read().decode().strip())
    
finally:
    client.close()
