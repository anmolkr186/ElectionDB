from django.shortcuts import render, redirect
from django.http import HttpResponse
import pyodbc
import threading
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from datetime import datetime, timedelta
from django.contrib import messages
from django.views.generic import TemplateView
from django.http import JsonResponse
import json
import copy
# from chartjs.views.lines import BaseLineChartView


grapgquery = ["SELECT vote, COUNT(*) FROM voterTable GROUP BY vote;",
              "Select Category , COUNT(*) from Booth_Level_Officer Group by Category;", "select Religion,COUNT(*) from Voter group by Religion;"]
# database connection

cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=dbms54.database.windows.net,1433',
                      user='dbms54@dbms54.database.windows.net', password='qwertyuiop@123', database='DMBSProj')
cursor = cnxn.cursor()
# multithreading
lock = threading.Lock()

#username : demouser
#password : demopassword


def getgraph():
    lock.acquire()
    cursor.execute(grapgquery[0])
    data = cursor.fetchall()
    val1 = []
    data1 = []
    for row in data:
        val1.append(row[0])
        data1.append(row[1])
    cursor.execute(grapgquery[1])
    data = cursor.fetchall()
    val2 = []
    data2 = []
    for row in data:
        val2.append(row[0])
        data2.append(row[1])
    cursor.execute(grapgquery[2])
    data = cursor.fetchall()
    val3 = []
    data3 = []
    for row in data:
        val3.append(row[0])
        data3.append(row[1])
    lock.release()
    return val1, data1, data2, val2, data3, val3


table1 = []
table2 = []
table3 = []


def tablequery():
    query = "Select Voter_ID,Name,Age,City,Booth_Number from Voter;"
    prt = ["Voter_ID", "Name", "Age", "City", "Booth_Number"]
    cursor.execute(query)
    rows = cursor.fetchall()
    data = []
    data.append(copy.deepcopy(prt))
    size = len(prt)
    for i in rows:
        data.append(i)
    print(data)
    table1 = copy.deepcopy(data)
    query = "SELECT vote, COUNT(*) FROM voterTable GROUP BY vote;"
    prt = ["vote", "total "]
    cursor.execute(query)
    rows = cursor.fetchall()
    data = []
    data.append(copy.deepcopy(prt))
    size = len(prt)
    for i in rows:
        data.append(i)
    print(data)
    table2 = copy.deepcopy(data)
    query = "Select * from Booth_Level_Officer;"
    prt = ["offId", "Name", "Category", "BoothNo", "Address", "Contact"]
    cursor.execute(query)
    rows = cursor.fetchall()
    data = []
    data.append(copy.deepcopy(prt))
    size = len(prt)
    for i in rows:
        data.append(i)
    print(data)
    table3 = copy.deepcopy(data)


def updater(request):
    print("here in updateer ")
    val1, data1, data2, val2, data3, val3 = getgraph()
    tablequery()
    return JsonResponse({"val1": val1, "data1": data1, "data2": data2, "val2": val2, "data3": data3, "val3": val3, "table1": table1, "table2": table2, "table3": table3}, status=200)


def index(request):
    val1, data1, data2, val2, data3, val3 = getgraph()
    print(val2, data2)
    print(val3, data3)
    tablequery()
    return render(request, 'index.html', {"val1": val1, "data1": data1, "data2": data2, "val2": val2, "data3": data3, "val3": val3, "table1": table1, "table2": table2, "table3": table3})


def login(request):
    print("hererereererererererererererererererer")
    username = request.POST['username']
    password = request.POST['password']
    lock.acquire()
    cursor.execute(
        "SELECT password FROM adminTable where username='"+username+"'"+";")
    data = cursor.fetchall()
    lock.release()
    print(data)
    if(len(data) == 0 or data[0][0] != password):
        print("invalid credentials")
        messages.info(request, 'Login Details are incorrect')
        val1, data1, data2, val2, data3, val3 = getgraph()
        print(val2, data2)
        tablequery()
        return render(request, 'index.html', {"val1": val1, "data1": data1, "data2": data2, "val2": val2, "data3": data3, "val3": val3, "table1": table1, "table2": table2, "table3": table3})
    else:
        return render(request, 'dashboard.html', {"username": username})


def dataquery(request, query, username, prt):
    lock.acquire()
    file1 = open("MyFile.txt", "a")
    file1.write("Username     :    "+username)
    file1.write("\n")
    file1.write("Query        :    "+query)
    file1.write("\n")
    cursor.execute(query)
    rows = cursor.fetchall()
    file1.write("Ended  \n")
    file1.close()
    lock.release()
    data = []
    data.append(prt)
    size = len(prt)
    for i in rows:
        data.append(i)
    print(data)
    return render(request, "selectedOption.html", {"username": username, "data": data, "size": size, "queryprocess": True})


