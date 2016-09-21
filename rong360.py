#!/usr/bin/env python
#coding:utf-8

import os
import time
import hashlib

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

    def downloadPage(self,url):

        r = requests.get(url=url,headers=self.headers)
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

    def getAbstractContent(self,url):

        name = self.getSignName(url)
        if not self.checkExistHtmlCache(name):

            content = self.downloadPage(url)
            self.saveHtmlCache(content,name)
        else:

            content = self.loadHtmlCache(name)
        return content

if __name__ == '__main__':
    pass
    url = 'http://www.rong360.com/licai-p2p/pingtai/rating'
    test = Rong360()
    test.createFolder(test.htmlCacheFolder)
    content=test.getAbstractContent(url)
    print content






