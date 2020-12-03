from urllib.parse import quote_plus
from requests import request
from html.parser import HTMLParser
from threading import Thread, Lock, Semaphore

'''
The base query string for op.gg multi-searches
names are appended post "=" sign after they have been made query safe
'''
multi_url = 'https://na.op.gg/multi/query='


'''
@brief: takes in a list of names as it's parameters
        returns a query string for a get request
        throws if no names are passed
'''
def make_multi_query(*names):
  if len(names) > 0:
    query_string = ','.join([quote_plus(name) for name in names])
    return multi_url + query_string
  else:
    raise Exception('Summoner Name missing')


def query_op(url):
  response = request('GET', url)
  return response.text


class Summoner:
  def updateName(self, name):
    self.name = name

  def updateRank(self, rank):
    self.rank = rank
  updateMap = {
    'name': updateName,
    'rank': updateRank
  }

  def __init__(self):
    self.name = ''
    self.rank = ''
    self.updates = []

  def __str__(self):
    return f'name: {self.name}\nrank: {self.rank}'

  def pushUpdate(self, name):
    self.updates.append(name)

  def applyUpdate(self, data):
    if len(self.updates) > 0:
      update = self.updates.pop()
      if update in self.updateMap.keys():
        self.updateMap[update](self, data)

  def asDict(self):
    return { 'name': self.name, 'rank': self.rank }



class Parser(HTMLParser):
  summoners = []

  def handle_starttag(self, tag, attrs):
    if tag == 'div' and tuple(['class', 'summoner-summary']) in attrs:
      self.summoners.append(Summoner())
    if tag == 'div' and tuple(['class', 'summoner-name']) in attrs:
      # print('adding name')
      self.summoners[len(self.summoners)-1].pushUpdate('name')
    if tag == 'div' and tuple(['class', 'lp']) in attrs:
      # print('adding rank')
      self.summoners[len(self.summoners)-1].pushUpdate('rank')

  def handle_data(self, data):
    data = data.replace('\\n', '')
    data = data.lstrip()
    data = data.rstrip()
    if len(self.summoners) > 0:
      if len(data) > 0:
        self.summoners[len(self.summoners) - 1].applyUpdate(data)
    pass

class Crawler(Thread):
  def __init__(self):
    Thread.__init__(self)
    self.parser = Parser()
    self.running_lock = Lock()
    self.running = True
    self.requestQueue = []
    self.queueCounter = Semaphore(0)
    self.daemon = True # Kills the thread once the GUI closes

  def run(self):
    while self.running:
      print('Waiting')
      self.queueCounter.acquire(1)
      with self.running_lock:
        [summoner_names, callback] = self.requestQueue.pop()
        try:
          query = make_multi_query(*summoner_names)
          response_text = query_op(query)
          self.parser.summoners = []
          self.parser.feed(response_text)
          callback([summoner.asDict() for summoner in self.parser.summoners])
        except:
          continue

  def addRequest(self, summonerNames, callback):
    self.requestQueue = [[summonerNames, callback], *self.requestQueue]
    self.queueCounter.release()


  @property
  def summoners(self):
    return self.parser.summoners

if __name__ == '__main__':
  query = make_multi_query('Flaiming Pheonix', 'M0nsterLULU', 'bringmethebeer')
  response_text = query_op(query)
  parser = Parser()
  parser.feed(response_text)
  print(query)
  for s in parser.summoners:
    print(str(s))
