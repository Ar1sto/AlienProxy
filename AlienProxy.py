#!/usr/bin/python3
#!/usr/bin/env Python3
#Coding: UTF-8
#Author: Ar1sto (https://github.com/Ar1sto)

# DISCLAIMER:
# The use of this software is at your own risk. 
# The author shall not be held liable for any legal repercussions or damages arising from the use of this software. 
# It is intended to be used for educational purposes only.

# AlienProxy-v1.1.2 (Patched_BETA-VERSION)

import json
import os
import requests
import socks
import logging
from datetime import datetime 
from requests.exceptions import RequestException, ProxyError
from requests.packages.urllib3.exceptions import InsecureRequestWarning as hdf
requests.packages.urllib3.disable_warnings(hdf)

class AlienProxy:
    API_URL = 'https://proxylist.geonode.com/api/proxy-list?limit=100&page=1&sort_by=lastChecked&sort_type=desc'
    PROXY_FILE = 'tmp_proxies.json'
    INDEX_FILE = 'proxy_index.dat'

    def __init__(self):
        self.current_proxy = None
        self.init_api()
        self.c_time = None 
        logging.basicConfig(filename='AlienProxy_error.log', level=logging.ERROR)

    def rotate(self):
        try:
            # Laden des aktuellen Index aus der Index-Datei
            index = self.load_index()

            # Lade die Proxies aus der Proxy-Datei
            with open(self.PROXY_FILE, 'r') as f:
                proxies_data = json.load(f)["data"] # Zugriff auf 'data' Ebene 
                
            # Prüfung, ob Proxies vorhanden sind
            if not proxies_data:
                print("Keine Proxies gefunden.")
                return None, None, None

            # Wähle den nächsten Proxy aus der Liste aus
            if index < len(proxies_data):
                proxy_info = proxies_data[index]
                ip = proxy_info.get('ip')
                port = proxy_info.get('port')
                protocols = proxy_info.get('protocols') # Socks4/5

                # Speichern des aktuellen Proxys
                self.current_proxy = (f"{ip}:{port}")

                # Speichere den nächsten Index in der Index-Datei
                next_index = (index + 1) % len(proxies_data)
                self.save_index(next_index)

                print(f"\nWechsel zu Proxy [{ip}:{port}] mit Protokoll {protocols} für diesen Request.")
                return ip, port, protocols

            else:
                print("\nKeine weiteren Proxies verfügbar.")
                self.init_api()  # Aktualisiere die Proxy-Liste
                return self.rotate()  # Versuche erneut, einen Proxy zu rotieren

        except Exception as e:
            print(f"\nFehler beim Rotieren des Proxies: {e}")
            self.c_time = datetime.now()
            logging.error(f"[{self.c_time}] Error occurred: {e}", exc_info=True)
            return None, None, None

    def load_index(self):
        try:
            with open(self.INDEX_FILE, 'r') as f:
                index_str = f.read().strip() 
                if index_str:
                    index = int(index_str)
                else:
                    # Standardindexwert setzen, falls die Datei leer ist
                    index = 0
        except FileNotFoundError:
            index = 0
            self.c_time = datetime.now()
            logging.error(f"[{self.c_time}] Error occurred: {e}", exc_info=True)
        except ValueError:
            index = 0
            self.c_time = datetime.now()
            logging.error(f"[{self.c_time}] Error occurred: {e}", exc_info=True)
        return index

    def save_index(self, index):
        with open(self.INDEX_FILE, 'w') as f:
            f.write(str(index))

    def request(self, url, method='get', headers=None, data=None, **kwargs):
        proxy, protocol = self.get_and_test_proxy()
        if proxy and protocol:
            try:
                response = self.make_request_with_proxy(url, proxy, protocol, method=method, headers=headers, data=data, **kwargs)
                return response
            except RequestException as e:
                print(f"Fehler beim Senden des Requests: {e}")
                self.c_time = datetime.now()
                logging.error(f"[{self.c_time}] Error occurred: {e}", exc_info=True)
                return None
        else:
            print("Kein funktionierender Proxy gefunden.")
            return None

    def init_api(self):
        try:
            print("API wird zur Nutzung von AlienProxy initialisiert. Bitte warten...")
            response = requests.get(self.API_URL, timeout=30)
            response.raise_for_status()
            proxies = response.json()

            with open(self.PROXY_FILE, 'w') as f:
                json.dump(proxies, f)

            print("Proxies wurden erfolgreich von der API geladen.")

        except RequestException as e:
            print(f"Fehler beim Laden der Proxies von der API: {e}")
            self.c_time = datetime.now()
            logging.error(f"[{self.c_time}] Error occurred: {e}", exc_info=True)

    def get_and_test_proxy(self):
        try:
            with open(self.PROXY_FILE, 'r') as f:
                proxies_data = json.load(f)

            proxies = proxies_data.get('data', []) # Zugriff auf 'data' Ebene

            for proxy_info in proxies:
                ip = proxy_info.get('ip')
                port = proxy_info.get('port')
                protocols = proxy_info.get('protocols')

                if protocols:
                    protocol = protocols[0]  # Wähle das erste Protokoll in der Liste aus
                    proxy = f"{ip}:{port}"
                    return proxy, protocol
            raise ValueError("Keine Protokolle gefunden.")
            self.c_time = datetime.now()
            logging.error(f"[{self.c_time}] Error occurred: {e}", exc_info=True)

        except FileNotFoundError as e:
            raise FileNotFoundError("Proxy-Datei nicht gefunden. Bitte stelle sicher, dass die Datei vorhanden ist.") from e
            self.c_time = datetime.now()
            logging.error(f"[{self.c_time}] Error occurred: {e}", exc_info=True)
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError("Fehler beim Lesen der Proxy-Datei. Bitte überprüfe das Dateiformat.", doc="") from e
            self.c_time = datetime.now()
            logging.error(f"[{self.c_time}] Error occurred: {e}", exc_info=True)
        except Exception as e:
            raise Exception(f"Unerwarteter Fehler beim Laden und Testen der Proxies: {e}") from e
            self.c_time = datetime.now()
            logging.error(f"[{self.c_time}] Error occurred: {e}", exc_info=True)

    def make_request_with_proxy(self, url, proxy, protocol, method='get', **kwargs):
        if self.current_proxy is None:
            self.rotate() # Ist kein Proxy gesetzt wird rotiert

        proxy = self.current_proxy

        #session = requests.Session()
        proxy_url = f"{protocol}://{proxy}"
        proxys = {
            'http': proxy_url,
            'https': proxy_url
        }   
        session = requests.Session()
        session.proxies = proxys
        session.verify = False
        session.stream = True

        try:
            if method == 'get':
                response = session.get(url, timeout=10, **kwargs)
                print(f"->[GET-Request] =-=-= AlienProxy[{proxy_url}] =-=-= Host[{url}]") 
            elif method == 'post':
                print(f"->[POST-Request] =-=-= AlienProxy[{proxy_url}] =-=-= Host[{url}]")
                response = session.post(url, timeout=10, **kwargs)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
                self.c_time = datetime.now()
                logging.error(f"[{self.c_time}] Error occurred: {e}", exc_info=True)
            return response

        except RequestException as e:
            print(f"Proxy-Server: [{proxy_url}] verweigert die Verbindung...")
            self.c_time = datetime.now()
            logging.error(f"[{self.c_time}] Error occurred: {e}", exc_info=True)
            self.rotate()
            return None

        except Exception as e:
            print(f"Fehler beim Senden des Requests über {proxy}: {e}")
            self.c_time = datetime.now()
            logging.error(f"[{self.c_time}] Error occurred: {e}", exc_info=True)
            self.rotate()
            return None
        finally:
            session.close()
