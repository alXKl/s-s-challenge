import pymysql

endpoint = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
database_name = 'xxxxxxxxxxxxxxxxxxxxxxxx'


def session():
    username = input('Username: ')
    password = input('Password: ')

    try:
        connection = pymysql.connect(host=endpoint, user=username, passwd=password, db=database_name)
    except Exception as e:
                print(e)

    print("--------------------------------------------------------")
    print("|  Welcome to the db-session on the titanic data-set.  |")
    print("|  Please choose one of the following options:         |")
    print("--------------------------------------------------------")

    cursor = connection.cursor(pymysql.cursors.DictCursor)
    choice = False
    while(choice != 'q'):
        print("[1] Query the db.")
        print("[q] Quit session.")

        choice = input("Choose option: ")

        if choice == '1':
            statement = input("Enter your SQL-query: ")
            try: 
                cursor.execute(statement)
                result = cursor.fetchall()
                print(result)
            except Exception as e:
                print(e)
                
        elif choice == 'q':
            print("Good bye!")
        else:
            print("Your choice don't match any of the available options.")



if __name__ == "__main__":
    session()