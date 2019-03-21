'''
proxy
'''
from .utils import get_logger
from .db import ProxySql

class Proxy(object):
    '''基类'''

    @property
    def logger(self):
        return get_logger('ProxyPool.%s' % self.__class__.__name__.lower().replace('proxy', ''))

    @property
    def sql(self):
        return ProxySql()


from threading import Thread
class ProxyCrawler(Thread, Proxy):

    def __init__(self, crawl_func, *args, **kwargs):
        self.func = crawl_func
        super().__init__(*args, **kwargs)

    def run(self):
        for proxy in self.func():
            self.logger.debug('Got proxy %s' % proxy)
            self.sql.put(proxy)

    @property
    def logger(self):
        return get_logger('ProxyPool.%s' % self.func.__name__)