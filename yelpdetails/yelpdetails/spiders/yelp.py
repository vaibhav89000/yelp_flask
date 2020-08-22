# -*- coding: utf-8 -*-
import scrapy
import time
from ..items import YelpdetailsItem
# from scrapy.selector import Selector
from scrapy.selector import Selector
from scrapy_selenium import SeleniumRequest
import os
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
import re

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By



class YelpSpider(scrapy.Spider):
    name = 'yelp'

    website = 'Yelp'
    web_link = ""
    webname = ""
    phone = ""
    direction = ""
    NoSponsored = []
    competitor=[]

    find_key = ''
    near_key = ''
    page_key = 0

    def start_requests(self):
        index = 0
        yield SeleniumRequest(
            url="https://www.yelp.com/",
            wait_time=1000,
            screenshot=True,
            callback=self.parse,
            meta={'index': index},
            dont_filter=True
        )

    def parse(self, response):


        driver = response.meta['driver']

        try:
            driver.find_element_by_xpath("//input[@id='find_desc']").clear()
            search_input1 = driver.find_element_by_xpath("//input[@id='find_desc']")
        except:
            index = response.meta['index']
            yield SeleniumRequest(
                url="https://www.yelp.com/",
                wait_time=1000,

                callback=self.parse,
                errback=self.error_yelp,
                meta={'index': index},
                dont_filter=True
            )


        print(os.path.abspath(os.curdir))
        if (os.stat('option.txt').st_size != 0 and os.stat('location.txt').st_size != 0 and os.stat('pages.txt').st_size != 0):
            firstinput = os.path.abspath(os.curdir) + "\option.txt"
            secondinput = os.path.abspath(os.curdir) + "\location.txt"

            thirdinput = os.path.abspath(os.curdir) + "\pages.txt"

            f = open(firstinput, "r")
            find = f.read().splitlines()

            f = open(secondinput, "r")
            near = f.read().splitlines()

            f = open(thirdinput, "r")
            numpages = f.read().splitlines()

            numpages = int(numpages[0])

            length = len(find)
            index = response.meta['index']

            print('\n'*2)
            print(find, near)
            print('\n'*2)

            self.find_key = find[0]
            self.near_key = near[0]
            self.page_key = numpages


            find.pop(0)
            near.pop(0)

            # if (index < length):
            if (len(find) >= 0 and len(near) >= 0):
                search_input1.send_keys(self.find_key)
                # find.pop(0)
                driver.find_element_by_xpath("//input[@id='dropperText_Mast']").clear()
                search_input2 = driver.find_element_by_xpath("//input[@id='dropperText_Mast']")

                search_input2.send_keys(self.near_key)
                # near.pop(0)
                ind = index
                index += 1

                search_button = driver.find_element_by_xpath("//button[@id='header-search-submit']")
                search_button.click()

                with open('option.txt', 'w') as f:
                    f.write('')

                new_find = ''
                for b in find:
                    new_find += b + "\n"

                with open('option.txt', 'a') as f:
                    f.write(str(new_find))


                with open('location.txt', 'w') as f:
                    f.write('')

                new_near = ''
                for b in near:
                    new_near += b + "\n"

                with open('location.txt', 'a') as f:
                    f.write(str(new_near))


                # time.sleep(4)
                print(driver.current_url)
                page = []
                currpage = 0
                duplicate_sponsored = []
                yield SeleniumRequest(
                    url="https://www.google.com/maps",
                    wait_time=1000,
                    screenshot=True,
                    callback=self.google_maps,
                    meta={'page': page, 'index': index,
                          'currpage': currpage, 'duplicate_sponsored': duplicate_sponsored,"yelp_url": driver.current_url},
                    dont_filter=True
                )
            else:
                file = os.path.abspath(os.curdir) + "\issue.txt"
                # file1 = open(file, 'w')
                # file1.writelines(near)
                with open(file, "w") as file1:
                    file1.writelines(self.NoSponsored)


    def google_maps(self,response):
        driver = response.meta['driver']
        self.competitor=[]
        index = response.meta['index']
        # find = response.meta['find']
        # near = response.meta['near']
        # numpages = response.meta['numpages']
        duplicate_sponsored = response.meta['duplicate_sponsored']
        page = response.meta['page']
        currpage = response.meta['currpage']
        yelp_url = response.meta['yelp_url']


        driver.find_element_by_xpath("//*[@id='searchboxinput']").clear()
        search_input1 = driver.find_element_by_xpath("//*[@id='searchboxinput']")

        search_input1.send_keys(self.find_key+" "+self.near_key)

        search_button = driver.find_element_by_xpath('//*[@id="searchbox-searchbutton"]')
        search_button.click()

        time.sleep(7)

        driver = response.meta['driver']
        html = driver.page_source
        response_obj = Selector(text=html)

        details = response_obj.xpath("//*[@id='pane']/div/div[1]/div/div/div[4]/div[1]/div/div[1]/div[1]/div[1]/div[1]/div[2]/h3")

        for idx,detail in enumerate(details):
            name = detail.xpath(".//span/text()").get()
            if(idx>=2 and len(self.competitor)<4):
                self.competitor.append(name)
            if(len(self.competitor)==4):
                break
        print(self.competitor)
        time.sleep(30)

        yield SeleniumRequest(
            url=yelp_url,
            wait_time=1000,
            screenshot=True,
            callback=self.numberofpages,
            meta={'page': page, 'index': index,
                  'currpage': currpage, 'duplicate_sponsored': duplicate_sponsored},
            dont_filter=True
        )


    def numberofpages(self, response):
        driver = response.meta['driver']
        html = driver.page_source
        response_obj = Selector(text=html)
        page = response.meta['page']
        # catg=response.meta['catg']
        # numpages = response.meta['numpages']
        currpage = response.meta['currpage']
        duplicate_sponsored = response.meta['duplicate_sponsored']

        print()
        print('on the next page')
        print('current url', driver.current_url)
        print()

        time.sleep(2)

        details = response_obj.xpath('//*[@id="wrap"]/div[3]/div[2]/div/div[1]/div[1]/div[2]/div[2]/ul/li/div')
        if(len(details)==0):
            details = response_obj.xpath('//div[2]/div[2]/ul/li/div')
        flag = 0
        for i, detail in enumerate(details):

            check = detail.xpath('.//h3/text()').get()
            if (check == None):
                check = 'NA'
            print(i, check)
            if ('Sponsored Result' in check):
                flag = 1
            elif ('All Result' in check):
                flag = 0
            else:
                if (flag == 1):
                    sponsored_web_link = detail.xpath(
                        ".//div/div/div[2]/div[1]/div/div[1]/div/div[1]/div/div/h4/span/a/@href").get()
                    sponsored_web_name = detail.xpath(
                        ".//div/div/div[2]/div[1]/div/div[1]/div/div[1]/div/div/h4/span/a/text()").get()
                    if (sponsored_web_name not in duplicate_sponsored):
                        duplicate_sponsored.append(sponsored_web_name)
                        page.append(f"https://www.yelp.com{sponsored_web_link}")

        # time.sleep(100)

        index = response.meta['index']
        # find = response.meta['find']
        # near = response.meta['near']

        next_page = response_obj.xpath(
            '//a[@class ="lemon--a__373c0__IEZFH link__373c0__1G70M next-link navigation-button__373c0__23BAT link-color--inherit__373c0__3dzpk link-size--inherit__373c0__1VFlE"]/@href').get()

        print(next_page)
        if (next_page and currpage < self.page_key):
            currpage += 1
            yield SeleniumRequest(
                url=f"https://www.yelp.com{next_page}",
                wait_time=1000,
                screenshot=True,
                callback=self.numberofpages,
                errback=self.errback_numberofpages,
                meta={'page': page,
                      'currpage': currpage, 'duplicate_sponsored': duplicate_sponsored},
                dont_filter=True
            )
        else:
            # page.pop(0)
            print()
            print('All pages')
            print(page)
            print('\n'*2)
            if (len(page) != 0):
                a = page[0]
                page.pop(0)
                yield SeleniumRequest(
                    url=a,
                    wait_time=1000,
                    screenshot=True,
                    callback=self.scrapepages,
                    errback=self.errback_scrapepages,
                    meta={'page': page, 'index': index},
                    dont_filter=True
                )
            else:
                print()
                # print('near', near)
                print()
                # file = os.path.abspath(os.curdir) + "\issue.txt"
                # file1 = open(file, 'w')
                # file1.writelines(near)
                self.NoSponsored.append(self.near_key + " \n")
                file = os.path.abspath(os.curdir) + "\issue.txt"

                with open(file, "w") as file1:
                    file1.writelines(self.NoSponsored)
                yield SeleniumRequest(
                    url="https://www.yelp.com/",
                    wait_time=1000,
                    screenshot=True,
                    callback=self.parse,
                    errback=self.error_yelp,
                    meta={'index': index},
                    dont_filter=True
                )

    def scrapepages(self, response):
        Yelpdetails_Item = YelpdetailsItem()
        driver = response.meta['driver']
        html = driver.page_source
        response_obj = Selector(text=html)
        page = response.meta['page']
        # category = response.meta['category']
        index = response.meta['index']
        # find = response.meta['find']
        # near = response.meta['near']
        # catg = response.meta['catg']
        # duplicateurl = response.meta['duplicateurl']

        # if (response.url == 'https://www.google.com/'):
        #     print()
        #     print()
        #     print(self.webname)
        #     # print(category)
        #     print()
        #     print()
        #     self.name=str(self.name)
        #     a=self.name
        #     self.name=a.strip()
        #     if(self.name!=''):
        #         finalemail = response.meta['finalemail']
        #
        #         Yelpdetails_Item['Name'] = self.name
        #         Yelpdetails_Item['website_link'] = self.web_link
        #         Yelpdetails_Item['website_name'] = self.webname
        #         Yelpdetails_Item['phone'] = self.phone
        #         Yelpdetails_Item['Direction'] = self.direction
        #         Yelpdetails_Item['category'] = 'Sponsored Result'
        #         Yelpdetails_Item['find'] = find
        #         Yelpdetails_Item['near'] = near
        #         Yelpdetails_Item['website'] = self.website
        #
        #         Yelpdetails_Item['email'] = "-"
        #
        #         print()
        #         print()
        #         print(len(finalemail))
        #         print(type(finalemail))
        #         print()
        #         print()
        #         if (len(finalemail) == 0):
        #             yield Yelpdetails_Item
        #         else:
        #             if (len(finalemail) < 5):
        #                 length = len(finalemail)
        #             else:
        #                 length = 5
        #             for i in range(0, length):
        #                 Yelpdetails_Item['email'] = finalemail[i]
        #                 yield Yelpdetails_Item
        #
        #     if len(page) != 0:
        #
        #         a = page[0]
        #         page.pop(0)
        #         yield SeleniumRequest(
        #             url=a,
        #             wait_time=1000,
        #             screenshot=True,
        #             callback=self.scrapepages,
        #             errback=self.errback_scrapepages_all,
        #             meta={'page': page, 'index': index, 'find': find, 'near': near},
        #             dont_filter=True
        #         )
        #
        #     else:
        #         yield SeleniumRequest(
        #             url="https://www.yelp.com/",
        #             wait_time=1000,
        #             screenshot=True,
        #             callback=self.parse,
        #             errback=self.error_yelp,
        #             meta={'index': index},
        #             dont_filter=True
        #         )
        #
        # else:

        try:
            name = response_obj.xpath("//h1/text()").get()
        except:
            name = None

        try:
            webname = response_obj.xpath(
                "//section[1 or 2]/div/div[1]/div/div[2]/p[2]/a[contains(text(),'.com')]/text()").get()

        except:
            webname = None

        if (webname != None):
            try:
                web_link = response_obj.xpath(
                    "//section[1 or 2]/div/div[1]/div/div[2]/p[2]/a[contains(text(),'.com')]/@href").get()
            except:
                web_link = None

            try:
                phone = response_obj.xpath(
                    "//section[1 or 2]/div/div/div/div[2]/p[2][contains(text(),'0') or contains(text(),'1') or contains(text(),'2') or contains(text(),'3') or contains(text(),'4') or contains(text(),'5') or contains(text(),'6') or contains(text(),'7') or contains(text(),'8') or contains(text(),'9')]/text()").get()
            except:
                phone = None
            try:
                direction = response_obj.xpath(
                    "//section[1 or 2]/div/div[3 or 2]/div/div[2]/p/a[contains(text(),'Get Directions')]/@href").get()
            except:
                direction = None
        else:
            web_link = None
            try:
                phone = response_obj.xpath(
                    "//section[1 or 2]/div/div/div/div[2]/p[2][contains(text(),'0') or contains(text(),'1') or contains(text(),'2') or contains(text(),'3') or contains(text(),'4') or contains(text(),'5') or contains(text(),'6') or contains(text(),'7') or contains(text(),'8') or contains(text(),'9')]/text()").get()
            except:
                phone = None
            try:
                direction = response_obj.xpath(
                    "//section[1 or 2]/div/div[3 or 2]/div/div[2]/p/a[contains(text(),'Get Directions')]/@href").get()
            except:
                direction = None

        # try:
        #     category = category
        # except:
        #     category = 'All Results'
        print()
        print(name)
        print(direction)
        print(web_link)
        print(webname)
        print(phone)
        # print(category)
        print()
        if (name == None):
            name = "-"

        if (web_link == None):
            web_link = "-"
        else:
            web_link = f"https://www.yelp.com{web_link}"

        if (direction == None):
            direction = "-"
        else:
            direction = f"https://www.yelp.com{direction}"

        if (webname == None):
            webname = "-"

        if (phone == None):
            phone = "-"

        self.name = name
        self.web_link = web_link
        self.webname = webname
        self.phone = phone
        self.direction = direction

        if (web_link != "-"):
            yield SeleniumRequest(
                url=web_link,
                wait_time=1000,
                screenshot=True,
                callback=self.emailtrack,
                errback=self.errback_emailtrack,
                dont_filter=True,
                meta={'page': page, 'index': index}
            )
        else:
            driver = response.meta['driver']
            finalemail = []
            yield SeleniumRequest(
                url = driver.current_url,
                wait_time=1000,
                screenshot=True,
                callback=self.data_save,
                errback=self.error_google,
                dont_filter=True,
                meta={'page': page, 'index': index, 'finalemail': finalemail}
            )

    def emailtrack(self, response):
        driver = response.meta['driver']
        html = driver.page_source
        response_obj = Selector(text=html)
        page = response.meta['page']
        # category = response.meta['category']
        index = response.meta['index']
        # find = response.meta['find']
        # near = response.meta['near']
        # catg = response.meta['catg']
        # duplicateurl = response.meta['duplicateurl']
        links = LxmlLinkExtractor(allow=()).extract_links(response)
        Finallinks = [str(link.url) for link in links]
        linkscheck = []
        for link in Finallinks:
            if (
                    'Contact' in link or 'contact' in link or 'About' in link or 'about' in link  or 'CONTACT' in link or 'ABOUT' in link):
                linkscheck.append(link)

        links=[]
        for link in linkscheck:
            if('facebook' not in link and 'instagram' not in link and 'youtube' not in link and 'twitter' not in link and 'wiki' not in link and 'linkedin' not in link):
                links.append(link)
        links.append(str(response.url))

        if (len(links) > 0):
            l = links[0]
            links.pop(0)
            uniqueemail = set()
            yield SeleniumRequest(
                url=l,
                wait_time=1000,
                screenshot=True,
                callback=self.finalemail,
                errback=self.errback_finalemail,
                dont_filter=True,
                meta={'links': links, 'page': page, 'index': index,
                      'uniqueemail': uniqueemail}
            )
        else:
            finalemail=[]
            driver = response.meta['driver']
            yield SeleniumRequest(
                url = driver.current_url,
                wait_time=1000,
                screenshot=True,
                callback=self.data_save,
                errback=self.error_google,
                dont_filter=True,
                meta={'page': page, 'index': index, 'finalemail': finalemail}
            )

    def finalemail(self, response):
        links = response.meta['links']
        driver = response.meta['driver']
        html = driver.page_source
        response_obj = Selector(text=html)
        page = response.meta['page']
        # category = response.meta['category']
        index = response.meta['index']
        # find = response.meta['find']
        # near = response.meta['near']
        # catg = response.meta['catg']
        # duplicateurl = response.meta['duplicateurl']
        uniqueemail = response.meta['uniqueemail']

        flag = 0
        bad_words = ['facebook', 'instagram', 'youtube', 'twitter', 'wiki']
        for word in bad_words:
            if word in str(response.url):
                # return
                flag = 1
        if (flag != 1):
            html_text = str(response.text)
            mail_list = re.findall('\w+@\w+\.{1}\w+', html_text)
            #
            mail_list = set(mail_list)
            if (len(mail_list) != 0):
                for i in mail_list:
                    mail_list = i
                    if (mail_list not in uniqueemail):
                        uniqueemail.add(mail_list)
                        print('\n'*2)
                        print(uniqueemail)
                        print('\n'*2)
            else:
                pass

        if (len(links) > 0 and len(uniqueemail) < 5):
            print('\n'*2)
            print('hi', len(links))
            print('\n'*2)
            l = links[0]
            links.pop(0)
            yield SeleniumRequest(
                url=l,
                wait_time=1000,
                screenshot=True,
                callback=self.finalemail,
                errback=self.errback_finalemail,
                dont_filter=True,
                meta={'links': links, 'page': page, 'index': index,
                      'uniqueemail': uniqueemail}
            )
        else:
            print('\n'*2)
            print('hello')
            print('\n'*2)
            emails = list(uniqueemail)
            finalemail = []
            discard = ['robert@broofa.com']
            for email in emails:
                if ('.in' in email or '.com' in email or 'info' in email):
                    for dis in discard:
                        if (dis not in email):
                            finalemail.append(email)
            print('\n'*2)
            print('final', finalemail)
            print('\n'*2)

            yield SeleniumRequest(
                url=driver.current_url,
                wait_time=1000,
                screenshot=True,
                callback=self.data_save,
                errback=self.error_google,
                dont_filter=True,
                meta={'page': page, 'index': index, 'finalemail': finalemail}
            )









    def errback_finalemail(self,failure):
        meta=failure.request.meta
        links=meta['links']
        uniqueemail=meta['uniqueemail']
        if (len(links) > 0 and len(uniqueemail) < 5):
            print('\n'*2)
            print('hi i am in errback_finalemail', len(links))
            print('\n'*2)
            l = links[0]
            links.pop(0)
            yield SeleniumRequest(
                url=l,
                wait_time=1000,
                screenshot=True,
                callback=self.finalemail,
                errback=self.errback_finalemail,
                dont_filter=True,
                meta=meta
            )
        else:
            print('\n'*2)
            print('hello i am in errback_finalemail')
            print('\n'*2)
            emails = list(uniqueemail)
            finalemail = []
            meta['finalemail']=finalemail
            discard = ['robert@broofa.com']
            for email in emails:
                if ('.in' in email or '.com' in email or 'info' in email):
                    for dis in discard:
                        if (dis not in email):
                            finalemail.append(email)
            print('\n'*2)
            print('final', finalemail)
            print('\n'*2)
            yield SeleniumRequest(
                url='https://www.google.com/',
                wait_time=1000,
                screenshot=True,
                callback=self.data_save,
                errback=self.error_google,
                dont_filter=True,
                meta=meta
            )




    def errback_emailtrack(self, failure):
        print('\n'*2)
        print('in errback_emailtrack')
        print()
        meta=failure.request.meta
        finalemail = []
        meta['finalemail']=finalemail
        yield SeleniumRequest(
            url='https://www.google.com/',
            wait_time=1000,
            screenshot=True,
            callback=self.data_save,
            errback=self.error_google,
            dont_filter=True,
            meta=meta
        )


    def errback_numberofpages(self,failure):
        meta = failure.request.meta
        page=meta['page']
        # near=meta['near']
        print()
        print('All pages in errback_numberofpages')
        print(page)
        print('\n'*2)
        if (len(page) != 0):
            print()
            print('pages in errback_numberofpages')
            print()
            a = page[0]
            page.pop(0)
            yield SeleniumRequest(
                url=a,
                wait_time=1000,
                screenshot=True,
                callback=self.scrapepages,
                errback=self.errback_scrapepages,
                meta=meta,
                dont_filter=True
            )
        else:
            print()
            print('near errback_numberofpages', self.near_key)
            print()
            # file = os.path.abspath(os.curdir) + "\issue.txt"
            # file1 = open(file, 'w')
            # file1.writelines(near)
            self.NoSponsored.append(self.near_key + " \n")
            file = os.path.abspath(os.curdir) + "\issue.txt"

            with open(file, "w") as file1:
                file1.writelines(self.NoSponsored)
            yield SeleniumRequest(
                url="https://www.yelp.com/",
                wait_time=1000,
                screenshot=True,
                callback=self.parse,
                errback=self.error_yelp,
                meta={'index': meta['index']},
                dont_filter=True
            )


    def errback_scrapepages(self,failure):
        meta = failure.request.meta
        page=meta['page']
        # near=meta['near']
        print('\n'*2)
        print('in errback_scrapepages')
        print()
        if (len(page) != 0):
            print()
            print('page in errback_scrapepages')
            print()
            a = page[0]
            page.pop(0)
            yield SeleniumRequest(
                url=a,
                wait_time=1000,
                screenshot=True,
                callback=self.scrapepages,
                errback=self.errback_scrapepages,
                meta=meta,
                dont_filter=True
            )
        else:
            print()
            print('near in errback_scrapepages', self.near_key)
            print()
            # file = os.path.abspath(os.curdir) + "\issue.txt"
            # file1 = open(file, 'w')
            # file1.writelines(near)
            self.NoSponsored.append(self.near_key + " \n")
            file = os.path.abspath(os.curdir) + "\issue.txt"

            with open(file, "w") as file1:
                file1.writelines(self.NoSponsored)
            yield SeleniumRequest(
                url="https://www.yelp.com/",
                wait_time=1000,
                screenshot=True,
                callback=self.parse,
                errback=self.error_yelp,
                meta={'index': meta['index']},
                dont_filter=True
            )


    def errback_scrapepages_all(self,failure):
        meta = failure.request.meta
        print('\n'*2)
        print('in errback_scrapepages_all')
        print()
        page=meta['page']
        if len(page) != 0:
            print()
            print('near in errback_scrapepages_all')
            print()
            a = page[0]
            page.pop(0)
            yield SeleniumRequest(
                url=a,
                wait_time=1000,
                screenshot=True,
                callback=self.scrapepages,
                errback=self.errback_scrapepages_all,
                meta=meta,
                dont_filter=True
            )

        else:
            print()
            print('parse in errback_scrapepages_all')
            print()
            yield SeleniumRequest(
                url="https://www.yelp.com/",
                wait_time=1000,
                screenshot=True,
                callback=self.parse,
                errback=self.error_yelp,
                meta={'index': meta['index']},
                dont_filter=True
            )

    def error_yelp(self,failure):
        meta = failure.request.meta
        yield SeleniumRequest(
            url="https://www.yelp.com/",
            wait_time=1000,
            screenshot=True,
            callback=self.parse,
            errback=self.error_yelp,
            meta={'index': meta['index']},
            dont_filter=True
        )

    def error_google(self,failure):
        meta = failure.request.meta
        yield SeleniumRequest(
            url='https://www.google.com/',
            wait_time=1000,
            screenshot=True,
            callback=self.data_save,
            errback=self.error_google,
            dont_filter=True,
            meta=meta
        )


    def data_save(self,response):
        Yelpdetails_Item = YelpdetailsItem()
        driver = response.meta['driver']
        html = driver.page_source
        response_obj = Selector(text=html)
        page = response.meta['page']
        # category = response.meta['category']
        index = response.meta['index']
        # find = response.meta['find']
        # near = response.meta['near']
        # catg = response.meta['catg']
        # duplicateurl = response.meta['duplicateurl']


        print('\n'*2)
        print(self.webname)
        # print(category)
        print('\n'*2)
        self.name = str(self.name)
        a = self.name
        self.name = a.strip()
        if (self.name != ''):
            finalemail = response.meta['finalemail']

            Yelpdetails_Item['Name'] = self.name
            Yelpdetails_Item['website_link'] = self.web_link
            Yelpdetails_Item['website_name'] = self.webname
            Yelpdetails_Item['phone'] = self.phone
            Yelpdetails_Item['Direction'] = self.direction
            Yelpdetails_Item['category'] = 'Sponsored Result'
            Yelpdetails_Item['find'] = self.find_key
            Yelpdetails_Item['near'] = self.near_key
            Yelpdetails_Item['website'] = self.website

            Yelpdetails_Item['competitor1'] = '-'
            Yelpdetails_Item['competitor2'] = '-'
            Yelpdetails_Item['competitor3'] = '-'
            Yelpdetails_Item['competitor4'] = '-'

            for idx,map_name in enumerate(self.competitor):
                Yelpdetails_Item['competitor{}'.format(idx+1)] = map_name



            Yelpdetails_Item['email'] = "-"

            print('\n'*2)
            print(len(finalemail))
            print(type(finalemail))
            print('\n'*2)
            if (len(finalemail) == 0):
                yield Yelpdetails_Item
            else:
                if (len(finalemail) < 5):
                    length = len(finalemail)
                else:
                    length = 5
                for i in range(0, length):
                    Yelpdetails_Item['email'] = finalemail[i]
                    yield Yelpdetails_Item

        if len(page) != 0:

            a = page[0]
            page.pop(0)
            yield SeleniumRequest(
                url=a,
                wait_time=1000,
                screenshot=True,
                callback=self.scrapepages,
                errback=self.errback_scrapepages_all,
                meta={'page': page, 'index': index},
                dont_filter=True
            )

        else:
            yield SeleniumRequest(
                url="https://www.yelp.com/",
                wait_time=1000,
                screenshot=True,
                callback=self.parse,
                errback=self.error_yelp,
                meta={'index': index},
                dont_filter=True
            )
