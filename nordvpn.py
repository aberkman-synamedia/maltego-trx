#!/usr/bin/env python
# coding: utf-8


from NordVPN_switcher_master.nordvpn_switch import initialize_VPN, rotate_VPN
import requests


def check_ip_location():
    url = 'http://ipinfo.io/json'
    response = requests.get(url).json()
    return response['country']


def nordvpn():
    ip_location = check_ip_location()
    if ip_location == 'IL':
        initialize = initialize_VPN()
        rotate_VPN(initialize)
    else:
        print('\nyour current country is {} \nOK to run \n'.format(ip_location))






