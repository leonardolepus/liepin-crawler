# encoding: utf-8
import itertools

import scrapy
from liepin.items import LiepinItem

class LiepinSpider(scrapy.Spider):
    name = "liepin"
    start_urls = ["http://www.liepin.com/zhaopin/?pubTime=&salary=&searchType=1&clean_condition=&jobKind=&isAnalysis=&init=1&searchField=1&key=%s+&industries=&jobTitles=&dqs=020%%2C350140&compscale=&compkind=" % (keyword, ) for keyword in ['analyst', 'analytics', 'analysis', 'research', 'researcher', 'statistician', 'statistics', 'market', 'marketing', 'knowledge', 'mathematics', 'mathematician', 'scientist', 'data', 'nlp', 'natural language', "数据", "统计", "分析", "研究", "数学", "市场", "建模", "咨询"]]

    def parse(self, response):
        for sel in response.xpath('//ul[@class="sojob-list"]//div[@class="job-info"]//a[@href]'):
            url = sel.xpath('@href').extract()[0]
            yield scrapy.Request(url, self.parse_job_info)
        for sel in response.xpath('//div[@class="pager"]/div[@class="pagerbar"]/a[@href]'):
            if sel.xpath('text()').extract() and sel.xpath('text()').extract()[0] == u'\u4e0b\u4e00\u9875':
                url = sel.xpath('@href').extract()[0]
                yield scrapy.Request(url, self.parse)

    def parse_job_info(self, response):
        url = response.url
        job = response.xpath('//div[@id="job-view-enterprise"]//div[@class="title"]|//div[@id="job-hunter"]//div[@class="title"]')
        title = job.xpath('div[@class="title-info "]/h1/text()').extract()
        title = title[0] if title else None
        ent_name = job.xpath('div[@class="title-info "]/h3/a/text()|div[@class="title-info "]/h3/text()').extract()
        ent_name = ent_name[0] if ent_name else None
        ent_link = job.xpath('div[@class="title-info "]/h3/a/@href').extract()
        ent_link = ent_link[0] if ent_link else None
        comp = job.xpath('div[@class="job-main "]//p[@class="job-main-title"]/text()').extract()
        comp = comp[0].strip() if comp else None
        loc_time = job.xpath('div[@class="job-main "]//p[@class="basic-infor"]/span/text()').extract()
        loc_time = [s.strip() for s in loc_time if s.strip()]
        loc_time = [''.join([s.strip() for s in s.split('\n')]) for s in loc_time]
        if len(loc_time) >= 2:
            loc, time = loc_time[0:2]
        else:
            loc = None
            time = None
        reqs = job.xpath('div[@class="job-main "]//div[@class="resume clearfix"]/span/text()').extract()
        reqs = '\n'.join(reqs)
        #job description is relatively complex
        #it may consist several sections
        #if a section contains a list, it's considered as 'structured info'
        #otherwise it's considered as 'text info'
        #all structured sections are collected, aggregated and put to more_info field of the final item
        #all text sections are put to jd field of the item
        jd_sections = job.xpath('div[@class="job-main main-message "]|div[@class="job-main main-message"]|div[@class="job-main noborder main-message"]')
        text_jd = []
        struct_jd = []
        for sec in jd_sections:
            sec_title = sec.xpath('h3/text()').extract()
            sec_title = sec_title[0] if sec_title else 'Job description'
            sec_body = sec.xpath('div[@class="content content-word"]|div[@class="content"]')
            sec_text = sec_body.xpath('text()').extract()
            sec_text = '\n'.join([s.strip() for s in sec_text])
            sec_keys = sec_body.xpath('ul/li/span/text()').extract()
            sec_values = sec_body.xpath('ul/li/text()').extract()
            if sec_keys:
                info = '\n'.join([k+v for k, v in itertools.izip(sec_keys, sec_values)])
                info = '\n'.join([sec_title, sec_text, info])
                struct_jd.append(info)
            else:
                text_jd.append('\n'.join([sec_title, sec_text]))
        item = LiepinItem()
        item['url'] = url
        item['job_title'] = title
        item['ent_name'] = ent_name
        item['ent_link'] = ent_link
        item['compensation'] = comp
        item['location'] = loc
        item['time'] = time
        item['requirements'] = reqs
        item['jd'] = '\n'.join(text_jd)
        item['more_info'] = '\n'.join(struct_jd)
        yield item
