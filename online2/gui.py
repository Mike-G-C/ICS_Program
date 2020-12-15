#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
import tkinter.messagebox
#import pickle
import time
from chat_utils import *
import chat_client_class as chat_client
import argparse
import threading

parser = argparse.ArgumentParser(description='chat client argument')
parser.add_argument('-d', type=str, default=None, help='server IP addr')
args = parser.parse_args()

client = chat_client.Client(args)
client.init_chat()



h = 800
w = 700



class GUI():
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Login page")

        self.canvas = tk.Canvas(self.window, height=h, width=w)
        self.canvas.pack()

        self.frame = tk.Frame(self.window, bg='#DDFFE7')
        self.frame.place(relwidth=1, relheight=1)

        self.textFrame = tk.Frame(self.frame, bg='#DDFFE7').place(relwidth=0.5, relheight=0.3,relx=0.2, rely=0.2)
        self.title = tk.Label(self.textFrame, text="Welcome!", font="Times 48 bold",bg='#DDFFE7', fg="#29A0B1").place(relx=0.33, rely=0.25)
        tk.Label(self.textFrame, text="A chatting app could connect the world.", font="Monsterrat", bg='#DDFFE7', fg="#3a93f8").place(
                                                                                                          relx=0.27,
                                                                                                          rely=0.35)

        self.usr_name = tk.StringVar()
        self.usr_name.set("")

        self.label = tk.Label(self.frame, text="Name", bg='#DDFFE7', font="Monsterrat 20")
        self.label.place(relx=0.23, rely=0.65, relwidth=0.07, relheight=0.05)
        self.entry = tk.Entry(self.frame, font=40,textvariable=self.usr_name)
        self.entry.place(relwidth=0.32, relheight=0.05,relx=0.3, rely=0.65)

        #button
        self.button = tk.Button(self.frame, text="Log in", font="Times 18",command=self.fun1)
        self.button.place(relx=0.41, rely=0.8, relwidth=0.08, relheight=0.05)


        self.window.mainloop()



    def fun1(self):

        self.window.destroy()
        self.name = self.usr_name.get()
        ok = tk.messagebox.showinfo(title='Welcome', message='Chat away! ' + self.name)
        client.login(self.name)
        if ok == 'ok':
            self.chat_away()


    def chat_away(self):

        self.window2 = tk.Tk()
        self.window2.geometry("700x800")
        self.window2.title(self.name + "'s chatroom")

        '''Create Frames'''
        self.f_msglist = tk.Frame(self.window2,height = 400,width = 700, bg='#DDFFE7') #创建<消息列表分区 >
        self.f_msgsend = tk.Frame(self.window2,height = 400,width = 700, bg='#DDFFE7') #创建<发送消息分区 >
        self.f_floor = tk.Frame(self.window2,height = 90,width = 700, bg='#DDFFE7')   #创建<按钮分区>
        self.f_right = tk.Frame(self.window2, height = 90,width = 700,  bg='#DDFFE7')   #创建《功能分区>


        '''widgets'''
        self.txt_msglist = tk.Text(self.f_msglist, bg='#DDFFE7') #消息列表分区中创建文本控件
        self.txt_msglist.tag_config('green',foreground = 'blue') #消息列表分区中创建标签
        self.txt_msgsend = tk.Text(self.f_msgsend, bg='#DDFFE7') #发送消息分区中创建文本控件



        def chat_looping():
            while True:
                self.system_msg = client.proc()
                client.output()
                time.sleep(CHAT_WAIT)

                if self.system_msg != '':
                    self.txt_msglist.insert(tk.END, self.system_msg + '\n')



        reading_thread = threading.Thread(target = chat_looping)
        reading_thread.daemon = True
        reading_thread.start()


        def cancel_msg():
            self.txt_msgsend.delete('0.0',tk.END)


        def send_msg():

            self.msg = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())+'\n'
            self.txt_msglist.insert(tk.END,self.msg,'green')
            self.txt_msglist.insert(tk.END,self.txt_msgsend.get('0.0',tk.END))
            self.msg_content = str(self.txt_msgsend.get('0.0',tk.END)[:-1])
            client.console_input.append(self.msg_content)
            self.txt_msgsend.delete('0.0',tk.END)

        def get_time():
            client.console_input.append('time')

        def find_who():
            client.console_input.append('who')

        def chat_with():
            self.window3 = tk.Tk()
            self.window3.geometry("500x200")
            self.window3.title("Select a person")
            self.label_p = tk.Label(self.window3, text='Who do you want to chat with?', bg='#DDFFE7', font="Monsterrat 18").place(relx=0.25, rely=0.2)
            self.chat_name = tk.StringVar()
            self.chat_name.set("")
            self.entry_p = tk.Entry(self.window3,textvariable=self.chat_name).place(relx=0.29, rely=0.4)
            self.button_p = tk.Button(self.window3, text='Confirm', font="Times 18", command=chat_confirm).place(relx=0.42, rely=0.7)
            self.window3.mainloop()
        def chat_confirm():
            self.window3.destroy()
            client.console_input.append('c'+ self.chat_name.get())


        def search_term():
            self.window4 = tk.Tk()
            self.window4.geometry("500x200")
            self.window4.title("Select a term")
            self.label_s = tk.Label(self.window4, text='What word do you want to search?', bg='#DDFFE7', font="Monsterrat 18").place(
                relx=0.25, rely=0.2)
            self.search_term = tk.StringVar()
            self.search_term.set("")
            self.entry_s = tk.Entry(self.window4, textvariable=self.search_term).place(relx=0.29, rely=0.4)
            self.button_s = tk.Button(self.window4, text='Confirm', font="Monsterrat 18", command=search_confirm).place(relx=0.42,
                                                                                                     rely=0.7)
            self.window4.mainloop()
        def search_confirm():
            self.window4.destroy()
            client.console_input.append('?'+ self.search_term.get())
        def get_son():
            self.window5 = tk.Tk()
            self.window5.geometry("500x200")
            self.window5.title("Select a sonnet")
            self.label_n = tk.Label(self.window5, text='Which sonnet do you want to get?', bg='#DDFFE7', font="Monsterrat 18").place(
                relx=0.25, rely=0.2)
            self.sonnet_num = tk.StringVar()
            self.sonnet_num.set("")
            self.entry_n = tk.Entry(self.window5, textvariable=self.sonnet_num).place(relx=0.29, rely=0.4)
            self.button_n = tk.Button(self.window5, text='Confirm', font="Times 18", command=sonnet_confirm).place(relx=0.42,rely=0.7)
        def sonnet_confirm():
            self.window5.destroy()
            client.console_input.append('p' + self.sonnet_num.get())

        def quit_sys():
            client.console_input.append('q')
            self.window2.destroy()

        self.button_send = tk.Button(self.f_floor,text = 'Send',font="Monsterrat 15" ,activeforeground = "#3a93f8", height= 3, width=10,command = send_msg)
        self.button_cancel = tk.Button(self.f_floor,text = 'Cancel',font="Monsterrat 15", activeforeground = "#3a93f8", height= 3, width=10,command = cancel_msg) #按钮分区中创建按钮并绑定发送消息函数
        self.button_time = tk.Button(self.f_right, text='Time',font="Monsterrat 15" ,activeforeground = "#3a93f8", height= 2, width=10, command = get_time)
        self.button_who = tk.Button(self.f_right, text='Find',font="Monsterrat 15" ,activeforeground = "#3a93f8", height= 2, width=10, command = find_who)
        self.button_chat = tk.Button(self.f_right, text='Chat',font="Monsterrat 15" ,activeforeground = "#3a93f8", height= 2, width=10, command = chat_with)
        self.button_search = tk.Button(self.f_right, text='Search',font="Monsterrat 15" ,activeforeground = "#3a93f8", height= 2, width=10, command = search_term)
        self.button_sonnet = tk.Button(self.f_right, text='Sonnet',font="Monsterrat 15" ,activeforeground = "#3a93f8", height= 2, width=10, command = get_son)
        self.button_quit = tk.Button(self.f_right, text='Quit',font="Monsterrat 15", activeforeground = "#3a93f8", height= 2, width=10, command = quit_sys)
        # self.instruction = tk.Label(self.f_right,text= "\nChoose one of the following commands\n \
        # Time: calendar time in the system\n \
        # Find: to find out who else are there\n \
        # Chat: to connect to the peer and chat\n \
        # Search: to search one term in your chat logs\n \
        # Sonnet: to get one sonnet\n \
        # Quit: to leave the chat system\n\n",font="Monsterrat 13 italic",bg="white", fg='#3a93f8').place(relx=0.05, rely=0.675, relwidth=0.9)
        #
        '''分区布局'''

        self.f_msglist.grid(row = 1,column = 0 ) #msgs
        self.f_msgsend.grid(row = 2,column = 0)  #send area
        self.f_floor.grid(row = 3,column = 0)    #buttons
        self.f_right.grid(row=0, column=0)      #funtions

        self.txt_msglist.grid()  #消息列表文本控件加载
        self.txt_msgsend.grid()  #消息发送文本控件加载
        self.button_send.place(relx=0.3,rely = 0.2),#sticky = W)   #发送按钮控件加载
        self.button_cancel.place(relx=0.6,rely = 0.2)#取消按钮控件加载
        self.button_time.place(relx=0.05,rely = 0.3)
        self.button_who.place(relx=0.2,rely = 0.3)
        self.button_chat.place(relx=0.35,rely = 0.3)
        self.button_search.place(relx=0.5,rely = 0.3)
        self.button_sonnet.place(relx=0.65,rely = 0.3)
        self.button_quit.place(relx=0.8,rely = 0.3)
     #   self.instruction.place(relx=0.37,rely = 0.7)
    #    self.instruction.pack()

    #    print(162)

        self.window2.mainloop()



gui = GUI()
