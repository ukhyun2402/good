import requests
from urllib import parse
import urllib.request
from bs4 import BeautifulSoup
import time
import datetime
import os
import re

class GoodAuction:
    def __init__(self):
        """
        법원 경매 크롤러 클래스
        """
        self.URL = "http://www.courtauction.go.kr/"

    def log(self,action:str ='None', message:str='None',path:str=None):
        _current = datetime.datetime.now()
        _date = _current.strftime("%Y%m%d")
        # _current = datetime.datetime.now().strftime("%Y%m%d-%H:%M:%S")
        # 파일 경로 확인 및 파일경로 수정 필요
        if path is None:
            path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop','logs',_date)
            try:
                file = open(file=os.path.join(path,_date) + '.txt', mode='a+')
            except FileNotFoundError:
                try:
                    if os.path.exists(path) != True:
                        raise OSError
                except OSError:
                    os.makedirs(path)
                finally:
                    file = open(file=os.path.join(path,_date) + '.txt', mode='w+')
            file.write(_current.strftime("%Y%m%d, %H:%M:%S") + '\t' + action + '\t' + message)



    def set_url(self, url:str, param:dict = {}):
        _url = self.URL + url + '?'
        parameter = ''
        for k,y in param.items():
            parameter += (str(k) + '=' + str(y) +'&')
        parameter = parse.urlencode(parameter, encoding='EUC-KR')
        return _url + parameter

    def get_list_of_auction(self):
        # count = 0
        target = 0
        self.list_of_auction = list()
        while 1:
            param = {'targetRow':str(target),'page':'default40','pageSpec':'default40'}
            _url = self.set_url("RetrieveRealEstMulDetailList.laf?jiwonNm=&srnID=PNO102000")
            _html = requests.get(_url)
            soup = BeautifulSoup(_html.text, features='html.parser')
            sp = None

            for sp in soup.findAll('input', {'type':'checkbox','name':'chk'}):
                # count += 1
                self.list_of_auction.append(sp.get('value'))

            break
            # if sp is None:
            #     break
            # else:
            #     target += 40
            #     time.sleep(5)

        self.list_of_auction = set(self.list_of_auction)

        for auction in self.list_of_auction:
            print(auction)

a = GoodAuction()
# a.set_url('hello',{'dasdsa':"gdsdfs", 'dsadsd':"dasdsa"})
a.get_list_of_auction()
