import paramiko

host = "147.45.67.249"
user = "root"
password = "ZaC8tUI0fg302"

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(host, username=user, password=password, timeout=10)

# Check unit
stdin, stdout, stderr = client.exec_command('ps -o unit -p $(pgrep openclaw-gateway)')
print("Unit:")
print(stdout.read().decode())

# Hard kill, but first check supervisor
stdin, stdout, stderr = client.exec_command('systemctl restart openclaw')
err = stderr.read().decode()
if err:
    print("Restart openclaw error:", err)
    stdin, stdout, stderr = client.exec_command('killall openclaw-gateway')

print("Process killed to force restart.")

client.close()
