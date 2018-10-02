# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.conf import settings
from fake_useragent import UserAgent
from freeproxies import FreeProxies
import socket

class RandomProxyIpMiddleware(object):
    """Randomly rotate proxies Ips based on FreeProxies lib"""

    @staticmethod
    def check_connection(proxy, spider, timeout=3):
        """
        """
        protocol, host, port = proxy.replace('//','').split(':')
        spider.logger.debug("PROXY host: {} port: {}".format(host, port))
        try:
            socket.setdefaulttimeout(timeout)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, int(port)))
            return True
        except Exception as ex:
            spider.logger.debug("EXCEPTION: {}".format(ex.message))
            return False

    def process_request(self, request, spider):
        proxy = FreeProxies().random_elite

        while not RandomProxyIpMiddleware.check_connection(proxy, spider):
            spider.logger.debug('PROXY {} NOT VALID. GET ANOTHER!'.format(proxy))
            proxy = FreeProxies().random_elite

        request.meta['proxy'] = proxy

class RandomUserAgentMiddleware(object):
    """Randomly rotate user agents based on Fake_UserAgent lib"""

    def process_request(self, request, spider):
        ua = UserAgent(verify_ssl=False).random
        if ua:
            request.headers.setdefault('User-Agent', ua)