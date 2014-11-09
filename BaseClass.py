# import urllib2
import urllib
import httplib
import json
import dns.resolver
from Config import Config


class BaseClass():
    def __init__(self):
        self.overallstatus = None
        self.queryresponse = None
        self.data = None
        self.objjson = None

        self.queryhost = Config.getconfig('QUERY_HOST')
        self.queryapp = Config.getconfig('QUERY_app')
        self.protocol = Config.getconfig('QUERY_PROTOCOL')
        self.body = Config.getconfig('QUERY_BODY')
        self.method = Config.getconfig('QUERY_METHOD')
        self.headers = Config.getqueryheaders()
        self.dnsservers = self.getdnsservers()

    def getdnsservers(self):
        dnsservers = list()
        with open('./DNSservers') as f:
            for line in f:
                if line.startswith('#'):
                    pass
                else:
                    dnsservers.append(line.replace('\n', ''))
        return dnsservers


    def callwithhttplib(self):
        url = self.queryhost
        path = self.queryapp
        data = self.querydatabuilder()
        if len(data) > 0:
            path += '?' + data
        if self.protocol.lower() == 'https':
            conn = httplib.HTTPSConnection(url)
        else:
            conn = httplib.HTTPConnection(url)
        conn.request(self.method, path, self.body, self.headers)
        response = conn.getresponse()
        self.data = response.read()
        conn.close()
        self.queryresponse = '\nResponse Code:\n %s %s\nResponse Header:\n %s\nResponse Message:\n %s' % (
        response.status, response.reason, response.getheaders(), self.data)
        return response.status

    def querydatabuilder(self):
        f = Config.getquerydata()
        return urllib.urlencode(f)

    def convertjson(self, strjson):
        try:
            self.objjson = json.loads(strjson)
            return self.objjson
        except Exception:
            pass

    def parsejson(self, json):
        try:
            for item in json:
                hexcid = hex(item['cid'])
                hexappid = hex(item['app_id'])
                hostname = '2-01-%s-%s.cdx.cedexis.net' % (hexcid, hexappid)
                cname = item['cname']
                self.checkdns(hostname, cname)
            return True
        except Exception:
            return False

    def checkdns(self, hostname, cname):
        for item in self.dnsservers:
            dnsserver = item
            actcname = self.getcname(hostname, dnsserver)
            global status
            error = ['No Answer', 'Other Error']
            if actcname == cname:
                if any(x in actcname for x in error):
                    status = False
                else:
                    status = True
            else:
                status = False
            if status is False:
                self.overallstatus = False
            Config.writednsstatustofile(hostname + '|' + str(status) + '|' + actcname + '|' + dnsserver + '\n', status)

    def getcname(self, hostname, dnsserver):
        my_resolver = dns.resolver.Resolver()
        my_resolver.nameservers = [dnsserver]

        try:
            answers = my_resolver.query(hostname, 'CNAME')
            for rdata in answers:
                print rdata.target
                return rdata.target
        except Exception as inst:
            if str(type(inst)) == '<class \'dns.resolver.NoAnswer\'>':
                return 'No Answer'
            else:
                return 'Other Error'

    def isrunwithjsonfile(self):
        # Load sample json as response from Query service
        if Config.getconfig('RUN_WITH_JSON_FILE') == 'yes':
            filename = Config.getconfig('TEST_JSON_FILE')
            f = open(filename)
            self.data = f.read()
