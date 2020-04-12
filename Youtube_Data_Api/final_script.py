# -*- coding: utf-8 -*-
"""
Created on Sun Jun  9 01:52:53 2019

@author: Mehdi
"""


from apiclient.discovery import build
import os
import re
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
analyser = SentimentIntensityAnalyzer()


playlists=[]
playlist_title=[]
playlist_items_title=[]
playlists_items=[]
comments =[]
comment_id=[]
reply_count=[]
like_count=[]
comment_visible=[]
canreply=[]
user_id=[]
video_title=[]
vc=[]
playlist=[]
channel=[]
thumbnails=[]
channel_id=[]
views=[]
c_ids=[]
vc=[]
temp=[]
v_discription=[]
v_published=[]
v_duration=[]
v_defination=[]
like=[]
dislike=[]
channel_title=[]
views_count=[]
v_thumbnails=[]
v_id=[]
test=[]
video_privicy=[]
category_id=[]
comments_new=[]
playlist_privicy=[]
comments_sentiments=[]
emojis_sentiments=[]


#----------------------------------------------------------------------------------------#

#Developer_key for Run Youtube_Api 
DEVELOPER_KEY ='AIzaSyCfZcNrgQXEdi4MK0OaNXrgUQoO9Pk1Dvw'
youtube = build('youtube', 'v3', developerKey=DEVELOPER_KEY)

#----------------------------------------------------------------------------------------#
#user pass a channel-Id
ch_id='UCvJJ_dzjViJCoLf5uKUTwoA'

#----------------------------------------------------------------------------------------#  
def get_channel_info(youtube, **kwargs):
  result = youtube.channels().list(**kwargs).execute()
  for item in result['items']:
      channel_title.append(item['snippet']['title'])

#----------------------------------------------------------------------------------------#  
      
#First Extract All Channels Playlist      
def get_playlist(youtube, **kwargs):
 request = youtube.playlists().list(**kwargs).execute()
 while request:
  for item in request['items']: 
    temp=item["id"]
    playlist_title.append(item["snippet"]["title"])
    res=item["status"]["privacyStatus"]
    if  res =='public':
         playlists.append(temp)
    else:
        print('Private Playlist')
    
    
    
  if 'nextPageToken' in request:
            kwargs['pageToken'] = request['nextPageToken']
            request = youtube.playlists().list(**kwargs).execute()
  else:
     break
        
p=get_playlist(youtube,part="snippet,contentDetails,status",pageToken=None,channelId=ch_id)

print(len(playlists),'Playlist Items in This Channel')

#----------------------------------------------------------------------------------------#
#second Extract All Channels Playlist_Items
def get_playlists_items(youtube, **kwargs):
  request = youtube.playlistItems().list(**kwargs).execute()
  while request:
   for item in request['items']: 
    temp=item["snippet"]["resourceId"]["videoId"]
    playlist_items_title.append(item["snippet"]["title"])
    res=item["status"]["privacyStatus"]
    if  res =='public':
        playlists_items.append(temp)    
    else:
        print('Private Video')
    
    
   if 'nextPageToken' in request:
            kwargs['pageToken'] = request['nextPageToken']
            request = youtube.playlistItems().list(**kwargs).execute()
   else:
     break

   
#----------------------------------------------------------------------------------------#
#Third Extract All Videos_Information
def get_videos_items(youtube, **kwargs):
  result = youtube.videos().list(**kwargs).execute()
  for item in result['items']:
          video_title.append(item["snippet"]["title"])
          channel_title.append(item['snippet']['channelTitle'])
          v_thumbnails.append(item['snippet']['thumbnails']['default']['url'])
          channel_id.append(item['snippet']['channelId'])
          views_count.append(item['statistics']['viewCount'])
          v_discription.append(item['snippet']['description'])
          v_published.append(item['snippet']['publishedAt'])
          v_duration.append(item['contentDetails']['duration'])
          v_defination.append(item['contentDetails']['definition'])
          like.append(item['statistics']['likeCount'])
          dislike.append(item['statistics']['dislikeCount'])
          category_id=item['snippet']['categoryId']
          #comments_count.append(item['statistics']['commentCount'])
          result=youtube.videoCategories( ).list(part ='snippet',id=category_id).execute() 
          for result in result['items']: 
            vc.append(result["snippet"]['title'])

