import tkinter
import socket 
import threading
from tkinter import DISABLED, END, NORMAL, Label, simpledialog
from tkinter import Tk
import multiprocessing

class Client:
    server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    def __init__(self) -> None:
        self.server.connect(("127.0.0.1",9000))
        root=Tk()
        root.withdraw()
        self.nickname=simpledialog.askstring(root,"enter  your Nickname")
        
    def receive(self):
        while True:
            try:
                message=self.server.recv(1024)
                if(message.decode("UTF-8")=="NICK"): 
                    self.server.send(self.nickname.encode("UTF-8"))
                else :
                    self.messagebox.config(state=NORMAL)
                    self.messagebox.insert(END,message.decode("UTF-8"))
                    self.messagebox.config(state=DISABLED)
                    print(message.decode("UTF-8"))    
            except:
                break
    def send(self):
            message=self.enterbox.get("1.0",END )
            yourMessage="You : "+message
            self.messagebox.config(state=NORMAL)
            self.messagebox.insert(END,yourMessage)
            self.messagebox.config(state=DISABLED)
            self.enterbox.delete(1.0,END)
            self.server.send(message.encode("utf-8"))
    
    def changeRoom(self,room):
        message="ROOM_ID:"+room
        self.server.send(message.encode("utf-8"))
        self.messagebox.config(state=NORMAL)
        self.messagebox.delete(1.0,END)
        self.messagebox.config(state=DISABLED)

    def changeRoomUI(self):
        room=str(simpledialog.askinteger("Change Room","enter  ROOM_ID:",parent=self.window))
        self.changeRoom(room)
        print (room)

    def createRoom(self):
        self.messagebox.config(state=NORMAL)
        self.messagebox.delete(1.0,END)
        self.messagebox.config(state=DISABLED)
        self.server.send("CREATEROOM".encode("utf-8"))

    def gui(self):
        self.window=Tk()
        self.window.geometry("600x400")
        self.window.title(self.nickname)
        self.title=tkinter.Label(self.window,text="Chat Room")
        self.title.pack()
        self.messagebox=tkinter.Text(self.window,height=10)
        self.messagebox.pack(padx=10,pady=20)
        self.messagebox.config(state=DISABLED)
        self.enterbox=tkinter.Text(self.window,height=5)
        self.enterbox.pack(padx=10,pady=20)
        self.sendbutton=tkinter.Button(self.window,height=2,width=6,text="SEND",bg="Blue",fg="white",command=self.send,font=("Arial",10))
        self.sendbutton.pack(padx=10,pady=2)
        self.options=tkinter.Frame(self.window)
        self.options.pack(padx=10,pady=2)
        self.joinbutton=tkinter.Button(self.options,height=1,width=6,text="JOIN",bg="Blue",fg="white",command=self.changeRoomUI,font=("Arial",10))
        self.joinbutton.grid(row=0,column=0)
        self.createbutton=tkinter.Button(self.options,height=1,width=6,text="CREATE",bg="Blue",fg="white",command=self.createRoom,font=("Arial",10))
        self.createbutton.grid(row=0,column=1)
        self.window.mainloop()
        self.server.send("QUIT".encode("utf-8"))



client=Client()
window=threading.Thread(target=client.gui)
window.start()
client.receive()