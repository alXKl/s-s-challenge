import pymysql
import csv

endpoint = 'xxxxxxxxx'
username = 'xxxxxxxxx'
password = 'xxxxxxxxx'
database_name = 'xxxxxxxxx'

connection = pymysql.connect(host=endpoint, user=username, passwd=password, db=database_name)

def session():
    print("------------------------------------------------------------------------")
    print("|  Welcome to the db-session on the titanic data-set with admin role.  |")
    print("|  Please choose one of the following options:                         |")
    print("------------------------------------------------------------------------")

    cursor = connection.cursor(pymysql.cursors.DictCursor)
    choice = False
    while(choice != 'q'):
        print("[1] Operate on the db.")
        print("[2] Show all users.")
        print("[3] Add a new user with read-access.")
        print("[4] Remove a user.")
        print("[5] Create and fill the \"passengers\" table.")
        print("[q] Quit session.")

        choice = input("Choose option: ")

        if choice == '1':
            statement = input("Enter your SQL-statement: ")
            try: 
                cursor.execute(statement)
                result = cursor.fetchall()
                print(result)
            except Exception as e:
                print(e)

        elif choice == '2':
            try:
                cursor.execute("SELECT DISTINCT User FROM mysql.user")
                result = cursor.fetchall()
                print(result)
            except Exception as e:
                print(e)

        elif choice == '3':
            try:
                name = input("Create user-name: ")
                pw = input("Create user-password: ")
                cursor.execute("CREATE USER " + "\'" + name + "\'" +"@"+"\'%\'" + " IDENTIFIED BY " + "\'" + pw + "\'")
                cursor.execute("GRANT SELECT ON " + database_name + ".*" + " TO " + "\'" + name + "\'" +"@"+"\'%\'")
            except Exception as e:
                print(e)

        elif choice == '4':
            try:
                name = input("Remove user: ")
                cursor.execute("DROP USER " + "\'" + name + "\'" +"@"+"\'%\'")
            except Exception as e:
                print(e)

        elif choice == '5':
            try:
                create = """create table if not exists passengers (
                        id integer primary key,
                        survived integer,
                        pclass integer,
                        family varchar(255),
                        pname varchar(255),
                        sex varchar(6),
                        age double,
                        sibsp integer,
                        parch integer,
                        ticket varchar(255),
                        fare double,
                        cabin varchar(16),
                        embarked varchar(16) )"""
                cursor.execute(create)
                data = csv.reader(open('titanic_data.csv'))
                fill = """INSERT INTO challenge.passengers(id,survived,pclass,family,pname,sex,age,sibsp,parch,ticket,fare,cabin,embarked) 
                        VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
                next(data)
                for line in data:
                    line=[None if cell == '' else cell for cell in line]
                    cursor.execute(fill, line)
                connection.commit()
            except Exception as e:
                print(e)
                
        elif choice == 'q':
            print("Good bye!")
        else:
            print("Your choice don't match any of the available options.")
        print('')


if __name__ == "__main__":
    session()