def datalessquery(request, query, username):
    lock.acquire()
    file1 = open("MyFile.txt", "a")
    file1.write("Username     :    "+username)
    file1.write("\n")
    file1.write("Query        :    "+query)
    file1.write("\n")
    try:
        cursor.execute(query)
        cnxn.commit()
    except pyodbc.IntegrityError:
        print("Integrity error occured")
    file1.write("Ended  \n")
    file1.close()
    lock.release()
    return render(request, "selectedOption.html", {"username": username, "queryprocess": True, "size": str(0), "data": "Official added successfully"})


def queryini(request, query, username, querytype, prt):
    if(querytype == 1):
        return dataquery(request, query, username, prt)
    else:
        return datalessquery(request, query, username)

def queryprocess(request):
    username = request.POST['username']
    queryn = int(request.POST['vote'])
    print(username, " ", queryn)
    query = ""
    qt = 0
    prt = []
    if(queryn == 1):
        query = "Select Voter_ID,Name,Age,City,Booth_Number from Voter;"
        prt = ["Voter_ID", "Name", "Age", "City", "Booth_Number"]
        qt = 1
    elif(queryn == 2):
        query = "SELECT vote, COUNT(*) FROM voterTable GROUP BY vote;"
        prt = ["vote", "total "]
        qt = 1
    elif(queryn == 3):
        print()
        ids = request.POST['officerid']
        name = request.POST['name']
        category = request.POST['category']
        bn = request.POST['bn']
        add = request.POST['add']
        contact = request.POST['contact']
        query = "INSERT INTO Booth_Level_Officer(OfficerId , Name ,Category , BoothNo , Address , Contact) VALUES ('"+ids +"' , '"+name +"' , '"+ category+"' , '"+bn +"' , '"+ add+"' , '"+contact +"');"
        qt = 0
    elif(queryn == 4):
        query = "Select * from Booth_Level_Officer;"
        prt = ["offId", "Name", "Category", "BoothNo", "Address", "Contact"]
        qt = 1
    else:
        query = "SELECT  C.CandidateID,C.Name, C.PARTYID, P.PartyName from Candidate C, Party P;"
        prt = ["C.CandidateID", "C.Name", "C.PARTYID", "P.PartyName"]
        qt = 1

    thread1 = threading.Thread(target = queryini(request, query, username, qt, prt), args = ())
    #thread1.start()
    #thread1.join()
    return queryini(request, query, username, qt, prt)


def votinglogin(request):
    return render(request, 'votinglogin.html')


def votingcast(request):
    print("herer")
    username = request.POST['username']
    vt = int(request.POST['vote'])
    print(username, vt)
    cursor.execute("UPDATE voterTable SET vote="+str(vt) +
                   "where username='"+username+"';")
    cnxn.commit()
    lis = countvotes()
    return render(request, 'voterdashboard.html', {"username": username, "voted": str(True), "list": lis})


def countvotes():
    cursor.execute("SELECT vote FROM voterTable;")
    data = cursor.fetchall()
    print(data)
    lis = []
    for i in range(4):
        lis.append(0)
    for i in data:
        print(i[0])
        if(i[0] != 0):
            lis[i[0]-1] += 1
    print(lis)
    return lis


def voterdashboard(request):
    # checking for credentials from votinglogin.html
    print("checking")
    username = request.POST['voter_username']
    password = request.POST['voter_password']
    cursor.execute(
        "SELECT * FROM voterTable where username='"+username+"'"+";")
    data = cursor.fetchall()
    print(data)
    if(len(data) == 0 or data[0][1] != password):
        print("invalid credentials")
        messages.info(request, 'Login Details are incorrect')
        return HttpResponseRedirect('votinglogin.html')
    else:
        voted = False
        if(data[0][2] != 0):
            voted = True
        lis = countvotes()
        return render(request, 'voterdashboard.html', {"username": username, "voted": str(voted), "list": lis})


'''try:
    query = "INSERT INTO adminTable(username , password) VALUES ('demouser1' , 'demopassword1');"
    cursor.execute(query) 
    print("here")
    cnxn.commit()
except pyodbc.IntegrityError:
    print("Integrity error occured")'''

'''
text = "SELECT * FROM Assembly1212;"
thread1 = threading.Thread(target = queryini(text , "demo" , 1), args = ())
thread1.start()
thread1.join()
thread2 = threading.Thread(target = queryini(text , "demo" , 2), args = ())
thread2.start()
thread2.join()'''
