import threading
from views.Landing import Landing, Api
from services.Listener import Listener
import os

class Launcher:
    def __init__(self):
        user_home = os.path.expanduser("~")
        port = Launcher.available_port()
        api_landing = Api()
        api_landing._port_api = port
        listener = threading.Thread(target=Listener, args=(port, api_landing,))
        listener.start()
        Landing(api_landing, debug=False)
        listener.join()

    @staticmethod
    def available_port():
        """
            :return: Devuelve el puerto disponible.
        """
        import socket
        sock = socket.socket()
        sock.bind(('', 0))
        return sock.getsockname()[1]

if __name__ == '__main__':
    Launcher()
