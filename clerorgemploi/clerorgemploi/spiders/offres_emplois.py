# -*- coding: utf-8 -*-
import scrapy
import logging


class OffresEmploisSpider(scrapy.Spider):
    name = 'offres_emplois'
    allowed_domains = ['cler.org']
    start_urls = ['https://www.cler.org/outils/offres-emploi/']

    def parse(self, response):
        titles = response.xpath(
            "//ul[@class='l-postList']/li[@class='l-postList__item']/a")
        for title in titles:
            name = title.xpath(".//article/h1/text()").get()
            link = title.xpath(".//@href").get()
            date_posted = title.xpath(
                ".//article/time/@datetime").get()
            location = title.xpath(
                ".//article/div[@class='c-meta']/span[@class='c-meta__meta'][1]/text()").get()
            department = title.xpath(
                ".//article/div[@class='c-meta']/span[@class='c-meta__meta'][2]/text()").get()
            society_name = title.xpath(
                ".//article/div[@class='c-meta']/span[@class='c-meta__meta'][3]/text()").get()
            contract_type = title.xpath(
                ".//article/div[@class='mgTop--s']/div[@class='c-tag c-tag--off'][1]/text()").get()
            experience_level = title.xpath(
                ".//article/div[@class='mgTop--s']/div[@class='c-tag c-tag--off'][2]/text()").get()

            # yield{
            #     'name': name,
            #     'link': link,
            #     'date_posted': date_posted,
            #     'location': location,
            #     'department': department,
            #     'society_name': society_name,
            #     'contract_type': contract_type,
            #     'experience_level': experience_level
            # }

            yield scrapy.Request(url=link, callback=self.parse_title, meta={'offers_name': name, 'offers_date_posted': date_posted, 'offers_location': location, 'offers_department': department, 'offers_society_name': society_name, 'offers_contract_type': contract_type, 'offers_experience_level': experience_level, 'link': link})

        next_pages = response.xpath("//a[@class='page-numbers']")

        for next_page in next_pages:
            next = next_page.xpath(".//@href").get()

            if next:
                yield response.follow(url=next, callback=self.parse)

    def parse_title(self, response):
        name = response.request.meta['offers_name']
        date_posted = response.request.meta['offers_date_posted']
        location = response.request.meta['offers_location']
        department = response.request.meta['offers_department']
        society_name = response.request.meta['offers_society_name']
        contract_type = response.request.meta['offers_contract_type']
        experience_level = response.request.meta['offers_experience_level']
        link = response.request.meta['link']

        rows = response.xpath(
            "//div[@class='l-row bg-light']/div[@class='l-col l-col--content fc']")
        for row in rows:
            email = row.xpath(".//p/text()").getall()
            apply_before = row.xpath(".//h2/text()").get()

            yield {
                'name': name,
                'date_posted': date_posted,
                'location': location,
                'department': department,
                'society_name': society_name,
                'contract_type': contract_type,
                'experience_level': experience_level,
                # 'Nom': society_name,
                # 'Nom_Alternatif': society_name,
                # 'Ville': location,
                # 'URL': link,
                'Email': email,
                'contact': email,
                'apply_before': apply_before,
                'Link': link
            }

        # next_page = response.xpath(
        #     "//a[@class='page-numbers']/@href").getall()

        # if next_page:
        #     yield response.follow(url=next_page, callable=self.parse_title)
