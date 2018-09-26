# -*- coding: utf-8 -*-
import scrapy
from scrapy.utils.log import configure_logging
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError, TimeoutError, TCPTimedOutError

class ComicsBoxSpider(scrapy.Spider):
    name = "comicsbox"

    #define a start_urls class attribute with a list of URLs
    #is used by the default implementation of start_requests()
    #to create the initial requests for your spider
    start_urls = [
        'http://www.comicsbox.it/albo_ita_editore.php',
    ]

    def errback(self, failure):
        """
        """
        """Handles an error"""
        return {
            'url': err.request.url,
            'status': 'error_downloading_http_response',
            'message': str(err.value),
        }
        # log all failures
        self.logger.error(repr(failure))

        # in case you want to do something special for some errors,
        # you may need the failure's type:

        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)

        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)

    def parse(self, response):
        """
            recursively follow the link to the italian editor pages, extracting data from it
        """
        # follow links to italian editor pages
        for href in response.xpath('//table[@id="lista-table"]//a/@href').extract()[100:]:
            print('href', href, response.urljoin(href))
            yield scrapy.Request(response.urljoin(href), callback=self.parse_editor, errback=self.errback)

    def parse_editor(self, response):
        """
            recursively follow the link to the italian editor pages, extracting data from it
        """
        for href in response.xpath('//table[@id="lista-table"]//span[@class="title2"]/a/@href').extract():
            print('href', href, response.urljoin(href))
            yield scrapy.Request(response.urljoin(href), callback=self.parse_comic, errback=self.errback)

    def parse_comic(self, response):

        editor = response.xpath("descendant-or-self::span[@id = 'data_issue']/text()").extract_first().replace('&nbsp','').split('|')[0].strip()

        elems = response.css('div.alboita_right')
        #print 'elems', len(elems)

        for elem in elems:

            tmp = elem.xpath('text()').extract()
            pages = tmp[0].replace('pagine','').strip()
            date = tmp[-1].strip().replace('(','').replace(')','')

            series = elem.xpath('./strong/a/text()').extract_first()
            div = elem.xpath("descendant-or-self::div[@class = 'alboita_dettagli']")
            text = [t for t in div.xpath('text()').extract() if t.strip()]
            spans = div.xpath('./span/text()').extract()
            tmp = {'script':set(), 'art':set(), 'inks':set()}

            for n, s in enumerate(spans):
                type = text[n+1].replace('/','').replace('(','').replace(')','').strip().lower()
                try:
                    tmp[type].add(s)
                except:
                    continue

            title = div.xpath('./span/strong/text()').extract_first()

            yield {
                'series': series,
                'title': title,
                'script': list(tmp['script']),
                'art': list(tmp['art']),
                'inks': list(tmp['inks']),
                'date' : date,
                'editor' : editor,
                'pages' : pages,
            }