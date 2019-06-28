from tkinter import *
from pygame import mixer
import tkinter.messagebox
from tkinter import filedialog
from mutagen.mp3 import MP3
import os

root = Tk()
root.title("Music Player")
root.iconbitmap('music.ico')
root.geometry('550x670')
root.resizable(0,0)

mixer.init()


def on_closing():
    from tkinter import messagebox
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()
        # cv2.destroyAllWindows()
root.protocol("WM_DELETE_WINDOW", on_closing)

def info():
    tkinter.messagebox.showinfo('About us','This is a music player which works on your choice!!')

def play_music():
    try:
        global selected_song
        selected_song = listbox.curselection()
        selected_song = int(selected_song[0])
        mixer.music.load(listofsongs[selected_song])
        mixer.music.play()
        listbox.itemconfig(selected_song,bg = 'turquoise3')
        statusbar['text'] = 'Playing '+ os.path.basename(os.path.basename(listofsongs[selected_song]))
        audio = MP3(listofsongs[selected_song])
        len = audio.info.length
        min, sec = divmod(len, 60)
        min = round(min)
        sec = round(sec)
        timeformat = '{:02d}:{:02d}'.format(min, sec)
        show_length['text'] = 'Length -' + ' ' + timeformat

    except Exception as e:
        print(e)
        tkinter.messagebox.showerror('Error','No file chosen!!')

def stop_music():
    mixer.music.stop()
    statusbar['text'] = 'Music stopped'

def set_vol(val):
    volume=int(val)/100
    mixer.music.set_volume(volume)

def browse_button():
    global filename_path
    filename_path = filedialog.askdirectory()
    add_to_playlist(filename_path)

listofsongs = []
def add_to_playlist(f):
    global listofsongs
    global listbox
    global index
    index = 0
    os.chdir(f)
    for i in os.listdir(f):
        if i.endswith('.mp3'):
            filename = os.path.basename(i)
            file = os.path.realpath(i)
            listbox.insert(index,filename)
            listofsongs.append(file)
            index+=1
    mixer.music.load(listofsongs[0])
    mixer.music.play()
    statusbar['text'] = 'Playing music '+os.path.basename(listofsongs[0])
    audio = MP3(listofsongs[0])
    len = audio.info.length
    min, sec = divmod(len, 60)
    min = round(min)
    sec = round(sec)
    timeformat = '{:02d}:{:02d}'.format(min, sec)
    show_length['text'] = 'Length -' + ' ' + timeformat
    listbox.itemconfig(0, bg = 'turquoise3')


pause = True
def pause_music():
    global pause
    if pause:
        mixer.music.pause()
        statusbar['text'] = 'Music paused'
        pause = False
    else:
        mixer.music.unpause()
        statusbar['text'] = 'Music unpaused'
        pause = True

# for menu bar .......................................................................................
menubar = Menu(root)
root.config(menu = menubar)

subMenu = Menu(menubar,tearoff = 0)
menubar.add_cascade(label = 'File',menu = subMenu)
menubar.add_cascade(label = 'About',command = info)
subMenu.add_command(label = 'Open',command = browse_button)
subMenu.add_command(label = 'Exit',command = root.destroy)


# Root ..............................................................................................

text = Label(root)
text.pack(fill = X)


# Top Frame ...........................................................................................
top_frame = Frame(root)
top_frame.pack()


listbox = Listbox(top_frame,selectmode=ACTIVE,width=90,height=20,fg='white',bg = 'black',font = ('times',10),relief = SUNKEN)
listbox.pack(fill = X)

sb = Scrollbar(root,orient = 'vertical')
sb.configure(command = listbox.yview)
sb.pack(side = 'right',fill = 'y')
listbox.configure(yscrollcommand = sb.set)



show_length = Label(root,text = "Length - --:-- ",font = ('times',13))
# show_length.grid(row = 1,column = 0,pady = 10)
show_length.place(x = 10,y = 370)


# Lowest Frame ...............................................................................................

lowest_frame = Frame(root)
lowest_frame.pack()

def add_button():
    file1 = filedialog.askopenfilename()
    print(file1)
    file2 = os.path.basename(file1)
    listbox.insert(0,file2)
    listofsongs.insert(0,file1)

add_button = Button(lowest_frame,text = 'ADD SONG',bg = 'yellow',fg = 'black',width = 10,font = ('times',10,'bold'),command  = add_button)
add_button.pack(side = LEFT,padx = 30,pady = 40)

def del_song():
    deletedsong = listbox.curselection()
    deletedsong = int(deletedsong[0])
    listbox.delete(deletedsong)
    listofsongs.remove(listofsongs[deletedsong])
    print(listofsongs)

del_button = Button(lowest_frame,text = 'DEL SONG',bg = 'yellow',fg = 'black',width = 10,font = ('times',10,'bold'),command = del_song)
del_button.pack(side = LEFT,pady = 40)


# Middle Frame...........................................................................................

from PIL import Image,ImageTk

middle_frame = Frame(root)
middle_frame.pack(pady = 10)

img1 = ImageTk.PhotoImage(Image.open('play_button.png'))
image1 = Button(middle_frame,image = img1,activebackground = 'black',command = play_music)
image1.grid(row = 0,column = 0,padx = 10)

img3 = ImageTk.PhotoImage(Image.open('pause_button.png'))
image3 = Button(middle_frame,image = img3,activebackground = 'black',command = pause_music)
image3.grid(row = 0,column = 1,padx = 10)

img2 = ImageTk.PhotoImage(Image.open('stop_button.png'))
image2 = Button(middle_frame,image = img2,activebackground = 'black',command = stop_music)
image2.grid(row = 0,column = 2,padx = 10)

# Bottom Frame ..................................................................................................

bottom_frame = Frame(root)
bottom_frame.pack()

scale1 = Scale(bottom_frame,from_ =0,to = 100,orient = HORIZONTAL,command = set_vol,resolution = 10)
scale1.set(70)
scale1.grid(row = 0,column = 3)
# mixer.music.set_volume(0.7)

volume = Label(bottom_frame,text = 'VOLUME',font = ('times',10,'bold'))
volume.grid(row = 1,column = 3)

# Root ..................................................................................................

statusbar = Label(root,text = 'Play music',relief = SUNKEN,anchor = W,bg = 'black',fg = 'white')
statusbar.pack(side = BOTTOM,fill = X)

global filename_path
filename_path = filedialog.askdirectory()
add_to_playlist(filename_path)

root.mainloop()