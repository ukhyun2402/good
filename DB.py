import psycopg2
import psycopg2.errors
import psycopg2.sql

class GoodAuction_ProgressSQL:
    def __init__(self):
        try:
            self.conn = psycopg2.connect(
                host="222.104.180.71",
                database="Auction",
                user="postgres",
                password="hyun@1051..",
                port="10000",
            )
            self.cur = self.conn.cursor()
            # self.init()
        except psycopg2.DatabaseError:
            print("Connection Fail.")
        else:
            print("Connect!")
    
    def insert(self,SQL,params=''):
        try:
            self.cur.execute(SQL,params)
            self.conn.commit()
        except psycopg2.Error:
            return 0
        
    def select(self, SQL, params=''):
        self.cur.execute(SQL, params)
        result = self.cur.fetchall()
        for row in result:
            print(row)
    def update(self,SQL):
        try:
            self.cur.execute(SQL)
            return 1
        except psycopg2.Error:
            return 0

    def init(self):
        self.cur.execute("TRUNCATE TABLE AUCTION_LIST")
        self.conn.commit()

a = GoodAuction_ProgressSQL()
a.select('select * from auction_list')