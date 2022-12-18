#!/usr/bin/env python
# coding: utf-8


import requests
import socket
import maltego_trx.nordvpn


def get_ip(host):
    try:
        response = socket.gethostbyname(host)
        return response
    except Exception as e:
        return None


def version(domain, port):
    try:
        r = '''http://{}:{}/c/version.js'''.format(domain, port)
        res = requests.get(r)
        xtc_panels = {"var ver = '5.3.0';": 'xtc',
                      "var ver = '5.3.1';": 'sc',
                      "var ver = '';": 'nxt',
                      "var ver = 'XUI 1.0';": 'xui'}
        if res.status_code != 200:
            return "status code for version.js isn't 200"
        if res.text in xtc_panels.keys():
            return xtc_panels[res.text]
        else:
            return False
    except Exception as e:
        return False


def get_asn(host_ip):
    r = '''http://ipinfo.io/{}'''.format(host_ip)
    response = requests.get(r)
    return response


def main(host, port):
    panel = version(host, port)
    if not panel:
        return False, False
    if panel == 'xtc':
        return True, panel
    else:
        return False, panel

