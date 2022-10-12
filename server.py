import random
import socket
import threading
from Person import Person 
class Server:
    server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    def __init__(self) -> None:
        self.server.bind(("127.0.0.1",9000))
        self.person=[]
        self.rooms={0:set({})}
    def start (self):
        self.server.listen()
    def brodcast(self,message,person):
        print(self.rooms)
        for i in self.rooms[person.roomId]:
            newmessage=str(person)+": "+(message.decode("UTF-8"))
            if(person.client !=i.client):
                i.client.send(newmessage.encode("UTF-8"))
    def add(self):
        while True:
            try:
                client,addr=self.server.accept();
                client.send("NICK".encode("UTF-8"))
                nickname=client.recv(1024).decode("UTF-8")
                person=Person(nickname=nickname, client=client ,roomId=0)
                self.person.append(person)
                room=self.rooms[0]
                room.add(person)
                self.brodcast(f"welcome to server {person.nickname}\n".encode("UTF-8"),person)
                thread=threading.Thread(target =self.handleClient,args=(person,))
                thread.start()
                
            except:
                break
    def remove(self,client):
        for i in self.person:
            if client == i.client:
                self.person.remove(i)
    def handleClient(self,person):
        while True:
            try:
                message=person.client.recv(1024)
                if (message.decode("UTF-8")=="QUIT"):
                    self.remove(person.client) 
                    return
                if (message.decode("UTF-8")=="CREATEROOM"):
                    self.createRoom(person)
                    continue 
                if ("ROOM_ID:" in message.decode("UTF-8")):
                    id=int(message.decode("UTF-8").strip("ROOM_ID:").strip("\n"))
                    self.joinRoom(person,id)
                    print(person)
                    print(self.rooms)
                    continue
                self.brodcast(message,person)
            except:
                pass
    def generateRoomId(self):
        id=random.randint(1000,9999)
        if id in self.rooms.keys():
            self.generateRoomId()
        return id

    def createRoom(self,person):
        id=self.generateRoomId()
        room=self.rooms[person.roomId]
        room.remove(person)
        self.rooms[id]={person}
        person.roomId=id
        person.client.send(f"YOUR ROOM ID IS :{id}\n".encode("UTF-8"))

    def joinRoom(self,person,id):
        if (person.roomId != id):
            if id in self.rooms.keys():
                room=self.rooms[person.roomId]
                room.remove(person)
                room=self.rooms[id]
                room.add(person)
                person.client.send(f"YOU JOINED THE ROOM WITH ID :{id}\n".encode("UTF-8"))
            else:
                room=self.rooms[person.roomId]
                room.remove(person)
                self.rooms[id]={person}
                person.client.send(f"NO! ROOM  WITH ID :{id}\nNEW ROOM WITH ID :{id} IS CRETAED\n".encode("UTF-8"))
            person.roomId=id

server=Server()
server.start()
server.add()
