import MultipartPostHandler, urllib2, urllib, cookielib

class CasJobs:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.loginurl = 'http://casjobs.sdss.org/CasJobs/login.aspx'
        self.importurl = 'http://casjobs.sdss.org/CasJobs/TableImport.aspx'
        cookies = cookielib.CookieJar()
        opener = urllib2.HTTPCookieProcessor(cookies)
        opener = urllib2.build_opener(opener, MultipartPostHandler.MultipartPostHandler)
        urllib2.install_opener(opener)
        self.login()

    def login(self):
        params = urllib.urlencode({'userid': self.username, 'password': self.password})
        response = urllib2.urlopen(self.loginurl, params)
        self.page = response.read()
        print self.page
        response.close()

    def import_table(self, filename, tablename, tableexists=False, format='text'):
        if tableexists:
            tableTypeDD = 1
        else:
            tableTypeDD = 0
        if format == 'text':
            DataType = 0
        elif format == 'votable':
            DataType = 1
        elif format == 'dataset':
            DataType = 2
        params = urllib.urlencode({'tableTypeDD': tableTypeDD, 'NameBox': tablename,
                                   'DataType': DataType, 'importType': 1,
                                   'httpBox': open(filename, 'rb')})
        response = urllib2.urlopen(self.importurl, params)
        self.page = response.read()
        print self.page
        response.close()
