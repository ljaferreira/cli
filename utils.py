import psutil


def get_pid(port):
    connections = psutil.net_connections()
    for con in connections:
        if con.raddr != tuple():
            if con.raddr.port == port:
                return con.pid, con.status
        if con.laddr != tuple():
            if con.laddr.port == port:
                return con.pid, con.status
    return 0, None


def kill_older_process(port: int):
    pid, _ = get_pid(port)
    if pid is None or pid > 0:
        p = psutil.Process(pid)
        p.terminate()
