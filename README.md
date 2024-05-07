# AlienProxy

![AlienProxy Logo](assets/logo.png)

AlienProxy ist ein Python-Modul, das entwickelt wurde, um Proxies von einer externen API abzurufen und sie für HTTP- und SOCKS-basierte Anfragen zu verwenden. Dabei vereinfacht AlienProxy das passive und aktive rotieren von Proxie-Server.

## Installation

Installieren Sie notwendige Module mit pip:

```bash
pip install -r requirements.txt
```

## Verwendung

Importieren Sie das Modul in Ihrem Python-Skript:

```python
from AlienProxy import AlienProxy
```

Verwenden Sie dann die `AlienProxy`-Klasse, um Proxies abzurufen und Anfragen durchzuführen:

```python
proxy = AlienProxy()
response = proxy.request(url, method='get', headers=headers, data=data)
```

## Funktionen und Features

- Abrufen von Proxies von einer externen API
- Rotation der Proxies
- Unterstützung von HTTP, HTTPS, SOCKS4 und SOCKS5 Proxies
- Automatisches Handling von HTTP- und SOCKS-Anfragen

## Mitwirkende

- Ar1sto - [GitHub](https://github.com/Ar1sto)
- API - [Geonode](https://proxylist.geonode.com)

## Hinweis

Dieses Modul ist nur zu Bildungszwecken gedacht. Die Verwendung liegt in der Verantwortung des Benutzers.
