from pdfminer.high_level import extract_pages
import os.path

file = open('test3.txt','w+',encoding='utf-8')
path = os.path.join('1.감정평가서','000210-20190130102490-1-0000.pdf')
# print(path)
for page_layout in extract_pages(path):
    for element in page_layout:
        file.write(repr(element)+'\n')
