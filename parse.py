#!/usr/bin/python
""" parses twitter JSON data from stdin.  A huge to-do
    is to accept input/output filenames.  right now, the filenames are hard-coded for testing
    purposes """
import re
import simplejson as json
import codecs
import sys



def writeToLog(logFile,text):
  fileHandle.write(text + '\n')

def getClient(clientText):
  urlRegexp = re.compile("\<.*[a|A].*\>(.*)\<.*/[a|A].*\>")  #h/t @mattrepl for the regexp.
  client = urlRegexp.match(dict['source'])
  if client == None:
    client = clientText
  else:
    client = client.groups()[0]
  return client

logFile='tweets.txt'
badFile='bad.txt'

logFileHandle = codecs.open(logFile,'a','utf-8')
badFileHandle = codecs.open(badFile,'a','utf-8')
  
for line in sys.stdin:
  try:
    dict=json.loads(line)
    
  except:
    # if we can't convert the json to a dict, lets log it and skip the row.
    writeToLog(badFileHandle,line)
    continue
    
  try:
    # look for a text element.  this helps avoid deleted and scrub_geo tweets.
    if 'text' not in dict.keys():
      continue
    
    # check to see if the tweet has a source.  This might not be necessary
    # i ran into tweets without a source but those might have been scrub_geo tweets
    if 'source' in dict.keys():
      client = getClient(dict['source'])
    else:
      client = 'Undefined'
      
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
    writeToLog(logFileHandle,text)
  except:
    #text = '%d\t%s' % (dict['id'],dict['user']['screen_name'])
    writeToLog(badFileHandle,line + '\n')
logFileHandle.close()
badFileHandle.close()
    