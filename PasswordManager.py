from tkinter import *
from tkinter import messagebox
from PIL import Image,ImageTk
import webbrowser
import random
from string import *
import mysql.connector as sqltor
from  cryptography.fernet import Fernet



def add(user):
    tn=user
    def adden():
        if not ename.get():
            messagebox.showinfo('Error','Entry should be given')
        else:        
            cursor.execute("show tables like '{une}'".format(une=tn))
            r=cursor.fetchone()
            if not r:
                cursor.execute(f"CREATE TABLE {tn} (entryname TEXT NOT NULL, username TEXT, passwd TEXT, comment TEXT, PRIMARY KEY (entryname(255)))")
            insert_sql = f"""
            INSERT INTO {tn}  
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(insert_sql,(ename.get(),u.get(),p.get(),com.get('1.0',END).strip()))
            con.commit()
            ename.delete(0,END)
            u.delete(0, END)
            p.delete(0, END)
            com.delete('1.0',END)
            messagebox.showinfo('','Entry Added')


    addentry_frame=Frame(features_win,bg='lightgreen',width=1250,height=650)
    addentry_frame.place(x=200,y=0,relheight=1,relwidth=1)
    Label(addentry_frame,anchor=CENTER,text='Entry Name',cursor='xterm',bg='white',fg='black',font=('Times',20,'bold')).place(x=600,y=60)
    ename=Entry(addentry_frame,relief='groove',width=25,bg='white',font=('calibre',16))
    ename.place(x=525,y=100)
    Label(addentry_frame,anchor=CENTER,text='Username',cursor='xterm',bg='white',fg='black',font=('Times',20,'bold')).place(x=600,y=170)
    u=Entry(addentry_frame,relief='groove',width=25,bg='white',font=('calibre',16))
    u.place(x=525,y=210)
    Label(addentry_frame,anchor=CENTER,text='Password',cursor='xterm',bg='white',fg='black',font=('Times',20,'bold')).place(x=600,y=270)
    p=Entry(addentry_frame,relief='groove',width=25,bg='white',font=('calibre',16))
    p.place(x=525,y=310)
    Label(addentry_frame,anchor=CENTER,text='#Comments',cursor='xterm',bg='white',fg='black',font=('Times',20,'bold')).place(x=600,y=360)
    com=Text(addentry_frame,cursor='xterm',font=('calibre',16,'italic'),width=25,height=5)
    com.place(x=525,y=400)
    addentry=Button(addentry_frame,width=10,text='ADD',bg='pink',font=('System',16,'bold'),command=adden)
    addentry.place(x=600,y=550)
        

def delete(en,us):
    cursor.execute("delete  from {} where entryname = '{}'".format(us,en))
    con.commit()
    hideframes()
    view(us)

    
def save(en,us,ename,u,p,com):
    cursor.execute("delete  from {} where entryname = '{}'".format(us,en))
    
    cursor.execute("insert into {} values('{}','{}','{}','{}')".format(us,ename.get(),u.get(),p.get(),com.get('1.0',END).strip()))
    con.commit()
    hideframes()
    view(us)

    


def buttonview(entryname,user):
    en,us=entryname,user
    cursor.execute("select * from {} where entryname = '{}'".format(us,en))
    t=cursor.fetchone()
    hideframes()
    frame=Frame(features_win,bg='lightgreen',width=1250,height=650)
    frame.place(x=200,y=0,relheight=1,relwidth=1)
    Label(frame,anchor=CENTER,text='Entry Name',cursor='xterm',bg='white',fg='black',font=('Times',20,'bold')).place(x=600,y=60)
    ename=Entry(frame,relief='groove',width=25,bg='white',font=('calibre',16))
    ename.insert(0,t[0])
    ename.place(x=525,y=100)
    Label(frame,anchor=CENTER,text='Username',cursor='xterm',bg='white',fg='black',font=('Times',20,'bold')).place(x=600,y=170)
    u=Entry(frame,relief='groove',width=25,bg='white',font=('calibre',16))
    u.insert(0,t[1])
    u.place(x=525,y=210)
    Label(frame,anchor=CENTER,text='Password',cursor='xterm',bg='white',fg='black',font=('Times',20,'bold')).place(x=600,y=270)
    p=Entry(frame,relief='groove',width=25,bg='white',font=('calibre',16))
    p.insert(0,t[2])
    p.place(x=525,y=310)
    Label(frame,anchor=CENTER,text='#Comments',cursor='xterm',bg='white',fg='black',font=('Times',20,'bold')).place(x=600,y=360)
    com=Text(frame,cursor='xterm',font=('calibre',16,'italic'),width=25,height=5)
    com.place(x=525,y=400)
    com.insert('1.0',t[3])
    addentry=Button(frame,width=10,text='DELETE',bg='pink',font=('System',16,'bold'),command=lambda:delete(en,us))
    addentry.place(x=550,y=550)
    addentry=Button(frame,width=10,text='SAVE',bg='pink',font=('System',16,'bold'),command=lambda:save(en,us,ename,u,p,com))
    addentry.place(x=680,y=550)
    
    
    
        

def view(username):
    
    
    user =username
    def on_canvas_configure(event):
        mycanvas.configure(scrollregion=mycanvas.bbox("all"))
    def on_frame_configure(event):
        mycanvas.configure(scrollregion=mycanvas.bbox("all"))
    
    mycanvas=Canvas(features_win,width=1250,height=950,bg='lightgreen')
    mycanvas.place(x=200,y=0,relheight=1,relwidth=1)
    scroll=Scrollbar(features_win,orient='vertical',command=mycanvas.yview)
    scroll.pack(side=RIGHT,fill='y')
    mycanvas.configure(yscrollcommand=scroll.set)
    mycanvas.bind('<Configure>',on_canvas_configure)
    scrollable_frame =Frame(mycanvas,bg='orange')
    mycanvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    scrollable_frame.bind("<Configure>", on_frame_configure)
    cursor.execute("show tables like '{une}'".format(une=user))
    r=cursor.fetchone()
    if  r:
        cursor.execute('select entryname from {us}'.format(us=user))
        for i in cursor.fetchall():
            button = Button(scrollable_frame, text=i[0],width=185,height=10,bg='pink',font=('Times',10),command=lambda:buttonview(i[0],user))
            button.pack(pady=5, padx=5, anchor='w',side='top',fill='x')
        

    
def generate():
    
    def gene(charlen,nolen,symbollen):
        password=''
        length=charlen+nolen+symbollen
        c=ascii_letters
        n=digits
        s=punctuation
        while(length>0):
            
            ps=random.choice(c+n+s)
            if ps in c and charlen>0:
                charlen-=1
                length-=1
                password+=ps
            if ps in n and nolen>0:
                nolen-=1
                length-=1
                password+=ps
            if ps in s and symbollen>0:
                symbollen-=1
                length-=1
                password+=ps
        return password
    
    def uppasswd(charlen,nolen,symbollen):
        
        new_password = gene(int(charlen),int(nolen),int(symbollen))
        entry_var.set(new_password)
    
    generate_frame=Frame(features_win,bg='lightgreen',width=1250,height=650)
    generate_frame.place(x=200,y=0,relheight=1,relwidth=1)
    Label(generate_frame,text='PASSWORD GENERATOR',cursor='xterm',bg='lightgreen',fg='black',font=('Times',25,'bold')).pack(side='top')
    Label(generate_frame,text='Number of alphabets required in you password: ',cursor='xterm',bg='lightgreen',fg='black',font=('Times',20,'bold'),padx=15,pady=15).place(x=50,y=250)
    charlen=Entry(generate_frame,width=7,bg='white',font=('calibre',12))
    charlen.place(x=710,y=270)
    Label(generate_frame,text='Number of numbers required in you password: ',cursor='xterm',bg='lightgreen',fg='black',font=('Times',20,'bold'),padx=15,pady=15).place(x=50,y=300)
    nolen=Entry(generate_frame,width=7,bg='white',font=('calibre',12))
    nolen.place(x=710,y=320)
    Label(generate_frame,text='Number of special symbols required in you password: ',cursor='xterm',bg='lightgreen',fg='black',font=('Times',20,'bold'),padx=15,pady=15).place(x=50,y=350)
    symbollen=Entry(generate_frame,width=7,bg='white',font=('calibre',12))
    symbollen.place(x=710,y=370)
    entry_var=StringVar()
    passwd=Entry(generate_frame,width=15,bg='white',font=('calibre',16),state='readonly',textvariable=entry_var)
    passwd.place(x=565,y=450)
    gen=Button(generate_frame,width=10,text='Generate',font=('System',14),command=lambda:uppasswd(charlen.get(),nolen.get(),symbollen.get()))
    gen.place(x=600,y=490)
    
          
        
    
def urls(username):
    def go_to_site(link):
        webbrowser.open(link)
    def delete_link(index):
        with open(r'urls.txt', 'r') as file:
                lines = file.readlines()

        with open(r'urls.txt', 'w') as file:
            for line in lines:
                u=line.rstrip().split("|")
                if u[1]!= links[index]:
                    file.write(u[0]+'|'+u[1]+'\n')
        links.remove(links[index])


        update_links_display()
    
    def display():
        with open (r'urls.txt','r') as f:
            r=f.readlines()
            for i in r:
                u=i.rstrip().split('|')
                if u[0]==username:
                    links.append(u[1])
    
    def update_links_display():
        for widget in links_frame.winfo_children():
            widget.destroy()
        for i, link in enumerate(links):
            link_label = Label(links_frame,font=("System,14"), text=link, fg="blue",bg='pink', cursor="hand2", wraplength=300)
            link_label.grid(row=i, column=0,padx=5,pady=5,sticky="w")
            go_button = Button(links_frame, text="Go to Site", command=lambda l=link: go_to_site(l))
            go_button.grid(row=i, column=1,padx=5,pady=5)
            delete_button = Button(links_frame, text="Delete", command=lambda i=i: delete_link(i))
            delete_button.grid(row=i, column=2,padx=5,pady=5)
        canvas.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

        
    def add_link():
        link = link_entry.get()
        if link:
            with open (r'urls.txt','a+') as f:
                f.write(username+'|'+link+'\n')
            links.append(link)
            update_links_display()
            link_entry.delete(0, END)
    
    links=[]
    display()
    urls_frame=Frame(features_win,bg='lightgreen',width=1250,height=650)
    urls_frame.place(x=200,y=0,relheight=1,relwidth=1)
    addframe=Frame(urls_frame,bg='lightgreen',borderwidth=0,border=0,highlightthickness=0)
    addframe.pack(side=TOP)
    link_entry =Entry(addframe,width=50,font=('System',14))
    link_entry.pack( side=TOP,anchor=CENTER,padx=20,pady=10)
    add_button = Button(addframe,height=1,text="Add Link",width=10,command=add_link)
    add_button.pack(pady=10)
    canvas = Canvas(urls_frame, borderwidth=0,bg='lightgreen',border=0,highlightthickness=0)
    scrollbar = Scrollbar(features_win, orient="vertical", command=canvas.yview)
    links_frame = Frame(canvas,bg='lightgreen')
    canvas.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    canvas.create_window((500, 0), window=links_frame, anchor="nw")
    update_links_display()

    
            
            
                
def hideframes():
    for i in features_win.winfo_children():
        if i!=side_bar and i!=toggle_button:
            i.destroy()
        


def hideindicate():
    addent_indicate.configure(bg='yellow')
    view_indicate.configure(bg='yellow')
    genpass_indicate.configure(bg='yellow')
    url_indicate.configure(bg='yellow')

def indicate(lb,user):
    hideindicate()
    lb.configure(bg='darkblue')
    hideframes()
    if lb==addent_indicate:
        add(user)
    elif lb==view_indicate:
        view(user)
    elif lb==genpass_indicate:
        generate()
    elif lb==url_indicate:
        urls(user)


sidebar_visible=False
def toggle(side_bar):
    global sidebar_visible
    if sidebar_visible:
        side_bar.place_forget()
    else:
        side_bar.place(x=0,y=0,relheight=1,width=200)
    sidebar_visible=not sidebar_visible


def features(user):
    global features_win
    features_win=Tk()
    features_win.geometry('1250x650')
    features_win.configure(bg='lightgreen')
    features_win.title('Password Manager')
    global side_bar
    side_bar=Frame(features_win,bg='yellow')
    addentry=Button(side_bar,bd=0,highlightthickness=0,bg='yellow',width=10,text='Add Entry',font=('System',14,'bold'),fg='darkblue')
    addentry.pack(pady=30)
    global addent_indicate
    addent_indicate=Label(side_bar,text='',width=1,height=1,bg='yellow')
    addent_indicate.place(x=0,y=33)
    addentry.configure(command=lambda:indicate(addent_indicate,user))
    
    viewentry=Button(side_bar,bd=0,highlightthickness=0,bg='yellow',width=10,text='View',font=('System',14,'bold'),fg='darkblue')
    viewentry.pack(pady=30)
    global view_indicate
    view_indicate=Label(side_bar,text='',width=1,height=1,bg='yellow')
    view_indicate.place(x=0,y=123)
    viewentry.configure(command=lambda:indicate(view_indicate,user))
    
    genpass=Button(side_bar,bd=0,highlightthickness=0,bg='yellow',width=10,height=2,text='Generate\nPassword',font=('System',14,'bold'),fg='darkblue')
    genpass.pack(pady=30)
    global genpass_indicate
    genpass_indicate=Label(side_bar,text='',width=1,height=1,bg='yellow')
    genpass_indicate.place(x=0,y=220)
    genpass.configure(command=lambda:indicate(genpass_indicate,user))
    
    urlbutton=Button(side_bar,bd=0,highlightthickness=0,bg='yellow',width=10,text='Bookmark',font=('System',14,'bold'),fg='darkblue')
    urlbutton.pack(pady=30)
    global url_indicate
    url_indicate=Label(side_bar,text='',width=1,height=1,bg='yellow')
    url_indicate.place(x=0,y=320)
    urlbutton.configure(command=lambda:indicate(url_indicate,user))
    
    global toggle_button
    toggle_button=Button(features_win,width=5,text='MENU',font=('System',11,'bold'),command=lambda:toggle(side_bar))
    toggle_button.place(x=0,y=0)
    about_frame=Frame(features_win,bg='lightgreen',height=650,width=950)
    about_frame.place(x=300,y=0)
    about=Text(about_frame,bg='lightgreen',bd=0,highlightthickness=0,wrap='word',fg='black',height=150,width=87,font=('Helvetica',14),cursor='xterm',pady=4)
    about.place(x=5,y=350)
    about_text=('                       A password manager is an application that can generate, store and manage all of your account credentials\
   (usernames and passwords) and their associated login portals (websites, URLs) in a secure, central location (“vault”).\
   The vault is encrypted, so your passwords are never stored in clear-text anywhere. The benefit of using such an\
   application is that each website and account can have a unique, truly random, long password, and you don’t have to\
   remember it – the password manager can remember them for you, and even help you avoid typing your passwords into faked\
   or insecure websites. There is some risk in storing “all the keys to the castle” in one location, but overall, there is\
   a net benefit when you use a password manager configured securely,and as it’s intended.')
    about.insert('1.0',about_text)
    about.configure(state='disabled')
    image=Image.open(r'C:\Users\R.SENTHIL KUMAR\OneDrive\Pictures\Screenshots\Screenshot 2024-07-27 081757.png')
    image=image.resize((400,250))
    photo=ImageTk.PhotoImage(image)
    passimag=Label(about_frame,image=photo,bg='black')
    passimag.place(x=280,y=50)
    features_win.mainloop()
    

def encrypt_password(password):
    return cipher_suite.encrypt(password.encode())

def decrypt_password(encrypted_password):
    return cipher_suite.decrypt(encrypted_password).decode()
            



def login(username,password):
    user = username
    paswd = password
    with open(r"accounts.txt", "r") as mainfile:
        accdata = mainfile.readlines()
        for i in accdata:
            us, encrypted_pas = i.rstrip().split('|')
            if us == user.rstrip():
                decrypted_pas = decrypt_password(encrypted_pas.encode())
                if decrypted_pas == paswd.rstrip():
                    loginwin.destroy()
                    features(user)
                    break
        else:
            messagebox.showinfo('Error', 'Invalid account')            
            
    
                
def createnew(un, ps, win):
    encrypted_password = encrypt_password(ps)
    with open(r"accounts.txt", "a+") as accfile:
        data = accfile.read()
        if (un + '|') in data:
            messagebox.showinfo('Error', 'Account with username already exists')
        else:
            accfile.write(un + '|' + encrypted_password.decode() + '\n')
            messagebox.showinfo('Success', 'Account added!')
            logframe()
        

def addacc():
    for i in loginwin.winfo_children():
        i.destroy()
    createwin=Frame(loginwin,bg='lightgreen',width=1250,height=650)
    createwin.place(x=0,y=0,relheight=1,relwidth=1)
    Label(createwin,anchor=CENTER,text='Username',cursor='xterm',bg='lightgreen',fg='black',font=('Times',14,'bold')).place(x=660,y=270)
    u=Entry(createwin,width=30,bg='white',font=('calibre',12))
    u.place(x=625,y=300)
    Label(createwin,anchor=CENTER,text='Password',cursor='xterm',bg='lightgreen',fg='black',font=('Times',14,'bold')).place(x=660,y=325)
    p=Entry(createwin,width=30,bg='white',font=('calibre',12),show='*')
    p.place(x=625,y=355)
    signup=Button(createwin,width=10,text='signup',font=('System',14),command=lambda:createnew(u.get(),p.get(),createwin))
    signup.place(x=695,y=395)
    createwin.mainloop()




def logframe():
    loginframe=Frame(loginwin,bg='lightgreen',width=1250,height=650)
    loginframe.place(x=0,y=0,relheight=1,relwidth=1)
    #title
    label=Label(loginframe,anchor=CENTER,text='Password Manager',cursor='xterm',bg='lightgreen',fg='red',font=('Times',30,'bold'))
    label.place(x=620,y=0)

    #login account Entries
    Label(loginframe,anchor=CENTER,text='Username',cursor='xterm',bg='lightgreen',fg='black',font=('Times',20,'bold')).place(x=600,y=210)
    username=Entry(loginframe,width=30,bg='white',font=('calibre',12))
    username.place(x=730,y=222)
    Label(loginframe,anchor=CENTER,text='Password',cursor='xterm',bg='lightgreen',fg='black',font=('Times',20,'bold')).place(x=600,y=255)
    password=Entry(loginframe,width=30,bg='white',font=('calibre',12),show='*')
    password.place(x=730,y=267)
    log=Button(loginframe,width=10,text='login',font=('System',14))
    log.place(x=720,y=320)
    log.configure(command=lambda:login(username.get(),password.get()))
    Label(loginframe,anchor=CENTER,text='want to create new account',cursor='xterm',bg='lightgreen',fg='black',font=('Times',15,'bold')).place(x=600,y=360)
    create=Button(loginframe,width=5,text='create',font=('System',11),command=addacc)
    create.place(x=840,y=360)




con=sqltor.connect(host='<hostname>',user='<username>',passwd='<password>',database='<database_name>',port='<portno.>')

cursor=con.cursor()

cursor.execute("select * from pkey")
pkey=cursor.fetchall()
s=pkey[0][0]

key = s.encode()
cipher_suite = Fernet(key)

   
loginwin=Tk()
loginwin.geometry('1250x650')
loginwin.configure(bg='lightgreen')
loginwin.title('Password Manager')
logframe()

loginwin.mainloop()


            
        

    
    
    



