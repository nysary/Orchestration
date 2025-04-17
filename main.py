import paramiko
import threading

servers = [
    {"host": "1.2.3.4", "user": "root", "password": "pass1"},
    {"host": "1.2.3.5", "user": "root", "password": "pass2"},
]

command = "uptime"

def ssh_run(server):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(server["host"], username=server["user"], password=server["password"])

        stdin, stdout, stderr = ssh.exec_command(command)
        out = stdout.read().decode()
        err = stderr.read().decode()

        print(f"[{server['host']}] ✅")
        print(out.strip())
        if err:
            print("⚠️", err.strip())

        ssh.close()
    except Exception as e:
        print(f"[{server['host']}] ❌ Ошибка: {e}")

threads = []
for s in servers:
    t = threading.Thread(target=ssh_run, args=(s,))
    t.start()
    threads.append(t)

for t in threads:
    t.join()
