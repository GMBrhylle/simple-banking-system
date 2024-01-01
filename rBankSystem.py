import mysql.connector
from BankClient import BankClient
from datetime import datetime, date

from BankAccount import BankAccount

class BankSystem:
    def __init__(self):
        self.db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="bank_system"
        )
        self.cursor = self.db_connection.cursor()

    ### BANK CLIENT ###
     # NEW CLIENT DATABASE MANAGEMENT
    def createNewClient(self, client):
        query = "INSERT INTO CLIENT (ClientID, FirstName, MiddleName, LastName, DateOfBirth, Address, Contact, EmailAddress, TypeofID_1, TypeofID_2) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        
        accepted_id_query = "SELECT IDType FROM ListID"
        self.cursor.execute(accepted_id_query)
        accepted_id_types = [row[0] for row in self.cursor.fetchall()]

        print("\nSelect a Type of ID:")
        for i, id_type in enumerate(accepted_id_types, start=1):
            print(f"{i}. {id_type}")
            
        print("\nOne (1) valid ID is acceptable if the ID is a Passport, Driver’s License, PRC ID, UMID, SSS ID, PhilSys ID, or School ID (for minors).")
        
        while True:
            try:
                selected_id_index = int(input("Enter the number corresponding to the Type of ID: "))
                if 1 <= selected_id_index <= len(accepted_id_types):
                    selected_id = accepted_id_types[selected_id_index - 1]
                    client.type_of_id_1 = selected_id

                    if selected_id not in ['Passport', "Driver's License", 'Professional Regulations Commission (PRC) ID', 'UMID', 'SSS ID', 'PhilSys ID', 'School ID (for minors)']:
                        accepted_id_types = [id_type for id_type in accepted_id_types if id_type != selected_id]

                        print("\nPlease provide at least one more valid ID from the accepted list:")
                        accepted_id_types = [id_type for id_type in accepted_id_types if id_type not in ['Passport', "Driver's License", 'Professional Regulations Commission (PRC) ID', 'UMID', 'SSS ID', 'PhilSys ID', 'School ID (for minors)']]
                        for i, id_type in enumerate(accepted_id_types, start=1):
                            print(f"{i}. {id_type}")

                        selected_id_index = int(input("\nEnter the number corresponding to the Type of ID: "))
                        if 1 <= selected_id_index <= len(accepted_id_types):
                            selected_id = accepted_id_types[selected_id_index - 1]
                            client.type_of_id_2 = selected_id
                        else:
                            print("Invalid selection. Client creation failed.")
                    break
                else:
                    print("Invalid selection. Please enter a valid number.")
            except ValueError:
                print("Error: Please enter a number only.")

        try:
            self.cursor.execute(query, (
                client.client_id, client.first_name, client.middle_name, client.last_name, 
                client.date_of_birth, client.address, client.contact, client.email_address, 
                client.type_of_id_1, client.type_of_id_2
            ))
            self.db_connection.commit()
            print("\nClient added successfully!")
        except mysql.connector.Error as err:
            print(f"Error: {err}")


    
    # FIND CLIENT DATABASE MANAGEMENT
    def findClient(self, client_id):
        query = "SELECT * FROM CLIENT WHERE ClientID = %s"
        self.cursor.execute(query, (client_id,))
        client_data = self.cursor.fetchone()

        if client_data:
            client = BankClient(*client_data[0:8])
            client.type_of_id_1 = client_data[8]
            client.type_of_id_2 = client_data[9]
            return client
        else:
            print("Client not found.")
            return None


    # UPDATE CLIENT DATABASE MANAGEMENT
    def updateClientInformation(self, client_id, new_info):
        columns_to_update = ', '.join([f"{key} = '{value}'" for key, value in new_info.items()])
        query = f"UPDATE CLIENT SET {columns_to_update} WHERE ClientID = {client_id}"

        try:
            self.cursor.execute(query)
            self.db_connection.commit()
            print("Client information updated successfully!")
        except mysql.connector.Error as err:
            print(f"Error: {err}")


    # LIST ALL CLIENT DATABASE MANAGEMENT
    def listAllClients(self):
        query = "SELECT * FROM CLIENT"
        self.cursor.execute(query)
        all_clients_data = self.cursor.fetchall()

        if all_clients_data:
            print("List of all clients:")
            for client_data in all_clients_data:
                client = BankClient(*client_data[0:8])
                client.type_of_id_1 = client_data[8]
                client.type_of_id_2 = client_data[9]
                client.printDetails()
                print("-------------")
        else:
            print("No clients found.")


    # REMOVE CLIENT DATABASE MANAGEMENT
    def removeClient(self, client_id):
        query = "DELETE FROM CLIENT WHERE ClientID = %s"
        try:
            self.cursor.execute(query, (client_id,))
            self.db_connection.commit()
            print("Client removed successfully!")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    
    ### BANK ACCOUNT ###
    def openAccount (self, account_id, client_id, balance):
        try:
            query = "INSERT INTO account (AccountID, ClientID, TypeofAccount, Balance) VALUES (%s, %s, %s, %s)"
            account_type = 'Savings'
            self.cursor.execute(query, (account_id, client_id, account_type, balance))
            self.db_connection.commit()
            print("Account opened successfully!")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    
    def showAccountBalance (self, account_id, client_id):
        query = "SELECT Balance FROM account WHERE AccountID = %s AND ClientID = %s"
        self.cursor.execute(query, (account_id, client_id))
        balance = self.cursor.fetchone()

        if balance is not None:
            print(f"Account ID: {account_id}, Client ID: {client_id}, Balance: ₱{balance[0]}")
        else:
            print("Account not found.")
    
            
    # DEPOSIT MONEY DATABASE MANAGEMENT
    def depositAccount(self, account_id, amount):
        try:
            query = "UPDATE account SET Balance = Balance + %s WHERE AccountID = %s"
            self.cursor.execute(query, (amount, account_id))
            self.db_connection.commit()
            print(f"${amount} deposited successfully to Account ID: {account_id}")
        except mysql.connector.Error as err:
            print(f"Error: {err}")


    # WITHDRAW MONEY DATABASE MANAGEMENT
    def withdrawAccount(self, account_id, amount):
        try:
            query = "SELECT Balance FROM account WHERE AccountID = %s"
            self.cursor.execute(query, (account_id,))
            balance = self.cursor.fetchone()[0]
            if balance < amount:
                print("Insufficient funds!")
            else:
                query = "UPDATE account SET Balance = Balance - %s WHERE AccountID = %s"
                self.cursor.execute(query, (amount, account_id))
                self.db_connection.commit()
                print(f"${amount} withdrawn successfully from Account ID: {account_id}")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
    
                
    # CLOSE ACCOUNT DATABASE MANAGEMENT
    def closeAccount(self, account_id):
        try:
            query = "DELETE FROM account WHERE AccountID = %s"
            self.cursor.execute(query, (account_id,))
            self.db_connection.commit()
            print(f"Account ID: {account_id} closed successfully!")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        
    
    # MAIN MENU MANAGEMENT
    def mainMenu(self):
        while True:
            print("\nMain Menu")
            print("1. Client Management")
            print("2. Account Management")
            print("3. Quit")
            choice = input("\nEnter choice: ")

            if choice == '1':
                self.clientManagementMenu()
            elif choice == '2':
                self.accountManagementMenu()
            elif choice == '3':
                print("Exiting program...")
                break
            else:
                print("Invalid choice. Please try again.")


    # CLIENT MENU  MANAGEMENT
    def clientManagementMenu(self):
        while True:
            print("\nClient Management Menu")
            print("1. Create/Add New Client")
            print("2. Find Client")
            print("3. Update Client Information")
            print("4. List All Client")
            print("5. Remove Client")
            print("6. Back to Main Menu")
            choice = input("\nEnter choice: ")

            if choice == '1':
                client_id = int(input("\nEnter Client ID: "))
                
                first_name = None
                while first_name is None or not first_name.strip():
                    first_name = input("Enter First Name: ")
                    if not first_name.strip():
                        print("Error: Please enter your First Name")

                middle_name = input("Enter Middle Name (optional): ")

                last_name = None
                while last_name is None or not last_name.strip():
                    last_name = input("Enter Last Name: ")
                    if not last_name.strip():
                        print("Error: Please enter your Last Name")

                date_of_birth = None
                while date_of_birth is None:
                    date_str = input("Enter Date of Birth (YYYY-MM-DD): ")
                    try:
                        date_of_birth = datetime.strptime(date_str, "%Y-%m-%d").date()

                        if date_of_birth.year > datetime.now().year:
                            print("Error: The year should not be greater than the current year")
                            date_of_birth = None
                            continue

                        if date_of_birth > date.today():
                            print("Error: The date should not be greater than the current date")
                            date_of_birth = None
                            continue

                    except ValueError:
                        print("ERROR: FORMAT SHOULD BE YYYY-MM-DD")

                address = None
                while address is None or not address.strip():
                    address = input("Enter Address: ")
                    if not address.strip():
                        print("Error: Please enter your Address")

                contact = None
                while contact is None:
                    contact = input("Enter Contact Number: ")
                    if not contact.isdigit():
                        print("Error: Contact Number should contain numbers only")
                        contact = None

                email_address = None
                while email_address is None or not email_address.strip():
                    email_address = input("Enter Email Address: ")
                    if not email_address.strip():
                        print("Error: Please enter your Email Address")

                new_client = BankClient(client_id, first_name, middle_name, last_name, date_of_birth, address, contact, email_address)
                self.createNewClient(new_client)

            elif choice == '2':
                client_id = int(input("\nEnter Client ID to find: "))
                found_client = self.findClient(client_id)
                if found_client:
                    found_client.printDetails()

            elif choice == '3':
                client_id = int(input("Enter Client ID to update: "))
                new_info = {}
                print("Enter the information you want to update (leave blank if not updating):")
                new_info['FirstName'] = input("Enter New First Name: ")
                new_info['MiddleName'] = input("Enter New Middle Name: ")
                new_info['LastName'] = input("Enter New Last Name: ")
                new_info['Address'] = input("Enter New Address: ")
                new_info['Contact'] = input("Enter New Contact Number: ")
                new_info['EmailAddress'] = input("Enter New Email Address: ")
                
                new_info = {k: v for k, v in new_info.items() if v}

                self.updateClientInformation(client_id, new_info)

            elif choice == '4':
                self.listAllClients()

            elif choice == '5':
                client_id = int(input("Enter Client ID to remove: "))
                self.removeClient(client_id)

            elif choice == '6':
                break
            else:
                print("Invalid choice. Please try again.")


    # ACCOUNT MANAGEMENT MENU
    def accountManagementMenu(self):
        while True:
            print("\nAccount Management Menu")
            print("1. Open Account")
            print("2. Show Account Balance")
            print("3. Deposit Money")
            print("4. Withdraw Money")
            print("5. Close Account")
            print("6. Back to Main Menu")
            choice = input("\nEnter choice: ")

            if choice == '1':
                account_id = int(input("Enter Account ID: "))
                client_id = int(input("Enter Client ID: "))
                initial_balance = float(input("Enter Initial Balance: "))
                self.openAccount(account_id, client_id, initial_balance)

            elif choice =='2':
                account_id = int(input("Enter Account ID: "))
                client_id = int(input("Enter Client ID: "))
                self.showAccountBalance(account_id, client_id) 

            elif choice == '3':
                account_id = int(input("Enter Account ID: "))
                amount = float(input("Enter Amount to Deposit: "))
                self.depositAccount(account_id, amount)

            elif choice == '4':
                account_id = int(input("Enter Account ID: "))
                amount = float(input("Enter Amount to Withdraw: "))
                self.withdrawAccount(account_id, amount)

            elif choice == '5':
                account_id = int(input("Enter Account ID to Close: "))
                self.closeAccount(account_id)

            elif choice == '6':
                break

            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    bank_system = BankSystem()
    bank_system.mainMenu()