#----------------------------------------------------------------------------------------#
#Fourth Extract All  Videos-Comments
def get_video_comments(youtube, **kwargs):    
      results = youtube.commentThreads().list(**kwargs).execute()
      while results:
        for item in results['items']:
            reply_count.append(item['snippet']['totalReplyCount'])
            comment_id.append(item['snippet']['topLevelComment']['id'])
            comment_visible.append(item['snippet']['isPublic'])
            canreply.append(item['snippet']['isPublic'])
            user_id.append(item['id'])  
            res=item['snippet']['topLevelComment']['snippet']['textDisplay']
            if len(res) !=0:
                comments.append(res)
            else:
                print("Null or Disabled Comments")
           
        if 'nextPageToken' in results:
            kwargs['pageToken'] = results['nextPageToken']
            results = youtube.commentThreads().list(**kwargs).execute()
        else:
            break                   
#----------------------------------------------------------------------------------------#
def get_emoji_Detect():
 emoji_pattern = re.compile("["u"\U0001F600-\U0001F64F" u"\U0001F300-\U0001F5FF"  u"\U0001F1E0-\U0001F1FF" "]+",flags=re.UNICODE)     
 emj=[x for x in comments 
        if  re.findall(emoji_pattern, x) 
        ]
 #for English language
 emj=[re.sub('[a-zA-Z0-9]', '', _) for _ in comments]
 #for urdu language
 emj=[re.sub(r'[\u0600-\u06ff- \u093f ]', '', _) for _ in emj]
 #for special character
 emj=[re.sub("[\w  \r \n \d  \xa0]", '', _) for _ in emj]
 #for special symbols
 emj=[re.sub("[\x21-\x2F\x3A-\x40\x5B-\x60\x7B-\x7E]", '', _) for _ in emj]
 #for chinese language
 emj=[re.sub(u'[＾。↖ω↗ …… ？ ～！⺀-⺙⺛-⻳⼀-⿕々〇〡-〩〸-〺〻㐀-䶵一-鿃豈-鶴侮-頻並-龎]', '', _) for _ in emj]
 #for hindi language
 emj=[re.sub("[\u0900-\u097F]", '', _) for _ in emj]  
 #for Italian language
 emj=[re.sub('[a-zA-ZÀ-ú¡¡]+', '', _) for _ in emj] 
 
 
 return emj 
#----------------------------------------------------------------------------------------#

def get_String_Detect():
 text=[re.sub('[^a-zA-Z0-9 \s]+', '', _) for _ in comments]
 
 
 
 
 return text  

#----------------------------------------------------------------------------------------#

def get_comments_text_sentiments():
    text=[re.sub('[^a-zA-Z0-9 \s]+', '', _) for _ in comments]
    for i in text:
        score = analyser.polarity_scores(i)
        positive=score.get('pos')
        negative=score.get('neg')
        neutral=score.get('neu')
        
        if positive > negative and positive > neutral:
           comments_sentiments.append('positive')
        elif negative > positive and negative > neutral:
           comments_sentiments.append('negative')
        elif neutral > positive and neutral >negative:
           comments_sentiments.append('neutral')
        else:
           comments_sentiments.append('')  
       
    return comments_sentiments   
#----------------------------------------------------------------------------------------#
def get_Emojis_sentiments():
    emoji_pattern = re.compile("["u"\U0001F600-\U0001F64F" u"\U0001F300-\U0001F5FF"  u"\U0001F1E0-\U0001F1FF" "]+",flags=re.UNICODE)     
    emj=[x for x in comments 
            if  re.findall(emoji_pattern, x) 
            ]
     #for English language
    emj=[re.sub('[a-zA-Z0-9]', '', _) for _ in comments]
     #for urdu language
    emj=[re.sub(r'[\u0600-\u06ff- \u093f ]', '', _) for _ in emj]
     #for special character
    emj=[re.sub("[\w  \r \n \d  \xa0]", '', _) for _ in emj]
    #for special symbols
    emj=[re.sub("[\x21-\x2F\x3A-\x40\x5B-\x60\x7B-\x7E]", '', _) for _ in emj]
     #for chinese language
    emj=[re.sub(u'[＾。↖ω↗ …… ？ ～！⺀-⺙⺛-⻳⼀-⿕々〇〡-〩〸-〺〻㐀-䶵一-鿃豈-鶴侮-頻並-龎]', '', _) for _ in emj]
     #for hindi language
    emj=[re.sub("[\u0900-\u097F]", '', _) for _ in emj]  
     #for Italian language
    emj=[re.sub('[a-zA-ZÀ-ú¡¡]+', '', _) for _ in emj] 
    
    for i in emj:
        score = analyser.polarity_scores(i)
        positive=score.get('pos')
        negative=score.get('neg')
        neutral=score.get('neu')
        
        if positive > negative and positive > neutral:
           emojis_sentiments.append('positive')
        elif negative > positive and negative > neutral:
           emojis_sentiments.append('negative')
        elif neutral > positive and neutral >negative:
           emojis_sentiments.append('neutral')
        else:
           emojis_sentiments.append('')  
       
    return emojis_sentiments   



