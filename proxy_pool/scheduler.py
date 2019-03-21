import time
from .getter import crawl_funcs
from .checker import ProxyChecker
from .settings import LOWER_LIMIT
from .proxy import ProxyCrawler, Proxy

class ProxyScheduler(Proxy):

    def get_proxy(self, interval=5):
        while True:
            if self.sql.length < LOWER_LIMIT and self.sql.raw_length < 200:
                for func in crawl_funcs():
                    crawler = ProxyCrawler(func)
                    crawler.run()
            else:
                time.sleep(interval)

    def check_proxy(self, interval=5):
        checker = ProxyChecker()
        while True:
            if self.sql.raw_length != 0:
                count = 10 if self.sql.raw_length > 10 else self.sql.raw_length
                if count == 1:
                    proxy = self.sql.get_raw()
                    checker.check_one(proxy)
                else:
                    checker.check_many(count=count)
            else:
                time.sleep(interval)