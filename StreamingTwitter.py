import sys
import tweepy
import re 
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
import json
import csv
import random


# Creating dataset for Non-violation Tweets 
class myStreamListenerPOS(tweepy.StreamListener):
    def __init__(self, limit, api=None):
        self.n = limit
        self.api = api

    def on_status(self, status):
        try:
            tweets = []
            name = status.author.screen_name
            textTwitter = status.text
            
            #Converting into lowercase
            Tweet = textTwitter.lower()
            
            #Converting www.* or https?://* to URL
            Tweet = re.sub('((www\.[\s]+)|(https?://[^\s]+))','URL',Tweet)
            
            #Converting @username to User
            Tweet = re.sub('@[^\s]+','TWITTER_USER',Tweet)
            
            #Additional white space removal
            tweet = re.sub('[\s]+', ' ', Tweet)
            
            #Replacing words with hashtags
            Tweet = re.sub(r'#([^\s]+)', r'\1', Tweet)
            
            #trimming the tweeets
            Tweet = Tweet.strip('\'"')
            
            #happy and sad face emoticon removal
            a = ':)'
            b = ':('
            
            Tweet = Tweet.replace(a,'')
            Tweet = Tweet.replace(b,'')
           
            
            #Twitter @username tag and reTweets removal
            tag = 'TWITTER_USER' 
            rt = 'rt'
            Tweet = Tweet.replace(tag,'')
            Tweet = Tweet.replace(rt,'')
            final_tweet = Tweet
    
            f = open('pos_tweets.json', 'r+', encoding='utf-8')
            new = f.read()
            f.write(final_tweet+'\n')
            f.close()
        
            self.n = self.n+1
            if self.n < 3000: 
                return True
            else:
                print ('limit = '+str(self.n))
                return False
        
        except Exception as e:
            print (e)

    def on_error(self, status_code):
        
        return True  

    def on_timeout(self):
        
        return True 
        

# Creating dataset for Violation Tweets
class myStreamListenerNEG(tweepy.StreamListener):
    def __init__(self, limit, api=None):
        self.n = limit
        self.api = api

    def on_status(self, status):
        try:
            tweets = []
            name = status.author.screen_name
            textTwitter = status.text
            
            #Converting into lowercase
            Tweet = textTwitter.lower()
            
            #Converting www.* or https?://* to URL
            Tweet = re.sub('((www\.[\s]+)|(https?://[^\s]+))','URL',Tweet)
            
            #Converting @username to TWITTER_USER
            Tweet = re.sub('@[^\s]+','TWITTER_USER',Tweet)
            
            #Additional white space removal
            tweet = re.sub('[\s]+', ' ', Tweet)
            
            #Replacing words with hashtags
            Tweet = re.sub(r'#([^\s]+)', r'\1', Tweet)
            
            #trim
            Tweet = Tweet.strip('\'"')
            
            #happy and sad face emoticon removal 
            a = ':)'
            b = ':('
            Tweet = Tweet.replace(a,'')
            Tweet = Tweet.replace(b,'')
                        
            #Twitter @username tag and reTweets removal
            tag = 'TWITTER_USER' 
            rt = 'rt'
            Tweet = Tweet.replace(tag,'')
            Tweet = Tweet.replace(rt,'')
            final_tweet = Tweet
            
            f = open('neg_tweets.json', 'r+', encoding='utf-8')
            new = f.read()
            f.write(final_tweet+'\n')
            f.close()
        
            self.n = self.n+1
            if self.n < 3000: 
                return True
            else:
                print ('limit = '+str(self.n))
                return False
        
        except Exception as e:
            print (e)

    def on_error(self, status_code):
        
        return True 

    def on_timeout(self):
       
        return True 



    #Applying the authentication keys for streaming
def mainPOS():
    consumer_key = '14egBNgPz3kYv0KIvSt79BHT9'
    consumer_secret = 'BDByhniYiDPzzoiZL2YihQrP3G9O8Vq7IvT2HviazKkFVHzQv3'
    access_token = '2908010127-KQ7vuf5fLF4RAGV3ASXquj2XGzNpqpXLe5ai0d8'
    access_token_secret = 'V7iVXUYhqtmLru3C8X78jQZZo6O1w0GuPdadKRoJtSWSu'

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth) 

    print ("Establishing stream...\n")
    #filtering tweets using Non-violation keywords
    PosTweets = tweepy.streaming.Stream(auth, myStreamListenerPOS(limit=0))
    setTerms = [':)','happy', 'exited','beautiful']
    PosTweets.filter(None, setTerms, languages=["en"])
    
    #applying the authentication keys for streaming 
def mainNEG():
    consumer_key = '14egBNgPz3kYv0KIvSt79BHT9'
    consumer_secret = 'BDByhniYiDPzzoiZL2YihQrP3G9O8Vq7IvT2HviazKkFVHzQv3'
    access_token = '2908010127-KQ7vuf5fLF4RAGV3ASXquj2XGzNpqpXLe5ai0d8'
    access_token_secret = 'V7iVXUYhqtmLru3C8X78jQZZo6O1w0GuPdadKRoJtSWSu'

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth) 
    print ("Establishing stream...\n")
    #filtering tweets using violation keyword
    NegTweets = tweepy.streaming.Stream(auth, myStreamListenerNEG(limit=0))
    setTermsNEG =['armed conflict','illegal detention','injustice','activist','warfare','killings','racism', 'racial discrimination','pay inequality','sexual harassment', 'child abuse',
                  'dictatorship','genocide','invasion','slavery', 'child exploitation', 'oppression', 'refugee displacement','prejudice','Human trafficking','Child soldiers', 'Child labor',
                  'Gang violence', 'Child abuse','ethnic cleansing','mass graves','cheap labor', 'gay rights','Forced sterilization','sexual assault','bloodshed','warfare','chemical gas', 'gas attack']
    NegTweets.filter(None, setTermsNEG, languages=["en"])
     
    

if __name__ == '__main__':
    try:
        mainPOS()
        #mainNEG()
   
    except KeyboardInterrupt:
        print ("Disconnecting from Twitter... ")
print ("Done") 
