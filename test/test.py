from pdfminer.high_level import extract_pages
from pdfminer.layout import LAParams
from pdfminer.layout import LTText
import os.path

# 0.4 0.4

file = open(r'./test1.txt','w',encoding='utf-8')
# path = os.path.join('1.감정평가서','000210-20190130102490-1-0000.pdf')
for page_layout in extract_pages(r'1.감정평가서\000210-20190130102490-1-0000.pdf',laparams=LAParams(char_margin=1,line_overlap=0.2,line_margin=0.5)):
    for element in page_layout:
        # if isinstance(element, LTText):
        file.write(repr(element)+'\n')

file2 = open(r'./test2.txt','w',encoding='utf-8')
for page_layout in extract_pages(r'1.감정평가서\현기1612-049.pdf',laparams=LAParams(char_margin=1,line_overlap=0.9,line_margin=0.7)):
    for element in page_layout:
        # if isinstance(element, LTText):
        file2.write(repr(element)+'\n')