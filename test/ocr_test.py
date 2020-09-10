from PIL import Image
from pytesseract import *
from pdf2image import convert_from_path, convert_from_bytes
import configparser
import os

config = configparser.ConfigParser()
config.read(os.path.dirname(os.path.realpath(__file__)) + os.sep + 'envs' + os.sep + 'property.ini')

def ocrToStr(outTxtPath, fileName, lang='kor'):
    path = os.path.join('1.감정평가서','000210-20190130102490-1-0000.pdf')
    images = convert_from_path(path)
    for img in images:
        txtName = os.path.join(outTxtPath,fileName.split('.')[0])
        outText = image_to_string(img, lang=lang, config='--psm 1 -c preserve_interword_spaces=1')
        strTotxt(txtName,outText)

def strTotxt(txtName, outText):
    try:
        file = open(txtName + '.txt','a+', encoding='utf-8')
    except FileNotFoundError:
        file = open(txtName + '.txt', 'w+', encoding='utf-8')
    finally:
        file.write(outText)

if __name__ == "__main__":
    outTxtPath = os.path.dirname(os.path.realpath(__file__))
    ocrToStr(outTxtPath, 'out.txt', 'kor+eng')
