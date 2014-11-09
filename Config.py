__author__ = 'eason'

import ConfigParser
import time
import datetime


class Config ():
    config = ConfigParser.RawConfigParser()
    config.read('./system.cfg')

    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%dT%H:%M:%S')

    def __init__(self):
        pass

    @staticmethod
    def getconfig(propname):
        try:
            return Config.config.get('Section', propname)
        except Exception:
            Config.config.set('Section', propname, '')
            with open('./system.cfg', 'wb') as configfile:
                Config.config.write(configfile)
            return ''

    @staticmethod
    def getqueryheaders():
        headers = dict()
        # filename = open('./Headers')
        with open('./Headers') as fileheader:
            for line in fileheader:
                if line.startswith('#'):
                    pass
                else:
                    (key, val) = line.replace('\n', '').split(': ')
                    headers[key] = val
        return headers

    @staticmethod
    def writednsstatustofile(strdns, statusdns):
        with open('./results/DNSLIST_ALL_' + Config.st, 'a') as dnsall:
            dnsall.write(strdns)
        if statusdns is False:
            with open('./results/DNSLIST_ERROR_' + Config.st, 'a') as dnserror:
                dnserror.write(strdns)

    @staticmethod
    def readdnserror():
        with open('./results/DNSLIST_ERROR_' + Config.st) as dnserror:
            return '\nHOST|Status|Comment\n' + dnserror.read()