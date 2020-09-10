import requests
from urllib import parse
import urllib.request
from bs4 import BeautifulSoup
import time
import datetime
import os
import re

# from DB import GoodAuction_ProgressSQL

class GoodAuction_Court_Crawler:
    def __init__(self):
        """[summary]
        굿옥션에서 사용되어지는 Crawler의 기본 클래스입니다.
        """
        self.url = ""
        self.base_url = "http://www.courtauction.go.kr/"
        self.list_url = "https://www.courtauction.go.kr/RetrieveRealEstMulDetailList.laf?jiwonNm=&srnID=PNO102000&page=default40&pageSpec=default40"
        self.list_url_ = ""

        self.detail_total = "RetrieveRealEstCarHvyMachineMulDetailInfo.laf?"
        self.detail_case = "RetrieveRealEstDetailInqSaList.laf?"
        self.detail_document_history = "RetrieveRealEstSaDetailInqMungunSongdalList.laf?"
        self.detail_timeline_history = "RetrieveRealEstSaDetailInqGiilList.laf?"

        self.detail_list = [
            self.detail_total,
            self.detail_document_history,
            self.detail_timeline_history,
            self.detail_case,
        ]

        self.list_of_auction = []
        # self.DB = GoodAuction_ProgressSQL()

    def setURL(self,law_name='',case_number='',maemul_number=1,page=0):
        """
        Parameters
        ----------
        :param law_name str: 법원 이름
        :param case_number str: 사건번호
        :param maemul_number int: 같은 사건번호 내 다른 물건에 부여되는 번호
        :param page int: page 선택\n
        - page=0 : 상세페이지
        - page=1 : 사건 문건/송달내역
        - page=2 : 사건 기일내역
        - page=3 : 사건 경매검색사건 페이지
        """
        self.page = page
        query = [
            ('jiwonNm', law_name),
            ('saNo',case_number),
            ('maemulSer', maemul_number),
            ('_SRCH_SRNID','PNO102014') # ???
        ]
        if page == 0:
            pass
        elif page == 1:
            pass
        elif page == 2:
            pass
        elif page == 3:
            pass
        return self.base_url + self.detail_list[page] + self.url_encode(query=query)

    def url_encode(self,query):
        """
        한글로 전달되는 법원의 이름을 url 인코딩 해주는 함수
        """
        return parse.urlencode(query=query,encoding='EUC-KR')

    def get_list_of_auction(self):
        """
        현재 법원에서 게시중인 모든 사건들의 사건번호를 가져옴\n
        추출되는 정보 형식\n
        법원이름, 사건번호(YYYY013CCCCCCC), 물건번호 # YYYY 연도, CCCCCCC(Lpadding7,0)
        """
        # targetRow
        target = 6000
        # 실 사건 Count
        count = 0
        # 반복문 시작
        while 1:
            self.list_url_ = self.list_url + '&targetRow='+ str(target)
            html = requests.get(self.list_url_)        
            soup = BeautifulSoup(html.text,features='html.parser')
            sp = None
            for sp in soup.findAll('input',{'type':'checkbox','name':'chk'}):
                count+=1
                self.list_of_auction.append(sp.get('value'))
            # 더 이상 레코드가 없으면 Break
            if sp is None:
                break
            target += 40
            # 5초간 쉬기
            time.sleep(5)
            print(str(count)+" Done...( " + str(target) + " )")
        
        # 반복문 종료 후 Tuple로 변환(중복 제거)
        self.list_of_auction = tuple(self.list_of_auction)

        for a in self.list_of_auction:
            if self.DB.insert('INSERT INTO AUCTION_LIST(LAW,AUCTION_ID,MULGEON_NUMBER) VALUES(%s,%s,%s)',a.split(',')) == 0:
                self.log("경매 리스트 크롤링", a + "\tFail")
        self.log("경매 리스트 크롤링","\tDONE")

    def log(self, action, message):
        """
        (Windows OS만 해당)\n
        Log작성을 위한 함수\n
        Desktop\Logs\DateTime\ ____ \n
        디렉토리가 없는 경우 자동으로 생성함
        """
        dt = datetime.datetime.now()
        file_name = "["+ dt.strftime('%Y-%m-%d') + "]" + action + ".txt"
        path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop', 'Logs', dt.strftime('%Y-%m-%d'))
        file_path = os.path.join(path,file_name)
        try:
            file = open(file=file_path, mode="a+")
        except FileNotFoundError:
            try:
                if os.path.exists(path) != True:
                    raise OSError
            except OSError:
                os.makedirs(path)
            finally:
                file = open(file=file_path, mode="w+")

        file.write(dt.strftime("%Y-%m-%d %H:%M:%S") + "\t" + action +"\t"+ message + "\n")
        file.close()
    
    def get_detatil_auction_information(self):
        """
        튜플에 저장되어있는 각 사건에 대해서 상세페이지의 정보를 크롤링해오는 함수\n
        """
        # if(len(self.list_of_auction) == 0):
            # self.get_list_of_auction()
        # for ac in self.list_of_auction:
        _url = self.setURL(
            law_name="서울중앙지방법원",
            case_number="20180130010143",
            # maemul_number=1,
            # law_name=ac[0],
            # case_number=ac[1],
            # maemul_number=ac[2],
        )
        print(_url)
        self.get_gamjung_pdf(_url)

    def get_gamjung_pdf(self,url):
        query_param = url.split('?')[1]
        # Request 요청 Session 생성
        s = requests.Session()
        # Post 메소드로 기본정보 전송
        r = s.post(url="http://www.courtauction.go.kr/RetrieveRealEstSaGamEvalSeo.laf?" + query_param, headers={'user-agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36","Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"},timeout=None)
        # soup으로 파싱
        soup = BeautifulSoup(r.text,features='html.parser')
        # <frame name='mainFrame'> 선택
        frame = soup.find('frame',{'name':'mainFrame'})
        # 위 엘레멘트의 어트리뷰트 겟
        src = frame.get('src')
        # Session의 header를 설정
        r = s.get(url=src,headers={'user-agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36",'referer':"http://www.courtauction.go.kr/RetrieveRealEstSaGamEvalSeo.laf"},timeout=None)
        # 다시한번 soup으로 파싱
        soup = BeautifulSoup(r.text,features='html.parser')
        # <script> 태그 모두 선택
        src = soup.findAll('script')
        for a in src:
            # 대소문자를 구분하지않고 src.~.pdf로 끝나는 문자 선택
            regex = re.compile(r'src.*\.pdf',re.IGNORECASE)
            pdfPath = regex.search(str(a))
            if pdfPath is not None:
                pdfURL = "http://ca.kapanet.or.kr/" + pdfPath.group().replace('src =\'','')
                pdf_r = requests.get(pdfURL)
                print(pdfURL)
                path = os.path.join(os.path.join(os.environ['USERPROFILE']),'Desktop','hello.pdf')
                open(path,'wb').write(pdf_r.content)
    def get_meagack_pdf(self,url):
        pass
if __name__ == "__main__":
    a = GoodAuction_Court_Crawler()
    a.get_detatil_auction_information()

# http://www.courtauction.go.kr/RetrieveRealEstMgakMulMseo.laf?jiwonNm=%BC%AD%BF%EF%C1%DF%BE%D3%C1%F6%B9%E6%B9%FD%BF%F8&saNo=20180130010143&maemulSer=2&hOrvParam=YQN2WHHG1nS29x92QX9H4P1TDEVHwVlx81340CklBsHnklpcr5VlHWWRDU%2FC8DMwwvQvBX5xCfUYYLrtkiA3SiSHCYDZOiGnrUl%2FBkyClFOnBwZTQgKTRNd09wXAkQSNAAkA