#----------------------------------------------------------------------------------------#

def Remove_Special_characters(x):
    result=str(x).replace('(','').replace(')','').replace(' | ','').replace(',','').replace('-','').replace('[','').replace(']','').replace(' ','').replace('/','').replace('.','').replace('"','').replace(';','').replace(':','').replace('#','').replace('$','').replace('^','').replace('&','').replace('*','').replace('!','').replace('~','').replace('`','').replace('<','').replace('>','').replace('?','').replace('%','').replace('|','')[1:-1]
    return result
#----------------------------------------------------------------------------------------#



#----------------------------------------------------------------------------------------#

#create a parent Directory By channel_id
ch=get_channel_info(youtube,part="snippet",id=ch_id)
var=Remove_Special_characters(channel_title)   
dir_name='../Desktop/'+str(var)+'/' 
 

#----------------------------------------------------------------------------------------#
i=0
j=0
#----------------------------------------------------------------------------------------#
#outer-loop Iterate all playlists in the Channel 
while(i<len(playlists)):
   
#called Playlist Items Method       
 p_items=get_playlists_items(youtube,part="snippet,status",pageToken=None,playlistId=playlists[i]) 
 print('\n playlist id is '+playlists[i]+'\n')
 
 #create a Directories of Playlist
 var=[re.sub('[^a-zA-Z0-9]+', '', _) for _ in playlist_title]    
 os.makedirs(dir_name+var[i])
 #Remove special character from playlist_title
 p_title=Remove_Special_characters(playlist_title)
 
 
  
#create a Directories of Playlist  

 
#Inner-loop Iterate all playlists_Items in the Playlists 
 while(j<len(playlists_items)):
 
  #called videos  Items Method   
  v_items = get_videos_items(youtube,part="snippet,status,statistics,contentDetails",id=playlists_items[j])
  print(v_items)  
  #called comments_extract_Method
  comments_get = get_video_comments(youtube,part = 'snippet',videoId=playlists_items[j],pageToken=None,textFormat='plainText')
  
  
  #emojis_detect_Method_called            
  emojis_detect = get_emoji_Detect()
  emj_sent= get_Emojis_sentiments()
  comments_sent=get_comments_text_sentiments()
  print(emj_sent)
  #String_detect_Method_called
  string_txt = get_String_Detect() 
 
  #Remove special character from video title
  vd_title=Remove_Special_characters(video_title)   
  
  df0=pd.DataFrame({'channel_Title':channel_title}) 
  df1=pd.DataFrame({'Video_Title':video_title})
  df2=pd.DataFrame({'v_id':v_id})
  df3=pd.DataFrame({'id':user_id})
  df4 =pd.DataFrame({'Comments':string_txt})
  df5=pd.DataFrame({'Comments_Sentiments':comments_sent})
  df6=pd.DataFrame({'Emojis':emojis_detect})
  df7=pd.DataFrame({'Emojis_Sentiments':emj_sent})
  df8=pd.DataFrame({'Category':vc})
  df9=pd.DataFrame({'Discription':v_discription})
  df10=pd.DataFrame({'publishedAt':v_published})
  df11=pd.DataFrame({'Duration':v_duration})
  df12=pd.DataFrame({'Defination':v_defination})
  df13=pd.DataFrame({'likes':like})
  df14=pd.DataFrame({'Dislike':dislike})
  df15=pd.DataFrame({'Views_count':views_count})
  df16=pd.DataFrame({'Video_Thumbnail':v_thumbnails})
          
  f2 =(df0,df1,df2,df4,df5,df6,df7,df8,df9,df10,df11,df12,df13,df14,df15,df16)
  result = pd.concat(f2,axis=1,join_axes=[df6.index])
  df = pd.DataFrame(result)
  
  
  df.to_csv(dir_name+var[i]+'/'+vd_title+'.csv',index=False)
  
  
  
  
  #print(p_title)
  comments_sent.clear()
  string_txt.clear()
  emojis_detect.clear()
  emj_sent.clear()
  video_title.clear()
  user_id.clear()
  vc.clear()
  v_discription.clear()
  v_published.clear()
  v_duration.clear()
  v_defination.clear()
  like.clear()
  dislike.clear()
  views_count.clear()
  channel_title.clear()
  vc.clear()
  v_thumbnails.clear()
  playlist_privicy.clear()
  emojis_detect.clear()
  
  j=j+1
 
   
 i=i+1  
 
 
 
 
 
 
 
 
 
 
 