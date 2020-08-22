# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import sqlite3

class YelpdetailsPipeline(object):

    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.conn = sqlite3.connect("yelpdetails.db")
        self.curr = self.conn.cursor()

    def create_table(self):
        self.curr.execute("""DROP TABLE IF EXISTS detail""")
        self.curr.execute("""create table detail(
        Name text,
        website_link text,
        website_name text,
        phone text,
        Direction text,
        category text,
        find text,
        near text,
        email text,
        website text,
        competitor1 text,
        competitor2 text,
        competitor3 text,
        competitor4 text
        )""")
        # pass

    def process_item(self, item, spider):
        self.store_db(item)
        return item

    def store_db(self,item):
        self.curr.execute("""insert into detail values (?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",(
            item['Name'],
            item['website_link'],
            item['website_name'],
            item['phone'],
            item['Direction'],
            item['category'],
            item['find'],
            item['near'],
            item['email'],
            item['website'],
            item['competitor1'],
            item['competitor2'],
            item['competitor3'],
            item['competitor4']

        ))
        self.conn.commit()

