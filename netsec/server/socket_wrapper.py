from time import time


class BaseSocketWrapper:
    def __init__(self, sock, log=True):
        self.__socket = sock
        self.is_logging = log

    def __getattr__(self, item):
        if item.endswith("__sock_obj"):
            return self.__sock_obj
        return getattr(self.__socket, item)

    def __repr__(self):
        return repr(self.__socket)

    def __str__(self):
        return str(self.__socket)

    def __eq__(self, other):
        return self.__socket.__eq__(other)

    def __sock_obj(self):
        return self.__socket


class _CloseClient(BaseSocketWrapper):
    __closed = False

    def __init__(self, sock, count_ptr):
        super().__init__(sock)
        self.__cp = count_ptr

    def close(self, *args, **kwargs):
        self.__close()
        return self.__sock_obj().close(*args, **kwargs)

    def detach(self, *args, **kwargs):
        self.__close()
        return self.__sock_obj().detach(*args, **kwargs)

    def __close(self):
        if self.__closed:
            return
        self.__cp.value -= 1
        self.__closed = True


class _Pointer:

    def __init__(self, value=None):
        self.value = value


class ClientLimit(BaseSocketWrapper):
    _count = _Pointer(0)

    def __init__(self, sock, limit):
        super().__init__(sock)
        self.__limit = limit

    def accept(self):
        while True:
            conn = self.__sock_obj().accept()
            self._count.value += 1
            if self._count.value <= self.__limit:
                return _CloseClient(conn[0], self._count), conn[1]
            if self.is_logging:
                print("Maximum number of open connections (%d) reached, refusing new connections" % self.__limit)
            conn[0].close()
            self._count.value -= 1


class SocketBlocker(BaseSocketWrapper):

    def accept(self):
        while True:
            conn = self.__sock_obj().accept()
            if not self.should_block(conn):
                return conn
            if self.is_logging:
                print("Blocked socket: %s:%d" % (conn[1][0], conn[1][1]))
            conn[0].close()

    def should_block(self, conn):
        raise NotImplementedError


class StaticIpBlocker(SocketBlocker):

    def __init__(self, sock, block_set=(), *args, **kwargs):
        super().__init__(sock, *args, **kwargs)
        self.__block_set = block_set

    def should_block(self, conn):
        return conn[1][0] in self.__block_set


class LimiterIpBlocker(SocketBlocker):

    def __init__(self, sock, limit):
        super().__init__(sock)
        self.__queue_dict = {}
        self.__limit_num = limit[0]
        self.__limit_tim = limit[1]

    def should_block(self, conn):
        ip = conn[1][0]
        t = time()
        count = self._count_clear(ip, t)
        if len(count) >= self.__limit_num:
            if self.is_logging:
                print("%s connected %d/%d times in %d seconds" % (ip, len(count), self.__limit_num, self.__limit_tim))
            return True
        else:
            count.append(t)
            return False

    def _count_clear(self, ip, t):
        try:
            q: list = self.__queue_dict[ip]
        except KeyError:
            q = []
            self.__queue_dict[ip] = q
        while len(q) > 0:
            if t - q[0] > self.__limit_tim:
                del q[0]
            else:
                break
        return q
