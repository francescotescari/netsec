from syn_solution import send_syn

import sys


def _help(argv):
    print("Usage  : python %s target_ip target_port [spoof_ip:bool] [src_port:int]\n"
          "Example: python %s 192.168.1.25 8080 true" % (argv[0], argv[0]))
    exit(1)

def _bool_val(arg):
    if arg.isnumeric():
        arg = int(arg)
        return arg != 0
    if arg == "true":
        return True
    if arg == "false":
        return False
    raise ValueError


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Too few arguments")
        _help(sys.argv)
    target_ip = sys.argv[1]
    target_port = sys.argv[2]
    spoof_ip = False
    src_port = None
    if len(sys.argv) > 3:
        val = sys.argv[3].lower()
        try:
            spoof_ip = _bool_val(val)
        except:
            if val == "spoof_ip":
                spoof_ip = True
            else:
                print("Invalid spoof_ip value: %s" % val)
                _help(sys.argv)
    if len(sys.argv) > 4:
        val = sys.argv[4].lower()
        try:
            src_port = int(val)
        except:
            print("Invalid src_port value: %s" % val)
            _help(sys.argv)
    print("Sending a syn packet to %s:%s" % (target_ip, target_port))
    send_syn(target_ip, target_port, spoof_ip, src_port)
    print("Done")
