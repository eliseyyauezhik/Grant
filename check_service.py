import paramiko

host = "147.45.67.249"
user = "root"
password = "ZaC8tUI0fg302"

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(host, username=user, password=password, timeout=10)

stdin, stdout, stderr = client.exec_command('systemctl list-units --all | grep -i openclaw')
print("Found units:")
print(stdout.read().decode())

client.close()
