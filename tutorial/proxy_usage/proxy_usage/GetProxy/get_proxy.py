import urllib2
import requests
from proxy_usage.dbHelper.db_helper import DB_Helper

'''
proxy test example
In [73]: proxies = {'http': 'http://360pi:mluhoedrluthoeh@216.155.30.114:60000
    ...: ', 'https': 'http://360pi:mluhoedrluthoeh@216.155.30.114:60000'}

In [74]: response = requests.get('https://www.baidu.com/', proxies=proxies, st
    ...: ream=True)

In [75]: response.raw._connection.sock.socket.getpeername()
Out[75]: ('216.155.30.114', 60000)

In [76]: response.raw._connection.sock.socket.getsockname()
Out[76]: ('192.168.100.101', 54791)
'''


class Singleton(object):
    'Single instance example'
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            orig = super(Singleton, cls)
            cls._instance = orig.__new__(cls, *args, **kwargs)
        return cls._instance


class GetIp(Singleton):
    def __init__(self):
        self.db = DB_Helper()
        self.result = list(
            self.db.return_xici_proxy().ips_collection.find().limit(50)
        )
        print self.result

    def delete_proxy(self, proxy):
        'delete invalid proxy'
        result = self.db.return_xici_proxy().ips_collection.remove(proxy)
        print result
        print 'proxy is deleted: ', proxy

    def ip_validator(self, proxy):
        import ipdb; ipdb.set_trace()
        'validate if a ip is available or not'
        http_url = 'http://www.baidu.com/'
        https_url = 'https://www.alipay.com/'
        proxy_type = proxy.get('TYPE').lower()
        validation_url = http_url if proxy_type == 'http' else https_url
        proxy = '%s:%s'%(proxy.get('IP'), proxy.get('PORT'))
        try:
            request = urllib2.Request(url=validation_url)
            request.set_proxy(proxy, proxy_type)
            response = urllib2.urlopen(request, timeout=30)
        except Exception, e:
            print 'Reuqest Error: ', e
            self.delete_proxy(proxy)
            return False
        else:
            status_code = response.getcode()
            if 300 > status_code >= 200:
                print 'Effective proxy:', proxy
                return True
            else:
                print 'Invalid proxy:', proxy
                self.delete_proxy(proxy)
                return False

    def ip_validator_2(self, proxy):
        import ipdb; ipdb.set_trace()
        'validate if a ip is available or not'
        headers = {
            'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Mobile Safari/537.36'
        }
        http_url = 'http://www.baidu.com/'
        https_url = 'https://www.alipay.com/'
        proxy_type = proxy.get('TYPE').lower()
        validation_url = http_url if proxy_type == 'http' else https_url
        proxy = '%s:%s'%(proxy.get('IP'), proxy.get('PORT'))
        try:
            response = requests.get(
                validation_url,
                proxies = {proxy_type:proxy},
                headers= headers
            )
        except Exception, e:
            print 'Reuqest Error: ', e
            self.delete_proxy(proxy)
            return False
        else:
            status_code = response.status_code
            if 300 > status_code >= 200:
                print 'Effective proxy:', proxy
                return True
            else:
                print 'Invalid proxy:', proxy
                self.delete_proxy(proxy)
                return False