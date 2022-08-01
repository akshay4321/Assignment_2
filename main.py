import sqlite3
import pandas as panda

crypto_password = ""
file_contact = panda.read_excel("en_dn/chyper-code.xlsx")

data = file_contact.values.tolist()

def menu():
    print('1) SignUp')
    print('2) Login')
    print('3) Exit')

error_entry = True
validate = "False"

while error_entry:
    menu()

    try:
        option = int(input("Enter Your Option:- "))
    except ValueError:
        continue
    else:
        error_entry = "true"

    if(option == 1):

        while validate:
            try:
                login = input("Enter New User Login:- ")
                connection = sqlite3.connect("USER.DB")
                cursor = connection.cursor()

                cursor.execute("select count(*) from TB_USER WHERE LOGIN = '" + login + "' ")
                cur_result = cursor.fetchone()
                count = cur_result[0]
                if(count > 0):
                    print("Login Email is already taken\n")
                    continue
                else:
                    password = input("Enter New User Paasword:- ")
                    password = password.upper()

                    for i in password:
                        for sheet_cryp_data in data:
                            if i == str(sheet_cryp_data[0]):
                                crypto_password = crypto_password + str(sheet_cryp_data[1])

                    connection = sqlite3.connect("USER.DB")
                    cursor = connection.cursor()
                    cursor.execute(
                        "INSERT INTO TB_USER (LOGIN,CRYPTOGRAPHIC_PASSWORD) values ('" + login + "','" + crypto_password + "');")
                    cursor.execute("COMMIT;")
                    print("\n")
                    crypto_password = ""
                    print("**********  User Create Successfully!  **********")

            except ValueError:
                print("Error:Please Enter proper Input\n")
                continue
            else:
                break

        cursor.close()
        connection.close()

    elif(option == 2):


        while validate:
            try:
                login = input("Enter Login Details for Sign In:- ")
                password = input("Enter Paasword for Sign In:- ")
                password = password.upper()

                for i in password:
                    for sheet_cryp_data in data:
                        if i == str(sheet_cryp_data[0]):
                            crypto_password = crypto_password + str(sheet_cryp_data[1])

                connection = sqlite3.connect("USER.DB")
                cursor = connection.cursor()

                cursor.execute("select * from TB_USER WHERE LOGIN = '" + login + "' AND CRYPTOGRAPHIC_PASSWORD = '" + crypto_password + "' ")
                cur_result = cursor.fetchone()
                if(cur_result):
                    print("******************************")
                    print("Welcome,Hello " + cur_result[1] + "\n")
                    total_user_count = cur_result[3] + 1
                    print("Your Login count :" + str(total_user_count))
                    cursor.execute("UPDATE TB_USER SET ACCESS_COUNT = " + str(total_user_count) + "  WHERE LOGIN = '" + cur_result[1] + "' ")
                    cursor.execute("COMMIT;")

                    file_backup = open('data/userdb-backup.csv', mode='w+')
                    cursor.execute("SELECT * FROM TB_USER;")
                    results = cursor.fetchall()

                    for row in results:
                        file_backup.write(str(row).replace('(','').replace(')','') + "\n")

                    file_backup.flush()
                    print("\n")
                    crypto_password = ""
                    print("******************************")
                    break;

                else:
                    print("\n")
                    print("**********   Login and Paasword Does Not Match !   **********\n")
                    crypto_password = ""
                    continue

            except ValueError:
                print("Error:Please Enter proper Values\n")
                continue
            else:
                break

        cursor.close()
        connection.close()

    elif(option == 3):
        break
