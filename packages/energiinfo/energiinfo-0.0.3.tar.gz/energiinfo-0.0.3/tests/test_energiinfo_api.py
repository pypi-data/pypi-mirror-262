import pytest
from energiinfo.api import EnergiinfoClient


def test_dns_failure():
    apiclient = EnergiinfoClient('https://some.shittyurl.se','13','someone','password')
    assert apiclient.getStatus() == 'ERR'

def test_login_failure():
    apiclient = EnergiinfoClient('https://api4.energiinfo.se','13','someone','password')

    assert apiclient.getStatus() == 'ERR'  and 'Failed to login. Check your credentials and try again' == apiclient.getErrorMessage()

def test_logout_failure():
    apiclient = EnergiinfoClient('https://api4.energiinfo.se','13','someone','password')

    apiclient.logout()
    assert apiclient.getStatus() == 'ERR'  and 'Not logged in' == apiclient.getErrorMessage()