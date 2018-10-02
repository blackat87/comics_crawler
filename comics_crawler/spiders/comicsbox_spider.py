# -*- coding: utf-8 -*-
import scrapy
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError, TimeoutError, TCPTimedOutError

class ComicsBoxSpider(scrapy.Spider):
    name = "comicsbox"

    #define a start_urls class attribute with a list of URLs
    #is used by the default implementation of start_requests()
    #to create the initial requests for your spider
    start_urls = [
        'http://www.comicsbox.it/albo_ita_alpha.php',
        'http://www.comicsbox.it/comicsusa_alpha.php',
        'http://www.comicsbox.it/bandedessinee_alpha.php',
    ]

    def errback(self, failure):
        """
        Handles an error and log it
        """
        # log all failures
        self.logger.error(repr(failure))

        # in case you want to do something special for some errors,
        # you may need the failure's type:

        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            self.logger.error(message='HttpError on {}'.format(response.url))
            print('HttpError on {}'.format(response.url))

        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error(message='DNSLookupError on url {}. \n Message: {}'.format(request.url, str(failure.value)) )

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error(message='TimeoutError on url {}. \n Message: {}'.format(request.url, str(failure.value)))

    def parse(self, response):
        """
        Recursively follow the link to the series
        """
        series_links = response.xpath('//table[@id="lista-table"]//span[@class="title"]/a/@href').extract()
        self.logger.info('SERIES LINK: {}'.format(len(series_links)))
        for href in series_links:
            self.logger.debug('href: {} {}'.format(href, response.urljoin(href)))
            yield scrapy.Request(response.urljoin(href), callback=self.parse_series, errback=self.errback)

    def parse_series(self, response):
        """
        Recursively follow the link to the issues
        """
        issues_links = response.xpath('//table[@id="lista-table"]//span[@class="title2"]/a/@href').extract()
        for href in issues_links:
            yield scrapy.Request(response.urljoin(href), callback=self.parse_comic, errback=self.errback)

    def parse_comic(self, response):
        """
        Get data of the comic
        """
        try:
            editor = response.xpath("//span[@id='editore_issue']/text()").extract()[0].strip()
        except IndexError:
            self.logger.error('EDITOR list empty')
            editor = ''
        try:
            data_issue = response.xpath("//span[@id='data_issue']/text()").extract()[0].strip()
        except IndexError:
            self.logger.error('DATA_ISSUE list empty')
            data_issue = ''

        try:
            series = response.xpath("//div[@id='intestazione']/h1/text()").extract()[0].strip()
        except IndexError:
            self.logger.error('SERIES list empty')
            series = ''

        try:
            elems = response.xpath("//div[@class = 'alboita_right']")
        except IndexError:
            self.logger.error('ELEMS list empty')
            elems = []

        for elem in elems:
            pages = elem.xpath('text()').extract()[0].replace('pagine','').strip()

            tmp = {'scripts':set(), 'arts':set(), 'inks':set(), 'colors':set()}
            div = elem.xpath("descendant-or-self::div[@class='alboita_dettagli']")

            title = div.xpath("span[@class='titolo_storia']/strong/text()").extract()[0].strip()

            roles = [t.replace('/','').replace('(','').replace(')','').strip().lower().strip() for t in div.xpath('text()').extract() if t.strip()][1:]
            authors = div.xpath('a/text()').extract()

            for x, y in zip(authors, roles):
                if y not in tmp:
                    if y == 'color':
                        y = 'colors'
                    elif y == 'ink':
                        y = 'inks'
                    elif y == 'art':
                        y = 'arts'
                    elif y == 'script':
                        y = 'scripts'
                    else:
                        self.logger.debug('NEW ROLE>>> {} editor: {} series: {} title: {}'.format(y, editor, series, title))
                        tmp[y] = set()

                tmp[y].add(x.strip())

            data = {
                'series': series,
                'title': title,
                'date' : data_issue,
                'editor' : editor,
                'pages' : pages,
            }
            for k,v in tmp.items():
                data[k] = list(v)

            self.logger.info('DATA>>> {}'.format(data))

            yield data
