def check_servers(servers):
    offline_servers = []

    for server, status in servers.items():
        if status == "offline":
            offline_servers.append(server)

    return offline_servers


def write_log(offline_servers):
    file = open("server_log.txt", "a")

    for server in offline_servers:
        file.write("ALERT: " + server + " is down\n")

    file.close()


servers = {
    "web": "online",
    "database": "offline",
    "backup": "online"
}


problems = check_servers(servers)

write_log(problems)