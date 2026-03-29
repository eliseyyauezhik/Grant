import paramiko

host = "147.45.67.249"
user = "root"
password = "ZaC8tUI0fg302"

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(host, username=user, password=password, timeout=10)

stdin, stdout, stderr = client.exec_command('ps aux | grep -i openclaw; pm2 ls; docker ps')
print("Output:")
print(stdout.read().decode())

client.close()
