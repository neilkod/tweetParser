#!/usr/bin/python
""" parses twitter JSON data as obtained from the twitter streaming API.  A huge to-do
    is to accept input/output filenames.  right now, the filenames are hard-coded for testing
    purposes """
import re
import simplejson as json
import codecs
import sys


def writeToLogUnicode(logFile,text):
  fileHandle = codecs.open(logFile,'a','utf-8')
  fileHandle.write(text + '\n')
  fileHandle.close()

def getClient(clientText):
  urlRegexp = re.compile("\<.*[a|A].*\>(.*)\<.*/[a|A].*\>")  #h/t @mattrepl for the regexp.
  client = urlRegexp.match(dict['source'])
  if client == None:
    client = clientText
  else:
    client = client.groups()[0]
  return client
  
for line in sys.stdin:
  try:
    dict=json.loads(line)
  except:
    continue
  # make sure the tweet hasn't been deleted
  # if it has, skip it.  The streaming API sends deleted tweets,
  # we'll filter them out here.
  if 'delete' not in dict.keys():
  
    client = getClient(dict['source'])
    
    # remove linefeeds from the tweets.  I'm not sure if this is the best way to handle this.
    tweetText = re.sub('\n','',dict['text'])    
    
    """ build the string that gets written to the file.  its in the format
        id
        timestamp
        client
        username(screen_name)
        tweet text
    """
    
    text = '%d\t%s\t%s\t%s\t%s' % (dict['id'],dict['created_at'],client,dict['user']['screen_name'],tweetText)
    
    writeToLogUnicode('tweets.txt',text)
  
