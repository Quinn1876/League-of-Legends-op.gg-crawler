import tkinter as tk
import crawler as cr
from PIL import ImageTk, Image

class SummonerDisplay(tk.Frame):
  def __init__(self, master=None):
    tk.Frame.__init__(self, master)
    self.name = tk.StringVar()
    self.rank = tk.StringVar()
    self.name.set('')
    self.rank.set('')

    self.nameLabel = tk.Label(self, textvariable=self.name)
    self.rankLabel = tk.Label(self, textvariable=self.rank)
    self.padTop = tk.Frame(self, height=20)

    self.__args = []
    self.__kwargs = {}

  def pack(self, *args, **kwargs):
    tk.Frame.pack(self=self, *args, **kwargs)
    self.padTop.pack(side=tk.TOP)
    self.nameLabel.pack(side=tk.TOP)
    self.rankLabel.pack(side=tk.TOP)

  def place(self, *args, **kwargs):
    tk.Frame.place(self=self, *args, **kwargs)
    self.nameLabel.place(x=10, y=0)
    self.rankLabel.place(x=10, y=10)

  def setSummoner(self, name='', rank=''):

    self.name.set(name)
    self.rank.set(rank)



class Main(tk.Frame):
  def __init__(self, master=None, width=800, height=600):
    master.geometry(f"{width}x{height}")
    master.title('League Screener')
    master.resizable(False, False) # make the window a fixed size
    master.protocol("WM_DELETE_WINDOW", self.cleanup) # Override default shutdown command to clean up the backend
    master.iconbitmap('assets/icon.ico')
    # master.update_idletasks()
    # master.overrideredirect(1)
    # master.update_idletasks()
    tk.Frame.__init__(self, master)
    self.pack(fill=tk.BOTH, expand=1)
    self.master = master

    ## Set the Backround
    img = ImageTk.PhotoImage(Image.open('assets/backdrop.jpg').resize((width, height)))
    self.background = tk.Label(self, image=img)
    self.background.image = img
    self.background.place(x=-1, y=0)
    self.background.pack(side = "bottom", fill = "both", expand = "yes")

    self.summonerContainer = tk.Frame(self)
    self.summoner1 = SummonerDisplay(self.summonerContainer)
    self.summoner2 = SummonerDisplay(self.summonerContainer)
    self.summoner3 = SummonerDisplay(self.summonerContainer)
    self.summoner4 = SummonerDisplay(self.summonerContainer)
    self.summoner5 = SummonerDisplay(self.summonerContainer)

    self.summonerContainer.place(x = 100, y = 100)
    self.summoner1.pack(side=tk.LEFT)
    self.summoner2.pack(side=tk.LEFT)
    self.summoner3.pack(side=tk.LEFT)
    self.summoner4.pack(side=tk.LEFT)
    self.summoner5.pack(side=tk.LEFT)

    self.input = tk.Text(master=self, height=5, width=60, bg="#26265A", bd=0, fg="#FFAA00", font=("Times New Roman", 12), insertbackground="#FFAA00")
    self.paste_button = tk.Button(master=self, text="Paste", command=self.handlePaste, padx=22, bg="#26265A", fg="#FFAA00", font=("Times New Roman", 12))
    self.search_button = tk.Button(master=self, text="Search", command=self.handleSearch, padx=19, bg="#26265A", fg="#FFAA00", font=("Times New Roman", 12))

    self.input.place(x = 60, y = height - 30, anchor=tk.SW)
    self.paste_button.place(x = 580, y = height - 120)
    self.search_button.place(x = 580, y = height - 80)

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

