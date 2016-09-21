#!/usr/bin/env python
#coding:utf-8

import os
import time
import hashlib
import copy

from bs4 import BeautifulSoup
import requests

class Rong360():

    def __init__(self):

        self.headers = {'Host':'www.rong360.com',
                        'Cache-Control':'max-age=0',
                        'Upgrade-Insecure-Requests':'1',
                        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36',
                        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                        'Refer':'http://www.rong360.com/licai/',
                        'Accept-Encoding':'gzip, deflate, sdch',
                        'Accept-Language':'zh-CN,zh;q=0.8',
                        }
        self.baseDir = os.path.dirname(__file__)
        #缓存文件件
        self.htmlCacheFolder = os.path.join(self.baseDir,'.cache')
        #错误信息文件
        self.errorInfoPath = os.path.join(self.baseDir,'errorInfo.txt')
        #下载页面数量
        self.downloadPageCount = 0
        self.downloadPageErrorCount = 0
        self.crawlDataCount = 0
        self.crawlDataErrorCount = 0

    def createFolder(self,path):

        if os.path.exists(path):
            return True
        else:
            os.makedirs(path)
            return True

    def getSignName(self,string):

        if string:
            return hashlib.sha1(string).hexdigest()
        else:
            print '请输入需要签名的字符串'

    def downloadPage(self,url,headers):

        r = requests.get(url=url,headers=headers)
        if r.status_code == 200:
            self.downloadPageCount += 1
            return r.content
        else:
            self.downloadPageErrorCount += 1
            return False


    def saveHtmlCache(self,content,name):

        try:
            path = os.path.join(self.htmlCacheFolder,name+'.html')
            with open(path,'w') as f:
                f.write(content)
            return True
        except Exception as e:
            print '保存网页缓存出错!'
            return False

    def loadHtmlCache(self,name):

        try:
            path = os.path.join(self.htmlCacheFolder,name+'.html')
            with open(path,'r') as f:
                return f.read()
        except Exception as e:
            print '加载缓存出错!',e
            return False

    def checkExistHtmlCache(self,name):
        try:
            path = os.path.join(self.htmlCacheFolder,name+'.html')
            return True if os.path.exists(path) else False
        except Exception as e:
            print '检查缓存是否存在时出错!'

    def getListContent(self,url):

        name = self.getSignName(url)
        if not self.checkExistHtmlCache(name):

            content = self.downloadPage(url,self.headers)
            self.saveHtmlCache(content,name)
        else:

            content = self.loadHtmlCache(name)
        return content

    def parseListContent(self,content):

        if content:
            soup = BeautifulSoup(content,'lxml')
            return [{'pt_name':self.cleanBlank(tr.find('a',class_ = "doc-color-link").get_text()),
                     'pt_url':self.cleanBlank(tr.find('a',class_ = "doc-color-link").get('href')),
                     'pt_grade':self.cleanBlank(tr.find('td',class_ = "pingji").get_text()),
                     'pt_average':self.cleanBlank(tr.find('td',class_ = "average").get_text()),
                     'saleDate':self.cleanBlank(tr.find('td',class_ = "five_color").get_text()),
                     'ptBackground':self.cleanBlank(tr.find_all('td',class_="five_color")[1].get_text()),
                     'risk_disk':self.cleanBlank(tr.find('td',class_ = "risk_index").get_text())}
                    for tr in soup.find_all('tr') if tr.get('click-url')]

    def getDetailContent(self,url):

        name = self.getSignName(url)
        if not self.checkExistHtmlCache(name):
            headers = copy.deepcopy(self.headers)
            content = self.downloadPage(url,headers)
            self.saveHtmlCache(content,name)
        else:
            content = self.loadHtmlCache(name)
        return content

    def parseDetailBasic(self,content):

        if content:
            soup = BeautifulSoup(content,'lxml')
            for item in soup.find_all('div',class_="wrap-des wrap-clear"):
                pass
                for p in item.find_all('p'):
                    p.get_text()
            basicData = [p.get_text() for item in soup.find_all('div',class_="wrap-left wrap-clear") \
                    for p in item.find_all('p')][1::2]
            try:
                detailData = {'registeredCapital':self.cleanBlank(basicData[0]),
                              'dateSale':self.cleanBlank(basicData[1]),
                              'area':self.cleanBlank(basicData[2]),
                              'url':self.cleanBlank(basicData[3]),
                              'startMoney':self.cleanBlank(basicData[4]),
                              'managementFee':self.cleanBlank(basicData[5]),
                              'cashTakingFee':self.cleanBlank(basicData[6]),
                              'backGround':self.cleanBlank(basicData[7]),
                              'provisionsOfRisk':self.cleanBlank(basicData[8]),
                              'foundCustodian':self.cleanBlank(basicData[9]),
                              'safeguardWay':self.cleanBlank(basicData[10]),
                              'assignmentOfDebt':self.cleanBlank(basicData[11]),
                              'automaticBidding':self.cleanBlank(basicData[12]),
                              'cashTime':self.cleanBlank(basicData[13]),
                              }
                return detailData
            except Exception as e:
                return False

    def parseDetailPerson(self,content):

        if content:
            soup = BeautifulSoup(content,'lxml')
            data = [p.get_text() for p in \
                    soup.find_all('div',class_="loan-msg-con tab-con")[1].find_all('p')]
            return self.splitList(2,*self.cleanBlankOfList(*data))

    #清理空白元素
    def cleanBlankOfList(self,*args):
        list = []
        for i in args:
            if i:
                list.append(i)
        return list

    #按长度分割成列表
    def splitList(self,length,*args):

        list = []
        list2 = []
        j = 0
        for i in args:
            if j < length:
                list.append(i)
                j += 1
            else:
                list2.append(list)
                list = []
                list.append(i)
                j = 1
        return list2

    #清理字符串空白
    def cleanBlank(self,string):

        return string.replace(' ','').replace('\r','').replace('\n','')



if __name__ == '__main__':

    url = 'http://www.rong360.com/licai-p2p/pingtai/rating'
    test = Rong360()
    test.createFolder(test.htmlCacheFolder)
    content=test.getListContent(url)
    data = test.parseListContent(content)
    list = []
    for item in data:
        content = test.getDetailContent(item['pt_url'])
        time.sleep(2)
        result = test.parseDetailBasic(content)
        if not result:
            print '出错网址%s'%(item['pt_url'])
        else:
            for i in result:
                print result[i],'\n'
            persons = test.parseDetailPerson(content)
            for person in persons:
                if len(person) < 2:
                    print '人员解析出错网址%s'%(item['pt_url'])
                else:
                    print person[0],person[1]






