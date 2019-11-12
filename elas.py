# -*- coding: utf-8 -*-
"""
Created on Sun Nov 10 20:11:59 2019

@author: Abner
"""

from elasticsearch import helpers, Elasticsearch
import csv

es = Elasticsearch()

#刪除index
result = es.indices.delete(index='rent591', ignore=[400, 404])

#CSV檔存到index
with open('rent591.csv',encoding='utf-8') as f:
    reader = csv.DictReader(f)
    helpers.bulk(es, reader, index='rent591',doc_type='my-type')

#單一搜尋index
result = es.get(index='rent591', doc_type='my-type', id= 'R8377119')
print(result)
#批量搜尋index
ds1 = {
    'query': {'match': {'name': '吳'}} #查詢欄位name為a的資料
}
result = es.search(index='rent591',body=ds1)
print(result)