import tkinter as tk
import crawler as cr

class SummonerDisplay(tk.Frame):
  def __init__(self, master=None):
    tk.Frame.__init__(self, master)
    self.name = tk.StringVar()
    self.rank = tk.StringVar()
    self.name.set('')
    self.rank.set('')

    self.nameLabel = tk.Label(self, textvariable=self.name)
    self.rankLabel = tk.Label(self, textvariable=self.rank)

  def pack(self, *args, **kwargs):
    tk.Frame.pack(self=self, *args, **kwargs)
    self.nameLabel.pack(side=tk.TOP)
    self.rankLabel.pack(side=tk.TOP)

  def setSummoner(self, name='', rank=''):
    self.name.set(name)
    self.rank.set(rank)



class Main(tk.Frame):
  def __init__(self, master=None):
    master.geometry("800x600")
    master.title('League Screener')
    master.protocol("WM_DELETE_WINDOW", self.cleanup)
    tk.Frame.__init__(self, master)
    self.pack(fill=tk.BOTH, expand=1)
    self.master = master

    self.summonerContainer = tk.Frame(self)
    self.summoner1 = SummonerDisplay(self.summonerContainer)
    self.summoner2 = SummonerDisplay(self.summonerContainer)
    self.summoner3 = SummonerDisplay(self.summonerContainer)
    self.summoner4 = SummonerDisplay(self.summonerContainer)
    self.summoner5 = SummonerDisplay(self.summonerContainer)

    self.summonerContainer.pack(side=tk.TOP, fill=tk.BOTH)
    self.summoner1.pack(side=tk.LEFT)
    self.summoner2.pack(side=tk.LEFT)
    self.summoner3.pack(side=tk.LEFT)
    self.summoner4.pack(side=tk.LEFT)
    self.summoner5.pack(side=tk.LEFT)

    self.controls = tk.Frame(self)
    self.input = tk.Text(master=self.controls, height=5, width=60)
    self.button_container = tk.Frame(self.controls)
    self.paste_button = tk.Button(master=self.button_container, text="Paste", command=self.handlePaste, padx=22)
    self.search_button = tk.Button(master=self.button_container, text="Search", command=self.handleSearch, padx=19)

    self.controls.pack(side=tk.BOTTOM, pady=50)
    self.button_container.pack(side=tk.RIGHT)
    self.input.pack(side=tk.RIGHT, padx=50)
    self.paste_button.pack(pady=4)
    self.search_button.pack(pady=4)

    # Connection to Crawler
    self.crawler = cr.Crawler()
    self.crawler.start()

  def handlePaste(self):
    clipboard = self.master.clipboard_get()
    if len(clipboard) > 0:
      self.input.delete('1.0', tk.END)
      self.input.insert(tk.END, clipboard)

  def handleSearch(self):
    search_request = self.input.get('1.0', tk.END)
    # Format the search request for our caller
    lines = search_request.split('\n')
    summoners = []
    for line in lines:
      for summoner in [(summoner[:summoner.find('joined')].rstrip(' ') if summoner.find('joined') > 0 else summoner) for summoner in line.split(',') if len(summoner[:summoner.find('joined')].rstrip(' ')) > 0]:
        summoners.append(summoner)

    self.crawler.addRequest(summoners, self.crawlerCallback)

  def crawlerCallback(self, summoners):
    print(summoners)
    self.summoner1.setSummoner(**summoners[0])
    self.summoner2.setSummoner(**summoners[1])
    self.summoner3.setSummoner(**summoners[2])
    self.summoner4.setSummoner(**summoners[3])
    self.summoner5.setSummoner(**summoners[4])

  def cleanup(self):
    self.master.destroy()

app=tk.Tk()
main = Main(app)
main.mainloop()

