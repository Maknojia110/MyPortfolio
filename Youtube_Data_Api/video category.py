# -*- coding: utf-8 -*-
"""
Created on Wed JUL 31 01:52:53 2019

@author: Shahnawaz Irfan
"""


from apiclient.discovery import build





DEVELOPER_KEY = 'AIzaSyByLQumum94OxxLDbE1Tg0B9XjEVZU6KLs'
youtube = build('youtube','v3', developerKey=DEVELOPER_KEY)

result = youtube.videos().list(part="snippet,statistics,contentDetails",id=vid).execute()

for item in result['items']:
        m=item['snippet']['categoryId']
        




result=youtube.videoCategories( ).list(part ='snippet',id=m).execute() 
for result in result['items']: 
       print(result["snippet"]['title'])
        




      