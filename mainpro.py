from tkinter import *
from tkinter import messagebox as msg
import dbcon as db
from tkinter.simpledialog import askstring
from datetime import datetime as dt
from tkinter import ttk   
root=Tk()
root.state('zoomed')
root.update()
root.configure(bg='powder blue')
header=Label(root,bg='powder blue',fg='brown',text="Bank Automation System",font=('',40,'bold'))
header.pack()




def register(root,u,p,e,m):
    if(len(u)==0 or len(p)==0 or len(e)==0 or len(m)==0):
        msg.showwarning('Invalid',"please fill all fields")            
        return
    if('@' not in e):
        msg.showwarning('Invalid',"invalid email")
        return
    con=db.getCon()
    cur=con.cursor()
    cur.execute("select max(aco) from useraccount")
    row=cur.fetchone()
    newacno=row[0]+1
    cur.execute("insert into useraccount values(%s,%s,%s,%s,%s,%s,%s)",(u,p,e,m,newacno,1000,'saving'))
    con.commit()
    con.close()
    msg.showinfo('Congratulation',f"We have opend account with Account no:{newacno}")
    homeinfo(root)
def login(u,p,cb):
    if(len(u)==0 or len(p)==0):
        msg.showinfo('Invalid',"Username/Password can't be empty")
    elif(cb=='---select---'):
        msg.showinfo('Invalid',"Please select a type")
    else:
        if(cb=='Account Holder'):
            con=db.getCon()
            cur=con.cursor()
            cur.execute("select * from useraccount where username=%s and password=%s",(u,p))
            row=cur.fetchone()
            if(row!=None):
                msg.showinfo('Welcome',"Valid user")
                welcome(root,row)
            else:
                msg.showerror('Invalid',"Invalid user")
            con.commit()
            con.close()
        else:
            if(u=='admin' and p=='admin'):
                msg.showinfo('Welcome',"Welcome Admin")
                welcomeAdmin(root)
            else:
                msg.showerror('Invalid',"You are not an admin")    
def reset(e1,e2,e3=None,e4=None):
    l1=len(e1.get())
    l2=len(e2.get())
    e1.delete(0,l1)
    e2.delete(0,l2)
    if(e3!=None and e4!=None):
        l3=len(e3.get())
        l4=len(e4.get())
        e3.delete(0,l3)
        e4.delete(0,l4)

def signup(root):
    frmHome=Frame(root,bg='powder blue')
    l1=Label(frmHome,text='Username:',font=('',15,'bold'),bg='powder blue')
    l1.grid(row=0,column=2,sticky='e',ipadx=20,pady=15,padx=20)
    e1=Entry(frmHome,font=('',15,'bold'),bd=5)
    e1.grid(row=0,column=3)
    l2=Label(frmHome,text='Password:',font=('',15,'bold'),bg='powder blue')
    l2.grid(row=1,column=2)
    e2=Entry(frmHome,font=('',15,'bold'),bd=5,show='*')
    e2.grid(row=1,column=3)
    l3=Label(frmHome,text='Email:',font=('',15,'bold'),bg='powder blue')
    l3.grid(row=2,column=2,sticky='e',ipadx=20,pady=15,padx=20)
    e3=Entry(frmHome,font=('',15,'bold'),bd=5)
    e3.grid(row=2,column=3)


    l4=Label(frmHome,text='Mobile:',font=('',15,'bold'),bg='powder blue')
    l4.grid(row=3,column=2,sticky='e',ipadx=20,pady=15,padx=20)
    e4=Entry(frmHome,font=('',15,'bold'),bd=5)
    e4.grid(row=3,column=3)
    
    b1=Button(frmHome,command=lambda:register(root,e1.get(),e2.get(),e3.get(),e4.get()),text='submit',bd=5,width=10)
    b2=Button(frmHome,command=lambda:reset(e1,e2,e3,e4),text='reset',bd=5,width=10)
    
    b1.grid(row=4,column=2,pady=15,sticky='e')
    b2.grid(row=4,column=3)
    b3=Button(frmHome,command=lambda:logout(root),text='back',bd=5,width=10)
    b3.grid(row=4,column=4)
    frmHome.place(x=170,y=115,height=root.winfo_height(),width=root.winfo_width())

    
def homeinfo(root):
    frmHome=Frame(root,bg='powder blue')
    l1=Label(frmHome,text='Username:',font=('',15,'bold'),bg='powder blue')
    l1.grid(row=0,column=2,sticky='e',ipadx=20,pady=15,padx=20)
    e1=Entry(frmHome,font=('',15,'bold'),bd=5)
    e1.grid(row=0,column=3)
    l2=Label(frmHome,text='Password:',font=('',15,'bold'),bg='powder blue')
    l2.grid(row=1,column=2)
    e2=Entry(frmHome,font=('',15,'bold'),bd=5,show='*')
    e2.grid(row=1,column=3)

    l3=Label(frmHome,text='User Type:',font=('',15,'bold'),bg='powder blue')
    l3.grid(row=2,column=2)
    cb=ttk.Combobox(frmHome,font=('',13,'bold'),values=['---select---','Account Holder','Admin'])
    cb.current(0)
    cb.grid(row=2,column=3,pady=10)
    

    b1=Button(frmHome,command=lambda:login(e1.get(),e2.get(),cb.get()),text='submit',bd=5,width=10)
    b2=Button(frmHome,command=lambda:reset(e1,e2),text='reset',bd=5,width=10)
    b3=Button(frmHome,command=lambda:signup(root),text='signup',bd=5,width=20)

    b1.grid(row=3,column=2,pady=15,sticky='e')
    b2.grid(row=3,column=3)
    b3.place(x=150,y=220)
    frmHome.place(x=170,y=115,height=root.winfo_height(),width=root.winfo_width())

