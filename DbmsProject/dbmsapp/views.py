from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
import pyodbc 
server = 'dbms54.database.windows.net' 
database = 'DBMSProj' 
username = 'groupid' 
password = 'qwertyuiop@123' 
cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=dbms54.database.windows.net,1433', user='dbms54@dbms54.database.windows.net', password=password, database='DMBSProj')
print('done')
cursor = cnxn.cursor()
cursor.execute("SELECT @@version;") 
row = cursor.fetchone() 
while row: 
    print (row[0] )
    row = cursor.fetchone()

def home(request ):
    return render(request , "index.html" , {'name':"Names"})

def add(request):
    num1 = int(request.POST['num1'])
    num2 = int(request.POST['num2'])
    return render(request , "home.html" , { "name" : num1+num2})