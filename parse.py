#!/usr/bin/python
import re
import simplejson as json

def getClient(clientText):
  urlRegexp = re.compile("\<.*[a|A].*\>(.*)\<.*/[a|A].*\>")
  client = urlRegexp.match(dict['source'])
  if client == None:
    client = dict['source']
  else:
    client = client.groups()[0]
  return client
for line in file('tweets.json'):
  dict=json.loads(line)
  # make sure the tweet hasn't been deleted
  if 'delete' not in dict.keys():
    client = getClient(dict['source'])
    print client
#    print '%d\t%s\t%s\t%s\t%s' % (dict['id'],dict['created_at'],client,dict['user']['screen_name'],dict['text'])
print dict.keys()
