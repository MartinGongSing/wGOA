def downSampling3():


    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="goaubi"
    )

    mycursor = mydb.cursor()

    # Preparing the query to delete records
    sql = "TRUNCATE TABLE newpsap"

    try:
        # Execute the SQL command
        mycursor.execute(sql)

        # Commit your changes in the database
        mydb.commit()
    except:
        # Roll back in case there is any error
        mydb.rollback()



    data = {'IDpsap': [], 'blue': [], 'red': [], 'green': []}

    psapdisplay_det3 = psap.objects.using('dataGOA').order_by('-time').all()


    for unit in psapdisplay_det3:
        data['IDpsap'].insert(0, unit.time)
        data['blue'].insert(0, unit.blue)
        data['red'].insert(0, unit.red)
        data['green'].insert(0, unit.green)

    i=0
    while i < len(data['blue']):
        tim =  data['IDpsap'][i]
        blue100 = data['blue'][i:i+99]
        newblue = sum(blue100)/len(blue100)

        red100 = data['red'][i:i + 99]
        newred = sum(red100) / len(red100)

        green100 = data['green'][i:i + 99]
        newgreen = sum(green100) / len(green100)

        # data['newblue'].insert(0, newblue)


        # print("t=",tim )
        sql = "INSERT INTO newpsap (time, blue, red, green) VALUES (%s, %s, %s, %s)"

        val = (tim, newblue, newred, newgreen)

        mycursor.execute(sql, val)

        mydb.commit()

        print(mycursor.rowcount, "record inserted.")

        i += 100

    return None