def logout(root):
    homeinfo(root)

def withdraw(row):
    amt = int(askstring('Withdrwal', 'Enter Amount:'))
    con=db.getCon()
    cur=con.cursor()
    cur.execute("select * from useraccount where aco=%s",(row[4],))
    row=cur.fetchone()
    con.close()
    if(row[5]>=amt):
        con=db.getCon()
        cur=con.cursor()
        updatebal=row[5]-amt
        cur.execute("update useraccount set bal=%s where aco=%s",(updatebal,row[4]))
        cur.execute("insert into txnhistory values(%s,%s,%s,%s,%s)",(row[4],dt.now(),amt,'Debit',updatebal))
        con.commit()
        con.close()
        msg.showinfo('Success',f"Txn Success,Updated Bal:{updatebal}")
        
    else:
        msg.showerror('Fail',"Insufficient bal")
        
def deposit(row):
    amt = int(askstring('Deposit', 'Enter Amount:'))
    con=db.getCon()
    cur=con.cursor()
    cur.execute("select * from useraccount where aco=%s",(row[4],))
    row=cur.fetchone()
    con.close()
    if(amt>=0):
        con=db.getCon()
        cur=con.cursor()
        print('aaa',type(amt),type(row[5]))
        updatebal=row[5]+amt
        
        cur.execute("update useraccount set bal=%s where aco=%s",(updatebal,row[4]))
        cur.execute("insert into txnhistory values(%s,%s,%s,%s,%s)",(row[4],dt.now(),amt,'Credit',updatebal))
        con.commit()
        con.close()
        msg.showinfo('Success',f"Txn Success,Updated Bal:{updatebal}")
        
    else:
        msg.showerror('Fail',"Invalid amount")

def txn(row):
    con=db.getCon()
    cur=con.cursor()
    cur.execute("select * from txnhistory where aco=%s",(row[4],))
    data="Acn  \tdate \t\tamt   type  bal\n"
    for row in cur:
        for r in row:
            data=data+str(r)+"  "
        data=data+"\n"    
    msg.showinfo('Txn History',data)
    
    con.close()
    

def txnAdmin():
    con=db.getCon()
    cur=con.cursor()
    cur.execute("select * from txnhistory")
    data="Acn  \tdate \t\tamt   type  bal\n"
    for row in cur:
        for r in row:
            data=data+str(r)+"  "
        data=data+"\n"    
    msg.showinfo('Txn History',data)
    
    con.close()
    


def checkbal(acno):
        con=db.getCon()
        cur=con.cursor()
        cur.execute("select * from useraccount where aco=%s",(acno,))
        row=cur.fetchone()
        msg.showinfo('Balance',f"Your Balance:{row[5]}")
        con.commit()
        con.close()
    
def welcome(root,row):
    frmHome=Frame(root,bg='powder blue')
    l1=Label(frmHome,text=f'Welcome:{row[0]}',font=('',15,'bold'),bg='powder blue')
    l1.place(x=0,y=0)
    b1=Button(frmHome,width=10,command=lambda:checkbal(row[4]),text='check bal',bd=5)
    b2=Button(frmHome,width=10,command=lambda:withdraw(row),text='withdraw',bd=5)
    b3=Button(frmHome,width=10,command=lambda:deposit(row),text='deposit',bd=5)
    b4=Button(frmHome,width=10,command=lambda:txn(row),text='view txn',bd=5)
    b5=Button(frmHome,width=10,command=lambda:logout(root),text='logout',bd=5)
    b1.place(x=200,y=50)
    b2.place(x=200,y=100)
    b3.place(x=200,y=150)
    b4.place(x=200,y=200)
    
    b5.place(x=400,y=0)
    
    frmHome.place(x=170,y=115,height=root.winfo_height(),width=root.winfo_width())


def welcomeAdmin(root):
    frmHome=Frame(root,bg='powder blue')
    l1=Label(frmHome,text='Welcome:Admin',font=('',15,'bold'),bg='powder blue')
    l1.place(x=0,y=0)
    b4=Button(frmHome,width=10,command=lambda:txnAdmin(),text='view txn',bd=5)
    b5=Button(frmHome,width=10,command=lambda:logout(root),text='logout',bd=5)
    b4.place(x=200,y=100)
    
    b5.place(x=400,y=0)
    
    frmHome.place(x=170,y=115,height=root.winfo_height(),width=root.winfo_width())

homeinfo(root)    
root.mainloop()

