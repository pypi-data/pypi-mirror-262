from __future__ import annotations

import asyncio
import binascii
import datetime
import logging
import requests
from random import randrange

from .const import (
    BASE_ENDPOINT,
    BASE_HOSTNAME,
    BASE_URL,
    CMD_LOGIN,
    CMD_LOGOUT,
    CMD_PROFILE,
    CMD_METERPOINTS,
    CMD_INVOICES,
    CMD_PERIOD,
    CMD_OBJECTSETTINGS,
    CMD_TEMPERATURE,
    CLIENT_HEADERS,
    TOKEN_EXPRIATION,
    USER_AGENT_TEMPLATE,
)


class EnergiinfoClient:
    """
    A generic Python API client.
    """
    api_url = {}
    session = ""
    access_token = ""
    status = ""
    error_message = ""
    logged_in = False
    siteid = ""

    def __init__(self, apiurl: str, siteid: str, username: str, password: str, session=None):
         self.api_url = apiurl
         self.session = requests.Session()
         self.siteid = siteid
         self.access_token = self.get_access_token(apiurl, username, password)

    def getStatus(self):
        return self.status
    def getErrorMessage(self):
        return self.error_message

    def getLoginStatus(self):
        return self.logged_in

    def get_access_token(self, apiurl: str, username: str, password: str):
        if self.access_token != "":
            return self.access_token
        login_url = apiurl + "/?access_token=none&cmd={}".format(CMD_LOGIN)
        headers = {
            # ... (your headers for login)
        }
        data = {
            'site': self.siteid,
            'Username': username,
            'Password': password,
            'Captcha': '',
            'type': 'permanent',  # permanent remembers the login
        }

        try:
            response = requests.post(login_url, headers=headers, data=data)
            # Check if the login request was successful (status code 200)
            if response.status_code == 200:
                # Parse the JSON response
                response_data = response.json()
                self.status = response_data.get('status')
                if self.status == 'ERR':
                    self.error_message = response_data.get('error_message')
                    self.logged_in = False
                else:
                    self.logged_in = True
                # Extract and return the access token
                return response_data.get('access_token')
            else:
                self.status = 'ERR'
                self.logged_in = False
                self.error_message = response.json().get('error_message')
                # print(f"Failed to log in. Status code: {response.status_code}")
                return None
        except Exception as e:
            self.status = 'ERR'
            self.error_message = str(e)
            # print(f"An error occurred during login: {e}")
            return None

    def run_command(self, apiurl: str, command: str, headers, data):
        error_message = ''
        commandurl = apiurl + '/?access_token={}&cmd={}'.format(self.access_token, command)

        try:
            response = self.session.post(commandurl, headers=headers, data=data)

            # Check if the login request was successful (status code 200)
            if response.status_code == 200:
                # Parse the JSON response
                self.status = response.json().get('status')
                if self.status == 'ERR':
                    self.error_message = response.json().get('error_message')
                return response.json()
            else:
                self.status = 'ERR'
                self.error_message = response.json().get('error_message')
                # print(f"Failed to execute cmd: {command}. Status code: {response.status_code}")
                return None
        except Exception as e:
            # print(f"An error occurred durin cmd: {command}: {e}")
            self.status = 'ERR'
            self.error_message = str(e)
            return None

    def logout(self):
        if self.logged_in == True:
            response = self.run_command(self.api_url, CMD_LOGOUT, None, None)
        else:
            self.status = 'ERR'
            self.error_message = 'Not logged in'
            return None

        if response['status'] == 'OK':
            # Parse the JSON response
            self.status = response['status']
            if self.status == 'ERR':
                self.error_message = response_data.get('error_message')
                self.logged_in = False
            else:
                self.logged_in = False
        else:
            return None

    def get_metering_points(self) - >list:
        meterpoints = self.run_command(self.api_url, CMD_METERPOINTS, None, None)
        if meterpoints['status'] == 'OK':
            return meterpoints['list']
        else:
            return None

    def get_invoices(self, period):
        data_params = {
            'period': period,
        }
        invoicedata = self.run_command(self.api_url, CMD_INVOICES, None, data_params)
        if invoicedata['status'] == 'OK':
            return invoicedata['list']
        else:
            return None

    def get_interruptions(self, ):
        data_params = {
            'type': 'avbrottsinfo',
        }
        interruptions = self.run_command(self.api_url, CMD_OBJECTSETTINGS, None, data_params)
        print(interruptions)
        if interruptions['status'] == 'OK':
            return interruptions['value']
        else:
            return None

    def get_period_values(self, meteringpoint_id, period, signal, interval):
        data_params = {
            'meteringpoint_id': meteringpoint_id,
            'period': period,
            'signal': signal,
            'interval': interval,
        }
        perioddata = self.run_command(self.api_url, CMD_PERIOD, None, data_params)
        if perioddata['status'] == 'OK':
            return perioddata['values']
        else:
            return None
