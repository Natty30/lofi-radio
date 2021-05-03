from tkinter import *
import os, vlc, pafy #youtube-dl needed
import re, urllib.parse, urllib.request
from bs4 import BeautifulSoup
import threading

w=Tk()

def start():
    global isplaying
    global url
    isplaying = True
    video = pafy.new(url)
    best = video.getbest()
    playurl = best.url
    Instance = vlc.Instance("--no-video") #hide video player
    Instance.log_unset() #hide logs
    player = Instance.media_player_new()
    Media = Instance.media_new(playurl)
    Media.get_mrl()
    player.set_media(Media)
    while isplaying:
        player.play()
    player.stop()

def play(stream):
    global url
    url = stream
    global isplaying
    if isplaying:
        isplaying = False
        threading.Thread(target=start).start()
    else:
        threading.Thread(target=start).start()

def threaded_scrape(tagarg):
    global music_name
    music_name = tagarg
    threading.Thread(target=scrape).start()

def scrape():
    global music_name
    i = 0
    wid = 80
    query_string = urllib.parse.urlencode({"search_query": music_name})
    formatUrl = urllib.request.urlopen("https://www.youtube.com/results?" + query_string)
    search_results = re.findall(r"watch\?v=(\S{11})", formatUrl.read().decode())
    while wid+30<220:
                try:
                    Button(w,width=57,height=1,text=pafy.new("https://www.youtube.com/watch?v=" + search_results[i]).title,command=lambda i=i: play("https://www.youtube.com/watch?v=" + search_results[i]),border=0,fg='white',bg='#249794').place(x=10,y=wid)
                    wid += 20
                    i += 1
                except Exception as e:
                    break

def exit():
    os._exit(0)

isplaying = False
url = ""
music_name = "lofi"
width_of_window = 427
height_of_window = 250
screen_width = w.winfo_screenwidth()
screen_height = w.winfo_screenheight()
x_coordinate = (screen_width/2)-(width_of_window/2)
y_coordinate = (screen_height/2)-(height_of_window/2)
w.geometry("%dx%d+%d+%d" %(width_of_window,height_of_window,x_coordinate,y_coordinate))
w.title("LoFi")
#w.overrideredirect(1)
a='#249794'
w.configure(background='#249794')
Frame(w,width=427,height=241,bg=a).place(x=0,y=0)
b2=Button(w,width=10,height=1,text='Exit',command=exit,border=0,fg=a,bg='white')
b2.place(x=180,y=220)
l1=Label(w,text='Lo-Fi radio',fg='white',bg=a)
lst1=('Calibri (Body)',18,'bold')
l1.config(font=lst1)
l1.place(x=155,y=10)
tags=[]
try:
    with open("config.fi", "r") as configfile:
        configcontents = configfile.read()
        data = configcontents.split("\n")
        if len(data)>4:
            tags = configcontents.split("\n", 4)[:-1]
        else:
            tags = configcontents.split("\n")
except Exception as e:
    print(e)
    tags = ["lofi", "coding lofi", "anime lofi", "star wars lofi"]
i = 55
Label(w,text='Tags:',fg='white',bg=a,font=('Calibri (Body)',10,'bold')).place(x=10,y=50)
for tag in tags:
    Button(w,width=10,height=1,text=tag,command=lambda tag=tag: threaded_scrape(tag),border=0,fg=a,bg='white').place(x=i, y=50)
    i += 90
scrape()
w.resizable(False, False)
w.mainloop()


