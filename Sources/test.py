# Importing module
import mysql.connector
import uuid
 
# Creating connection object
mydb = mysql.connector.connect(
    host = "sql12.freesqldatabase.com",
    user = "sql12532759",
    password = "L7cn3eESyz",
    database="sql12532759"
)

mycursor = mydb.cursor()

# Printing the connection object
print(mydb)

# show all table
mycursor = mydb.cursor()
 
# mycursor.execute("Show tables;")
 
# myresult = mycursor.fetchall()
 
# for x in myresult:
#     print(x)

#insert assembly
# INSERT INTO `assembly` (`id`, `category`, `hasWorker`, `hasProduct`, `status`) VALUES ('2', 'SUV', '0', '0', 'STOPPED');
# sql = "INSERT INTO `assembly` (`id`, `category`, `hasWorker`, `hasProduct`, `status`) VALUES (%s, %s, %s, %s, %s)"
# val = ('1', 'SUV', '0', '0', 'STOPPED')
# mycursor.execute(sql, val)
# val = ('2', 'SEDAN', '0', '0', 'STOPPED')
# mycursor.execute(sql, val)
# val = ('3', 'MINIVAN', '0', '0', 'STOPPED')
# mycursor.execute(sql, val)
# mydb.commit()

#insert worker
#INSERT INTO `worker` (`id`, `name`, `specialization`, `workingShift`, `workingTime`, `assemblyId`) VALUES ('1', 'Nguyen Van Dien', 'SUV', 'ON_SHIFT', 'ON_FREE', 'None');
# sql = "INSERT INTO `worker` (`id`, `name`, `specialization`, `workingShift`, `workingTime`, `assemblyId`) VALUES (%s, %s, %s, %s, %s, %s)"
# val = ('1', 'Nguyen Van Dien', 'SUV', 'ON_SHIFT', 'ON_FREE', 'None')
# mycursor.execute(sql, val)
# val = ('2', 'Nguyen Minh Duy', 'SUV', 'OUT_SHIFT', 'NONE', 'None')
# mycursor.execute(sql, val)
# val = ('3', 'Nguyen Van Tien', 'SUV', 'ON_SHIFT', 'ON_FREE', 'None')
# mycursor.execute(sql, val)
# val = ('4', 'Nguyen Van Tung', 'SUV', 'ON_SHIFT', 'ON_FREE', 'None')
# mycursor.execute(sql, val)
# val = ('5', 'To Thi Minh Hang', 'SEDAN', 'ON_SHIFT', 'ON_FREE', 'None')
# mycursor.execute(sql, val)
# mydb.commit()


