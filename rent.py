from elasticsearch import helpers, Elasticsearch
import requests



def getData(city='',name='',grnder='',Seller_type='',Types='',situation='',claim='',cellPhone=''): #Seller_type=屋主 仲介 代理人 Types=型態  situation=現況  claim=性別
    es=Elasticsearch()
    url = "http://localhost:5601/api/console/proxy"
    querystring = {"path":"/_sql/translate","method":"POST"}
    
    payload = {"query": "select city , name , grnder , cellPhone , tel , mail , objType , size , Types , situation , claim , price from rent591 "}
    ds1 ="where "  #串出SQL語法
    if city!='':
        if ds1=="where ":
            ds1=ds1+"city='"+city+"' "
    if name!='':
        if ds1=="where ":
            ds1=ds1+"name like '"+name+"%' "
        else:
            ds1=ds1+"and name like '"+name+"%' "
    if grnder!='':
        if '男' in grnder:
            if ds1=="where ":
                ds1=ds1+"grnder = 'M' "
            else:
                ds1=ds1+"and grnder = 'M' "
        if '女' in grnder:
            if ds1=="where ":
                ds1=ds1+"grnder = 'F' "
            else:
                ds1=ds1+"and grnder = 'F' "
    if Seller_type!='':
        if len(Seller_type.split(';'))>1:
            if ds1=="where ":
                ds1=ds1+"(objType ='"+Seller_type.split(';')[0]+"' or objType ='"+Seller_type.split(';')[1]+"' ) "
            else:
                ds1=ds1+"and (objType ='"+Seller_type.split(';')[0]+"' or objType ='"+Seller_type.split(';')[1]+"' ) "
        else:
            if ds1=="where ":
                ds1=ds1+"objType = '"+Seller_type+"' "
            else:
                ds1=ds1+"and objType = '"+Seller_type+"' "
    if Types!='':
        if ds1=="where ":
                ds1=ds1+"Types = '"+Types+"' "
        else:
            ds1=ds1+"and Types = '"+Types+"' "
    if situation!='':
        if ds1=="where ":
            ds1=ds1+"situation = '"+situation+"' "
        else:
            ds1=ds1+"and situation = '"+situation+"' "
    if claim!='':
        if ds1=="where ":
            ds1=ds1+"(claim like '%"+claim+"%' or claim='N' or claim='男女生皆可')"
        else:
            ds1=ds1+"and claim like '%"+claim+"%' "
    if cellPhone!='':
        if ds1=="where ":
            ds1=ds1+"cellPhone = '"+cellPhone+"' "
        else:
            ds1=ds1+"and cellPhone = '"+cellPhone+"' "
    headers = {
        'connection': "keep-alive",
        'accept': "text/plain, */*; q=0.01",
        'origin': "http://localhost:5601",
        'kbn-version': "7.4.2",
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36",
        'dnt': "1",
        'content-type': "application/json",
        'sec-fetch-site': "same-origin",
        'sec-fetch-mode': "cors",
        'referer': "http://localhost:5601/app/kibana",
        'accept-encoding': "gzip, deflate, br",
        'accept-language': "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        'cache-control': "no-cache",
        'postman-token': "ec2cd153-5a65-4682-aef7-45e06a185ba7"
        }
    import json
    
    if ds1=="where ": 
#        print(payload)
        response = requests.request("POST", url, data=json.dumps(payload)  , headers=headers, params=querystring)
    else:
        payload['query']=payload['query']+ds1
        print(payload)
        response = requests.request("POST", url, data=json.dumps(payload)  , headers=headers, params=querystring) #取得Elasticsearch query
    print(response.text)
#
    result = es.search(index='rent591',body=response.text) #取得資料
    
    return result['hits']['hits']

#temp=getData(city='新北市',Seller_type='仲介;代理人',claim='男生')
#getData(city='新北市',Seller_type='仲介;代理人',claim='男生')
#t=getData(city='台北市',name='吳')
    