#!/usr/bin/python
""" parses twitter JSON data from stdin.  A huge to-do
    is to accept input/output filenames.  right now, the filenames are hard-coded for testing
    purposes """
import re
import simplejson as json
import codecs
import sys

archivedProcessedFile = True
archiveDirectory = 'processed'
compressProcessedFile=False




def writeToLog(logFile,text):
  logFile.write(text + '\n')

def getClient(clientText):
  urlRegexp = re.compile("\<.*[a|A].*\>(.*)\<.*/[a|A].*\>")  #h/t @mattrepl for the regexp.
  client = urlRegexp.match(clientText)
  if client == None:
    client = clientText
  else:
    client = client.groups()[0]
  return client
  
def parseTweet(jsondata,logFileHandle):
  try:
    dict=json.loads(jsondata)
    # look for a text element.  this helps avoid deleted and scrub_geo tweets.
    if 'text' in dict.keys():
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
    None


def parseFile(inputFile):

  parsed = 0
  cnt = 0
  
  # for the time being, we'll just assume the outputfile will be inputfile.out
  # we'll make this more dynamic later.
  # if 
  logFileHandle = codecs.open('output/' + inputFile + '.out' ,'w','utf-8')
#  badFileHandle = codecs.open('bad/' + inputFile + '.bad','w','utf-8')
  
  for line in file(inputFile):
    parseTweet(line,logFileHandle)
    cnt = cnt + 1

  print "%s: parsed %d tweets" % (inputFile,cnt)  
  if archivedProcessedFile :
    os.rename(inputFile,archiveDirectory + '/' + inputFile)

    
if __name__ == '__main__':
  logFile='tweets.txt'

  logFileHandle = codecs.open(logFile,'a','utf-8')


  for line in sys.stdin:
    parseTweet(line,logFileHandle)

  logFileHandle.close()
  badFileHandle.close()
    
