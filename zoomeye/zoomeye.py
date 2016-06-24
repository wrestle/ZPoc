__author__ = 'MR.SJ'
import json
import certifi
import pycurl
import StringIO
import random
import Queue
import os
class ZoomEye():
    def __init__(self):
        self.API_TOKEN = None
        self.url = 'https://api.zoomeye.org/user/login'
        self.user_name = "r00teer@163.com"
        self.password = "hehe123456"
        self.data = {
            "username": self.user_name,
            "password": self.password
        }
        self.post_data = json.dumps(self.data)
        self.port=''
        self.facets=''
        self.ip_list=[]
        self.ip_queue=Queue.Queue(-1)
    def _login(self):
        try:
            c = pycurl.Curl()
            c.setopt(pycurl.CAINFO, certifi.where())
            c.setopt(pycurl.URL, self.url)
            b = StringIO.StringIO()
            c.setopt(pycurl.USERAGENT, "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322)")
            c.setopt(pycurl.WRITEFUNCTION, b.write)
            c.setopt(pycurl.FOLLOWLOCATION, 1)
            c.setopt(pycurl.MAXREDIRS, 5)
            c.setopt(pycurl.CUSTOMREQUEST, "POST")
            c.setopt(pycurl.POSTFIELDS, self.post_data)
            c.perform()
            if b.getvalue():
                print 'success login'
                self.API_TOKEN = json.loads(b.getvalue())["access_token"]
            else:
                print 'success fail,get null result'
            print self.API_TOKEN
            b.close()
            c.close()
        except pycurl.E_HTTP_POST_ERROR:
            print pycurl.E_HTTP_POST_ERROR
        except Exception as e:
            print 'please check your password or username'
            print e.message
            pass

    def _search(self,port,page,facets):
        print 'get_data'
        url = 'https://api.zoomeye.org/host/search?query="port:{}"&page={}&facets={}'.format(port,page,facets)
        print '_get_url'
        data=self._get_url(url)
        self._parse_json(data)
        self._write_file()


    def _get_url(self, url):
        if self.API_TOKEN == None:
            print 'none token'
            return
        try:
            c = pycurl.Curl()
            c.setopt(pycurl.CAINFO, certifi.where())
            c.setopt(pycurl.URL, url)
            b = StringIO.StringIO()
            c.setopt(pycurl.WRITEFUNCTION, b.write)
            c.setopt(pycurl.USERAGENT, "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322)")
            print 'header'
            c.setopt(pycurl.HTTPHEADER, ['Authorization: JWT %s' % self.API_TOKEN.encode()])
            c.setopt(pycurl.CUSTOMREQUEST, "GET")
            c.setopt(pycurl.FOLLOWLOCATION, 1)
            c.perform()
            result = b.getvalue()

            print 'result'
        except Exception as e:
            print e
            print 'go error'
            pass
        return result

    def _write_file(self):
        strs=''
        for i in self.ip_list:
            ip='{}\n'.format(i)
            strs=strs+ip
        r=random.randrange(1,100000)
        path=os.getcwd()
        file_name='{}\\{}_{}.txt'.format(path,self.facets,r)
        print file_name
        while True:
            if os.path.exists("{}".format(file_name)):
                r=random.randrange(1,100000)
                file_name='{}\\{}_{}.txt'.format(path,self.facets,r)
            else:
                break


        print 'write result 2 file {}'.format(file_name)
        try:
            file=open(r(file_name),'w')
            file.write(strs)
            file.close()
        except IOError:
            print IOError


    def _parse_json(self, jsondata):
        port=self.port
        facets=self.facets
        data=json.loads(jsondata)
        for host in data['matches']:
                result = {}
                if host.has_key('site'):
                    result['site'] = host['site']
                else:
                    if host.has_key('ip'):
                        if port:
                            result['ip'] = "{}:{}" .format(host['ip'], host['portinfo']['port'])
                        else:
                            result['ip'] = host['ip']
                        self.ip_list.append(result['ip'])
                    else:
                        print 'just go wrong'
                if facets:
                    for facet in self.info['facets']:
                        if host.has_key(facet):
                            result[facet] = host[facet]
                        else:
                            for key in host.keys():
                                if isinstance(host[key], dict):
                                    if host[key].has_key(facet):
                                        result[facet] = host[key][facet]
                                        break
                            else:
                                result[facet] = ""

