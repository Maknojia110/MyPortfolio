

from apiclient.discovery import build
import pandas as pd

comments =[]
comment_id=[]
reply_count=[]
like_count=[]
comment_visible=[]
canreply=[]
user_id=[]
v_title=[]
vc=[]
playlist=[]
channel=[]
thumbnails=[]
c_id=[]
views=[]
c_ids=[]
vc=[]
temp=[]
dic=[]
pub=[]
dur=[]
defe=[]
like=[]
dislike=[]
c_title=[]
views_c=[]
thumbnails=[]
v_id=[]

p_id='PLXCG07DgKAFGWtoRZKy_KLFjDwrpaaSB8'

DEVELOPER_KEY ='AIzaSyBxjLtSETldawmT55XBVs_3nUgTjI7DFLw'
youtube = build('youtube', 'v3', developerKey=DEVELOPER_KEY)

#first extract all playlist_id#

def get_playlist(youtube, **kwargs):
 request = youtube.playlistItems().list(**kwargs).execute()
 while request:
  for item in request['items']: 
    playlist.append(item["snippet"]["resourceId"]["videoId"])
     
    
  if 'nextPageToken' in request:
            kwargs['pageToken'] = request['nextPageToken']
            request = youtube.playlistItems().list(**kwargs).execute()
  else:
     break
     
    
aa=get_playlist(youtube,part="snippet,contentDetails",pageToken=None,playlistId=p_id)

i=0

while(i<len(playlist)):
    
 def get_video_comments(youtube, **kwargs):
      results = youtube.commentThreads().list(**kwargs).execute()
 
      while results:
        for item in results['items']:
             
            reply_count.append(item['snippet']['totalReplyCount'])
            comment_id.append(item['snippet']['topLevelComment']['id'])
            #print()
            
            comment_visible.append(item['snippet']['isPublic'])
            canreply.append(item['snippet']['isPublic'])
            user_id.append(item['id'])
            comments.append(item['snippet']['topLevelComment']['snippet']['textDisplay'])

            
            

                
        if 'nextPageToken' in results:
            kwargs['pageToken'] = results['nextPageToken']
            results = youtube.commentThreads().list(**kwargs).execute()
        else:
            break
 
 result = youtube.videos().list(part="snippet,statistics,contentDetails",id=playlist[i]).execute()
 for item in result['items']:
          v_title.append(item["snippet"]["title"])
          channel.append(item['snippet']['channelTitle'])
          thumbnails.append(item['snippet']['thumbnails']['default']['url'])
          c_id.append(item['snippet']['channelId'])
          views.append(item['statistics']['viewCount'])
          c=item['snippet']['categoryId']
          dic.append(item['snippet']['description'])
          pub.append(item['snippet']['publishedAt'])
          dur.append(item['contentDetails']['duration'])
          defe.append(item['contentDetails']['definition'])
          like.append(item['statistics']['likeCount'])
          dislike.append(item['statistics']['dislikeCount'])
          views_c.append(item['statistics']['viewCount'])
          c_title.append(item['snippet']['channelTitle'])
          
      
 result=youtube.videoCategories( ).list(part ='snippet',id=c).execute() 
 for result in result['items']: 
         vc.append(result["snippet"]['title'])

        
 v_id.append(playlist[i])      
 print('video',i+1)       
 comments110=get_video_comments(youtube,part = 'snippet',videoId=playlist[i],pageToken=None,textFormat='plainText')
 
 df1 =pd.DataFrame({'Video_Title':v_title})
 df3 =pd.DataFrame({'comments':comments})
 df2=pd.DataFrame({'id':user_id})
 df4=pd.DataFrame({'Category':vc})
 df5=pd.DataFrame({'Discription':dic})
 df6=pd.DataFrame({'publishedAt':pub})
 df7=pd.DataFrame({'Duration':dur})
 df8=pd.DataFrame({'Defination':defe})
 df9=pd.DataFrame({'likes':like})
 df10=pd.DataFrame({'Dislike':dislike})
 df11=pd.DataFrame({'channel_Title':c_title})
 df12=pd.DataFrame({'Views_count':views_c})
 df13=pd.DataFrame({'Video_Thumbnail':thumbnails})
 df14=pd.DataFrame({'v_id':v_id})
  
 

 
 f2 =(df1,df2,df3,df4,df5,df6,df7,df8,df9,df10,df11,df12,df13,df14)
 result = pd.concat(f2,axis=1,join_axes=[df2.index])
 df = pd.DataFrame(result)
 abc=str(v_title).replace('(','').replace(')','').replace('|','').replace(',','').replace('-','').replace('[','').replace(']','').replace(' ','').replace('/','').replace('.','').replace('"','').replace(';','').replace(':','').replace('#','').replace('$','').replace('^','').replace('&','').replace('*','').replace('!','').replace('~','').replace('`','').replace('<','').replace('>','').replace('?','').replace('%','')[1:-1]   
 df.to_csv('C:/Users/RIP/Desktop/playlist/'+abc+'.csv',index=False)
      
 v_title.clear()
 
 views_c.clear()
 thumbnails.clear()
 vc.clear()
 user_id.clear()
 comments.clear()
 dic.clear()
 pub.clear()
 dur.clear()
 defe.clear()
 like.clear()
 dislike.clear()
 c_title.clear()
 v_id.clear()
 i=i+1   
 

 

   