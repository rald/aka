#!/usr/bin/env python3



import socket
import sys
import os


serv = "irc.undernet.org"
port = 6667
nick = "siestu"
pwrd = None
chan = "#makati"



DATA_FILE = "data.txt"



def skip(h, n):
    p = h.find(n)
    if p != -1:
        s0 = h[0:p]
        s1 = h[p + 1 :]
        return s0, s1
    return None, h



irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
irc.connect((serv, port))



if pwrd:
    irc.send(str.encode("PASS {}\r\n".format(pwrd)))
irc.send(str.encode("NICK {}\r\n".format(nick)))
irc.send(str.encode("USER {} {} {} :{}\r\n".format(nick, nick, nick, nick)))



buf = ""
while 1:
    buf += irc.recv(2040).decode()
    lst = buf.split("\r\n")
    lst = list(filter(None,lst))

    while len(lst) >= 1:
        txt = lst.pop(0)
        buf = "\r\n".join(lst)

        print(txt)

        if txt:
            usr = serv
            tmp = txt
            cmd = None
            par = None
            if tmp[0] == ":":
                usr, tmp = skip(tmp[1:], " ")
                if usr:
                    src, _ = skip(usr, "!")
                    cmd, par = skip(tmp, " ")

            """
            print("src: {}".format(src))
            print("cmd: {}".format(cmd))
            print("par: {}\r\n".format(par))                """
        
            if txt.find("PING") != -1:
                irc.send(str.encode("PONG {}\r\n".format(txt.split()[1])))
            elif cmd == "001":
                irc.send(str.encode("JOIN {}\r\n".format(chan)))
            elif cmd == "PRIVMSG" or cmd == "NOTICE":

                dst, msg = skip(par, " ")
                msg = msg[1:] if msg[0]==":" else msg

                print(
                    "{}{} <{}> {}".format(
                        "NOTICE: " if cmd == "NOTICE" else "", dst, src, msg
                    )
                )

                if msg.startswith(".aka"):
                    aka=msg[4:].strip()
                    
                    found = False
                    lines=[]
                    if os.path.exists(DATA_FILE):
                        with open(DATA_FILE,"r") as f:
                            for line in f:
                                lines.append(line.strip()) 

                        for line in lines:
                            lst=line.strip().split()
                            if aka.upper() in (name.upper() for name in lst):
                                found = True
                                irc.send(str.encode("PRIVMSG {} :{}: {} AKA: {}\r\n".format(chan,src,aka,line.strip())))
                                break

                            
            elif cmd == "NICK":

                fromNick = src;
                toNick = par[1:] if par[0]==":" else par;

                fromNick=fromNick.strip()
                toNick=toNick.strip()

                print("{} changed nick to {}.".format(fromNick,toNick))

                found = False
                lines=[]
                if os.path.exists(DATA_FILE):
                    with open(DATA_FILE,"r") as f:
                        for line in f:
                            lines.append(line.strip())

                    for i in range(len(lines)):
                        lst=lines[i].split()
                        if (fromNick.upper() in (name.upper() for name in lst)) or (toNick.upper() in lst):
                            found = True
                            if fromNick.upper() not in (name.upper() for name in lst):
                                lines[i]+=" "+fromNick.strip()                            
                            if toNick.upper() not in (name.upper() for name in lst):
                                lines[i]+=" "+toNick.strip()                            
                            break


                if not found:
                    lines.append(fromNick+" "+toNick)
                    

                for i in range(len(lines)):
                    lst0=lines[i].split();

                    again = True
                    while again:
                        again = False
                        for j in range(i+1,len(lines)):
                            lst1=lines[j].split()
                            for k in lst1:
                                if k.upper() in (name.upper() for name in lst0):

                                    lines[i]+=" "+lines[j].strip()
                                    again = True                
                                    break


                with open(DATA_FILE,"w") as f:
                    for line in lines:
                        f.write(line+"\n")
 

