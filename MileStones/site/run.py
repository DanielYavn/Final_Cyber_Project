from siteCode import app
import subprocess, re


# if __name__ == "__main__":
#    app.run(debug=True, threaded=True ,host='0.0.0.0')
def get_ip():
    ans = subprocess.check_output(['ipconfig'])
    ips = re.findall(r"IPv4 Address.*: ([0-9].*)\r", ans)
    for ip in ips:
        if ip[: 3] == "172":
            return ip

if __name__ == '__main__':
    ip = get_ip()
    app.run(debug=True, threaded=True,host=ip)
