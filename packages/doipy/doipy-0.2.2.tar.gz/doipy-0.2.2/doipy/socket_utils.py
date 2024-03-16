from contextlib import contextmanager
import socket
import ssl
import json

from doipy.config import settings


@contextmanager
def create_socket():
    ssl_settings = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ssl_settings.check_hostname = False
    ssl_settings.verify_mode = ssl.CERT_NONE
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        with ssl_settings.wrap_socket(sock) as ssl_sock:
            ssl_sock.connect((settings.ip, settings.port))
            yield ssl_sock


def send_message(message, ssl_sock):
    data = (json.dumps(message) + '\n').encode(encoding='UTF-8', errors='ignore')
    ssl_sock.send(data)
    ssl_sock.send(b'#\n')


def finalize_socket(ssl_sock):
    ssl_sock.send(b'#\n')


def read_response(ssl_sock):
    not_done = True
    reply_return = ''
    byte_size = 1024
    reply = ssl_sock.recv(byte_size)
    while not_done:
        received = ssl_sock.recv(byte_size)
        if received == b'\n#\n':
            # End of json message

            reply_return = reply.decode()
            reply = ssl_sock.recv(byte_size)
            if reply == b'#\n':
                # End of response
                not_done = False
            #else:
                # Next message starts
        else:
            reply += received
    # fixme: currently only the last full reply is returned
    return json.loads(reply_return)
