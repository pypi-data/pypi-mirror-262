import cx_Oracle

dsn_tns = cx_Oracle.makedsn('Host Name', 'Port Number', service_name='Service Name') # if needed, place an 'r' before any parameter in order to address special characters such as '\'.
conn = cx_Oracle.connect(user=r'User Name', password='Personal Password', dsn=dsn_tns) # if needed, place an 'r' before any parameter in order to address special characters such as '\'. For example, if your user name contains '\', you'll need to place 'r' before the user name: user=r'User Name'

c = conn.cursor()
c.execute('select * from database.table') # use triple quotes if you want to spread your query across multiple lines
for row in c:
    print (row[0], '-', row[1]) # this only shows the first two columns. To add an additional column you'll need to add , '-', row[2], etc.
#conn.close()