import requests
import json
import urllib3.util.connection as urllib3_cn
from typing import List
urllib3_cn.HAS_IPV6 = False

class BenchLibrary(object):

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_DOC_FORMAT = 'reST'
    ROBOT_LIBRARY_VERSION = "0.1"

    def __init__(self):
        super().__init__()
        self.ip = "127.0.0.1"
        self.port = 8000
        self.session = requests.Session()
        self.session.keep_alive = True
        self.params = {}        # 通用参数

    def setup_target(self, ip: str, port: int):
        """Setup target server

        Args:
            ip (str): Target server ip
            port (int): Target server port

        Returns:
            dict: {"status": "ok"} or {"status": "error", "message": "error message"}
        """
        self.ip = ip
        self.port = port
        return {"status": "ok"}
    
    def setup_address(self, address:int):
        """Setup address, 这个接口是为了兼容老的接口, 只是设置本地通用请求变量

        Args:
            address (int): 从机地址

        Returns:
            dict: {"status": "ok"}
        """
        self.params["slave"] = address
        return {"status": "ok"}

    def setup(self, port="/dev/ttyS0", baudrate=9600, timeout=0.1, channel=32, address=1,device_name:str="DAM"):
        """Setup the device

        Args:
            port (str, optional): Serial port. Defaults to "COM5".

        Returns:
            dict: {"status": "ok"} or {"status": "error", "message": "error message"}
        """
        params = {
            "port": port,
            "baudrate": baudrate,
            "timeout": timeout,
            "channel": channel,
            "device_name": device_name
        }
        # params.update(kwargs)
        self.params["slave"] = address
        url = f"http://{self.ip}:{self.port}/io/setup"
        resp = self.session.get(url, params=params)
        return resp.json()

    def open(self, cid: int):
        """Open a channel on an ECU

        Args:
            cid (int): Channel id

        Returns:
            dict: {"status": "ok", "tx": "tx data", "rx": "rx data"}
        """
        params = {
            "cid": cid
        }
        params.update(self.params)
        url = f"http://{self.ip}:{self.port}/io/open"
        resp = self.session.get(url, params=params)
        return resp.json()

    def close(self, cid: int):
        """Close a channel on an ECU

        Args:
            cid (int): Channel id

        Returns:
            dict: {"status": "ok"}
        """
        params = {
            "cid": cid
        }
        params.update(self.params)
        url = f"http://{self.ip}:{self.port}/io/close"
        resp = self.session.get(url, params=params)
        return resp.json()

    def read(self, address: int, num: int):
        """Read holding register data from an ECU

        Args:
            address (int): Address
            num (int): num

        Returns:
            dict: {"status": "ok", "contents": "data"}
        """
        params = {
            "address": address,
            "num": num
        }
        params.update(self.params)
        url = f"http://{self.ip}:{self.port}/io/read"
        resp = self.session.get(url, params=params)
        return resp.json()

    def write(self, address: int, data: int):
        """Write holding register data to an ECU

        Args:
            address (int): Address
            data (int): Data

        Returns:
            dict: {"status": "ok"}
        """
        params = {
            "address": address,
            "data": data
        }
        params.update(self.params)
        url = f"http://{self.ip}:{self.port}/io/write"
        resp = self.session.get(url, params=params)
        return resp.json()

    def read_input(self, address: int, num: int):
        """Read input register data from an ECU

        Args:
            address (int): Address
            num (int): num

        Returns:
            dict: {"status": "ok", "contents": "data"}
        """
        params = {
            "address": address,
            "num": num
        }
        params.update(self.params)
        url = f"http://{self.ip}:{self.port}/io/read/input"
        resp = self.session.get(url, params=params)
        return resp.json()

    def open_all(self):
        """Open all channels on all ECUs

        Returns:
            dict: {"status": "ok"}
        """
        params = {}
        params.update(self.params)
        url = f"http://{self.ip}:{self.port}/io/open/all"
        resp = self.session.get(url, params=params)
        return resp.json()

    def close_all(self):
        """Close all channels on all ECUs

        Returns:
            dict: {"status": "ok"}
        """
        params = {}
        params.update(self.params)
        url = f"http://{self.ip}:{self.port}/io/close/all"
        resp = self.session.get(url, params=params)
        return resp.json()

    def read_all_di(self):
        """Read all DI

        Returns:
            dict: {"status": "ok", "contents": [True, False, ...]}
        """
        params = {}
        params.update(self.params)
        url = f"http://{self.ip}:{self.port}/io/read/all/di"
        resp = self.session.get(url, params=params)
        return resp.json()

    def read_all_do(self):
        """Read all DO

        Returns:
            dict: {"status": "ok", "contents": [True, False, ...]}
        """
        params = {}
        params.update(self.params)
        url = f"http://{self.ip}:{self.port}/io/read/all/do"
        resp = self.session.get(url, params=params)
        return resp.json()
    
    def read_all_do_ext(self, slaves: List[int]):
        """Read all DO extended

        Args:
            slaves (List[int]): Slave list

        Returns:
            dict: {"status": "ok", "contents": [True, False, ...]}
        """
        params = slaves
        url = f"http://{self.ip}:{self.port}/io/read/all/do/ext"
        resp = self.session.post(url, json=params)
        return resp.json()

    def request(self, hexstring: str):
        """Send raw data to the device 

        Args:
            hexstring (str): Request hexstring

        Returns:
            dict: Response data
        """
        params = {
            "data": hexstring
        }
        url = f"http://{self.ip}:{self.port}/io/request"
        resp = self.session.get(url, params=params)
        return resp.json()
    
    def events(self):
        """Receive events from server

        Yields:
            dict: Event data
        """
        url = f"http://{self.ip}:{self.port}/io/events"
        resp = self.session.post(url, stream=True)
        with resp:
            for line in resp.iter_lines():
                if line:
                    line = line.decode('utf-8')
                    if line.startswith("data: "):
                        line = line[6:]
                    yield json.loads(line)