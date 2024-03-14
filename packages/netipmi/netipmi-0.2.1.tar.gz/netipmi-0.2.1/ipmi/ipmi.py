import abc
from typing import Dict, Any
import atexit
import datetime
import json
import requests
import time
import urllib3
import xml.etree.ElementTree as ET
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class IPMIInterface(abc.ABC):
    def __init__(self, server: str, user: str = "admin", password: str = "admin", proxy: Dict[str, Any] = {}):
        self.is_connected = False

    def get_data(self) -> float:
        return -1


class InvalidInterface(IPMIInterface):
    ...


class IPMI:
    def __init__(self, server: str, user: str = "admin", password: str = "admin", proxy: Dict[str, Any] = {}):
        print("Trying ipmi v1 interface")
        v1 = IPMIV1(server, user, password, proxy)
        if v1.is_connected:
            self.interface: IPMIInterface = v1
            return
        print("Trying ipmi v2 interface")
        v2 = IPMIV2(server, user, password, proxy)
        if v2.is_connected:
            self.interface = v2
            return
        print("Unable to connect on any interface")
        self.interface = InvalidInterface(server, user, password, proxy)

    def login(self) -> bool:
        return self.interface.is_connected

    def get_data(self) -> float:
        return self.interface.get_data()


class IPMIV2(IPMIInterface):
    def __init__(self, server: str, user: str = "admin", password: str = "admin", proxy: Dict[str, Any] = {}):
        self.proxies = proxy
        self.server = server
        self.is_connected = self.login(user, password)
        atexit.register(self.logoff)

    def login(self, user: str, password: str) -> bool:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1788.0',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.5',
            'user': f'"{user}"',
            'password': f'"{password}"',
            'Origin': self.server,
            'Connection': 'keep-alive',
            'Referer': f'{self.server}/restgui/start.html',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'sec-ch-ua-platform': '"Windows"',
            'sec-ch-ua': '"Edge";v="114", "Chromium";v="114", "Not=A?Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
        }
        try:
            response = requests.post(
                f'{self.server}/sysmgmt/2015/bmc/session',
                headers=headers,
                proxies=self.proxies,
                verify=False,
            )
            self.xsrf_token = response.headers["XSRF-TOKEN"]
            self.cookies = response.cookies
            return True
        except requests.exceptions.RequestException as e:
            print(f"Error {e}")
            self.xsrf_token = ""
            self.cookies = requests.cookies.RequestsCookieJar()
            return False

    def get_data(self) -> float:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1788.0',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.5',
            'X-SYSMGMT-OPTIMIZE': 'true',
            'XSRF-TOKEN': self.xsrf_token,
            'Connection': 'keep-alive',
            'Referer': f'{self.server}/restgui/index.html?{self.xsrf_token}',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'sec-ch-ua-platform': '"Windows"',
            'sec-ch-ua': '"Edge";v="114", "Chromium";v="114", "Not=A?Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
        }
        try:
            response = requests.get(f'{self.server}/sysmgmt/2015/server/sensor/power',
                                    cookies=self.cookies, headers=headers, proxies=self.proxies, verify=False)
            data = json.loads(response.text)
            now = data["root"]["powermonitordata"]["presentReading"]["reading"][0]["reading"]
            return float(now)
        except requests.exceptions.RequestException as e:
            print(f"Error {e}")
            return -1

    def logoff(self) -> bool:
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': f'{self.server}/restgui/index.html?{self.xsrf_token}',
            'XSRF-TOKEN': self.xsrf_token,
        }
        try:
            response = requests.delete(f'{self.server}/sysmgmt/2015/bmc/session',
                                       headers=headers, cookies=self.cookies, proxies=self.proxies, verify=False)
            print("Logging off")
            return response.status_code == 200
        except requests.exceptions.RequestException as e:
            print("Logging off failed")
            return False


class IPMIV1(IPMIInterface):
    def __init__(self, server: str, user: str = "admin", password: str = "admin", proxy: Dict[str, Any] = {}):
        self.server = server
        self.formSource = {
            "Get_PSInfoReadings.XML": "(0,0)", "time_stamp": 0, "_": ""}
        self.subpages = ["servh_psinfo", "monitor_pw_comsumption"]
        self.cookies = {"langSetFlag": "0", "language": "English", "SID": "",
                        "mainpage": "health", "subpage": self.subpages[1]}
        self.proxy = proxy
        self.user = user
        self.password = password
        self.is_connected = self.login()

    def login(self) -> bool:
        try:
            login = requests.post(self.server+"/cgi/login.cgi",
                                  data={"name": self.user,
                                        "pwd": self.password},
                                  proxies=self.proxy)

            if "SID" in login.cookies.get_dict().keys():
                self.cookies["SID"] = login.cookies.get_dict()["SID"]
                self.is_connected = True
            else:
                print("Wrong username or password")
            return True
        except requests.exceptions.RequestException as e:
            print("Connection error", e)
            return False

    def get_data(self) -> float:
        if not self.is_connected:
            print("Not connected")
            return -1
        now = datetime.datetime.now()
        tstamp = time.mktime(now.timetuple())
        self.formSource["time_stamp"] = tstamp
        try:
            rSource = requests.post(self.server+"/cgi/ipmi.cgi", data=self.formSource,
                                    cookies=self.cookies, proxies=self.proxy)
            ipmiS = ET.fromstring(rSource.content)
            total_power = 0.0
            for child in ipmiS:
                for item in child:
                    ps = item.attrib
                    total_power += int(ps["dcOutPower"], 16)
            return total_power
        except requests.exceptions.RequestException as e:
            print("Connection error", e)
            return -1

    @staticmethod
    def to_signed(num: int, signedbitb: int) -> int:
        if signedbitb > 0:
            # positive
            if (num % (0x01 << signedbitb)/(0x01 << (signedbitb-1))) < 1:
                return num % (0x01 << signedbitb-1)
            # negative
            else:
                temp = (num % (0x01 << signedbitb-1)
                        ) ^ ((0x01 << signedbitb-1)-1)
                return (-1-temp)
        else:
            return num
