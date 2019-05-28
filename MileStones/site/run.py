from siteCode import app
import socket, subprocess, re


# if __name__ == "__main__":
#    app.run(debug=True, threaded=True ,host='0.0.0.0')
def get_ip():
    ans = subprocess.check_output(['ipconfig'])
    ips = re.findall(r"IPv4 Address.*: ([0-9].*)\r", ans)
    for ip in ips:
        if ip[: 3] == "192":
            return ip

if __name__ == '__main__':
    ip = get_ip()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 0))
    _, port = sock.getsockname()
    sock.close()
    app.run(debug=True, threaded=True,host=ip)
