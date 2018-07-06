import arxiv as axv
import urllib
import os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from google.colab import auth
from oauth2client.client import GoogleCredentials


def download_arxiv_pdf(drive, savePath, pdf_url):
  response = urllib.request.urlopen(pdf_url)
  file = open('./'+savePath, 'wb') #b for binary
  file.write(response.read())
  file.close()
  print('下载论文' + " " + savePath)
  uploaded = drive.CreateFile({'title': savePath})
  #uploaded.SetContentString(response.read())
  uploaded.SetContentFile('./'+savePath)
  uploaded.Upload()
  print("保存至google drive 云盘成功")
  os.remove('./'+savePath)
  

keywords = 'Machine Learning'
auth.authenticate_user()
gauth = GoogleAuth()
gauth.credentials = GoogleCredentials.get_application_default()
drive = GoogleDrive(gauth)
print('接入google drive')

list = axv.query(search_query=keywords, start=0, max_results=2000)
print('搜索arxiv上关键字：{} 相关的论文'.format(keywords))

print('共找到arxiv收录论文{}篇'.format(len(list)))

print('开始下载...')

for obj in iter(list):
  filename = obj['title'] + ".pdf"
  filename = filename.replace(' ', '_').replace('/', '_').replace('\n', '_')
  pdf_url = obj['pdf_url']
  download_arxiv_pdf(drive, filename, pdf_url)
