import os
from .util import long2ip, ip2long, port


def generate(config):
    public_ip = config["public_ip"]
    current_ip = config["base_ip"]
    current_port = config["base_port"]

    rinetd_content = generate_rinetd('80', public_ip, current_ip, current_port)
    current_port += 1
    rinetd_content += generate_rinetd('443', public_ip, current_ip, current_port)
    current_port += 1

    for group in list(config["groups"].values()):
        for proxy in group["proxies"]:
            if proxy["dnat"]:
                current_ip = long2ip(ip2long(current_ip) + 1)
                for protocol in proxy["protocols"]:
                    rinetd_content += generate_rinetd(port(protocol), public_ip, current_ip, current_port)
                    current_port += 1
    return rinetd_content


def generate_rinetd(port, public_ip, current_ip, current_port):
    result = current_ip + ' ' + str(port) + ' ' + public_ip + ' ' + str(current_port) + os.linesep
    return result
