import re
import mysql.connector
import msvcrt
from BankClient import BankClient
from datetime import datetime, date

from BankAccount import BankAccount
import StringConstant

# accesses the class StringConstant
invoke_access = StringConstant.StringConstant

class BankSystem:
    def __init__(self):
        ''' Initializes the database and its connection. '''
        try:
            self.db_connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="bank_system"
            )
            self.cursor = self.db_connection.cursor()

            # Initialize menu flags
            self.current_menu = 'main_menu'
            self.previous_menu = None

        except mysql.connector.Error as err:
            print(invoke_access.ERROR_MESSAGES.get("ERROR_01: "), err)
            exit(1)

    ### BANK CLIENT ###
     # NEW CLIENT DATABASE MANAGEMENT
    def createNewClient(self, client):
        ''' This will be responsible for the creation of new clients. '''
        query = "INSERT INTO CLIENT (ClientID, FirstName, MiddleName, LastName, DateOfBirth, homeAddress, Contact, EmailAddress, TypeofID_1, TypeofID_2) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        
        accepted_id_query = "SELECT IDType FROM ListID"
        try:
            self.cursor.execute(accepted_id_query)
            accepted_id_types = [row[0] for row in self.cursor.fetchall()]

            print(f"\n", invoke_access.FIELD_LABEL_PROMPTS.get('PROMPT_01'))
            for i, id_type in enumerate(accepted_id_types, start=1):
                print(f"{i}. {id_type}")
                
            print(f"\n", invoke_access.FIELD_LABEL_PROMPTS.get('PROMPT_03'))
            
            while True:
                try:
                    selected_id_index = int(input(invoke_access.FIELD_LABEL_PROMPTS.get('PROMPT_04')))
                    if 1 <= selected_id_index <= len(accepted_id_types):
                        selected_id = accepted_id_types[selected_id_index - 1]
                        client.type_of_id_1 = selected_id

                        if selected_id not in ['Passport', "Driver's License", 'Professional Regulations Commission (PRC) ID', 'UMID', 'SSS ID', 'PhilSys ID', 'School ID (for minors)']:
                            accepted_id_types = [id_type for id_type in accepted_id_types if id_type != selected_id]

                            print(f"\n", invoke_access.FIELD_LABEL_PROMPTS.get('PROMPT_05'))
                            accepted_id_types = [id_type for id_type in accepted_id_types if id_type not in ['Passport', "Driver's License", 'Professional Regulations Commission (PRC) ID', 'UMID', 'SSS ID', 'PhilSys ID', 'School ID (for minors)']]
                            for i, id_type in enumerate(accepted_id_types, start=1):
                                print(f"{i}. {id_type}")

                            selected_id_index = int(input(f"\n{invoke_access.FIELD_LABEL_PROMPTS.get('PROMPT_06')}"))

                            if 1 <= selected_id_index <= len(accepted_id_types):
                                selected_id = accepted_id_types[selected_id_index - 1]
                                client.type_of_id_2 = selected_id
                            else:
                                print(invoke_access.ERROR_MESSAGES.get('ERROR_03'))
                        break
                    else:
                        print(f"\n", invoke_access.ERROR_MESSAGES.get('ERROR_04'))
                except ValueError:
                    print(f"\n{invoke_access.ERROR_MESSAGES.get('ERROR_05')}")

            try:
                self.cursor.execute(query, (
                    client.client_id, client.first_name, client.middle_name, client.last_name, 
                    client.date_of_birth, client.homeAddress, client.contact, client.email_address, 
                    client.type_of_id_1, client.type_of_id_2
                ))
                self.db_connection.commit()
                print(f"\n", invoke_access.FIELD_LABEL_PROMPTS.get('PROMPT_07'))
            except mysql.connector.Error as err:
                print(f"\n", invoke_access.ERROR_MESSAGES.get('ERROR_06'), err)
        except mysql.connector.Error as err:
            print(f"\n", invoke_access.ERROR_MESSAGES.get('ERROR_07'), err)


    # FIND CLIENT DATABASE MANAGEMENT
    def findClient(self, client_id):
        ''' Responsible for searching a client's details via ID. '''
        query = "SELECT * FROM CLIENT WHERE ClientID = %s"
        try:
            self.cursor.execute(query, (client_id,))
            client_data = self.cursor.fetchone()

            if client_data:
                client = BankClient(*client_data[0:8])
                client.type_of_id_1 = client_data[8]
                client.type_of_id_2 = client_data[9]
                return client
            else:
                print(f"\n{invoke_access.ERROR_MESSAGES.get('ERROR_09')} {client_id} {invoke_access.ERROR_MESSAGES.get('ERROR_9.5')}")
                return None
        except mysql.connector.Error as err:
            print(f"\n{invoke_access.ERROR_MESSAGES.get('ERROR_08')}{err}")
    

    # UPDATE CLIENT DATABASE MANAGEMENT
    def updateClientInformation(self, client_id, new_info):
        ''' The query happens within this function. '''
        if not new_info:
            print(f"\n{invoke_access.FIELD_LABEL_PROMPTS.get('PROMPT_25')}")
            return

        columns_to_update = ', '.join([f"{key} = '{value}'" for key, value in new_info.items()])
        query = f"UPDATE CLIENT SET {columns_to_update} WHERE ClientID = {client_id}"

        try:
            self.cursor.execute(query)
            self.db_connection.commit()
            print(f"\n{invoke_access.FIELD_LABEL_PROMPTS.get('PROMPT_26')} {client_id} {invoke_access.FIELD_LABEL_PROMPTS.get('PROMPT_27').upper()}")
        except mysql.connector.Error as err:
            print(f"\n{invoke_access.ERROR_MESSAGES.get('ERROR_22').capitalize()} {err}")
            
    def get_new_client_info(self):
        ''' This is a chain process of updateClientInformation(), replaces the old value with new ones. '''
        new_info = {}
        fields = [
            ('FirstName', f"{invoke_access.FIELD_LABEL_PROMPTS.get('PROMPT_28').title()}"),
            ('MiddleName', f"{invoke_access.FIELD_LABEL_PROMPTS.get('PROMPT_29').title()}"),
            ('LastName', f"{invoke_access.FIELD_LABEL_PROMPTS.get('PROMPT_30').title()}"),
            ('homeAddress', f"{invoke_access.FIELD_LABEL_PROMPTS.get('PROMPT_31').title()}"),
            ('Contact', f"{invoke_access.FIELD_LABEL_PROMPTS.get('PROMPT_32').title()}"),
            ('EmailAddress', f"{invoke_access.FIELD_LABEL_PROMPTS.get('PROMPT_33').title()}")
        ]
        
        for field, prompt in fields:
            value = input(f"Enter {prompt}:").strip()

            # Special case to allow clearing specific fields
            if value.lower() == "clear":
                new_info[field] = ''
            else:
                # Normalizes the case sensitivity of gathered inputs.
                transformed_value = (
                    value.upper() if field in ['FirstName', 'MiddleName', 'LastName']
                    else value.title() if field == 'homeAddress'   
                    else value  # If none of the above conditions are true, keep the value as it is
                )

                if transformed_value.strip():
                    new_info[field] = transformed_value

        return new_info


    # LIST ALL CLIENT DATABASE MANAGEMENT
    def listAllClients(self):
        ''' Responsible for showing all clients in the database. '''
        query = "SELECT * FROM CLIENT"

        try:
            self.cursor.execute(query)
            all_clients_data = self.cursor.fetchall()
            
            num_rows = len(all_clients_data)  # Get the number of rows
            header_msg = invoke_access.HEADER.get('HEADER_01')

            if num_rows > 0:

                header_format = "{:<15} {:<}".format('\nClient ID', 'Name')
                print(header_format)
                print('-' * (len(header_format) + 41))  # Adjust the multiplier as needed

                # Print the data
                max_name_length = max(len(f"{client_data[1]} {client_data[2]} {client_data[3]}") for client_data in all_clients_data)
                name_format = "{:<15} {:<" + str(max_name_length) + "}"

                # Print the data
                for client_data in all_clients_data:
                    client_id = str(client_data[0])
                    first_name = client_data[1]
                    middle_name = client_data[2] if client_data[2] and client_data[2] != 'NULL' else ''  # if the column contains null values, print a whitespace as a string to display.
                    last_name = client_data[3]

                    name = f"{first_name} {middle_name} {last_name}"

                    # Print the data in the dynamically determined column width
                    print(name_format.format(client_id, name))
                    print('-' * (20 + max_name_length))

                # Prints the total number of clients found after the query.
                print(f"{invoke_access.FIELD_LABEL_PROMPTS.get('PROMPT_09')} {num_rows} {invoke_access.FIELD_LABEL_PROMPTS.get('PROMPT_9.5')}\n")  # Print the total number of clients
                print('=' * len(header_msg))
            else:
                # No clients found
                if 'client'.upper() in query:
                    invoke_access.drawNotAvailable(type_menu='client(s)')
                    print('=' * len(invoke_access.HEADER.get('HEADER_10')))
                
                #print(f"{num_rows} {invoke_access.FIELD_LABEL_PROMPTS.get('PROMPT_9.5')}")
        except mysql.connector.Error as err:
            print(f"{invoke_access.FIELD_LABEL_PROMPTS.get('ERROR_11')} {err}")


    # REMOVE CLIENT DATABASE MANAGEMENT
    def removeClient(self, client_id):
        check_query = "SELECT ClientID FROM CLIENT WHERE ClientID = %s"
        delete_query = "DELETE FROM CLIENT WHERE ClientID = %s"

        try:
            # Check if the client ID exists in the database
            self.cursor.execute(check_query, (client_id,))
            existing_client = self.cursor.fetchone()

            if existing_client:
                print(f"\n\t{invoke_access.FIELD_LABEL_PROMPTS.get('PROMPT_38')}")
                print(f"\t{invoke_access.FIELD_LABEL_PROMPTS.get('PROMPT_39')}")
                is_confirm = str(input(f"{invoke_access.FIELD_LABEL_PROMPTS.get('PROMPT_37')}").strip().upper())

                if is_confirm == 'Y':
                    # Client ID found, proceed with deletion AFTER CONFIRMATION.
                    self.cursor.execute(delete_query, (client_id,))
                    self.db_connection.commit()
                    print(f"{invoke_access.FIELD_LABEL_PROMPTS.get('PROMPT_10')}{client_id}{invoke_access.FIELD_LABEL_PROMPTS.get('PROMPT_10.5')}")
                else:
                    print(f"{invoke_access.FIELD_LABEL_PROMPTS.get('PROMPT_40')}") # operation cancelled
            else:
                # Client ID not found, print a message
                print(f"{invoke_access.FIELD_LABEL_PROMPTS.get('PROMPT_23').title()} {client_id} {invoke_access.FIELD_LABEL_PROMPTS.get('PROMPT_24').title()}")

            print(f"{invoke_access.UI_ELEMENTS.get('ELEMENT_01')}")

        except mysql.connector.Error as err:
            print(f"{invoke_access.ERROR_MESSAGES.get('ERROR_12')} {client_id} {invoke_access.ERROR_MESSAGES.get('ERROR_12')} {err}")


    # BANK ACCOUNT MANAGEMENT - OPEN ACCOUNT
    def openAccount(self, account_id, client_id, balance):
        ''' Responsible for opening a new bank account for a client. '''
        try:
            query = "INSERT INTO account (AccountID, ClientID, TypeofAccount, Balance) VALUES (%s, %s, %s, %s)"
            account_type = 'Savings'
            self.cursor.execute(query, (account_id, client_id, account_type, balance))
            self.db_connection.commit()
            print("Account opened successfully!")
        except mysql.connector.Error as err:
            print(f"Error opening account: {err}")

    
    # BANK ACCOUNT MANAGEMENT - SHOW ACCOUNT BALANCE
    def showAccountBalance(self, account_id, client_id):
        ''' Responsible for displaying the balance of a bank account. '''
        query = "SELECT Balance FROM account WHERE AccountID = %s AND ClientID = %s"
        try:
            self.cursor.execute(query, (account_id, client_id))
            balance = self.cursor.fetchone()

            if balance is not None:
                print(f"Account ID: {account_id}, Client ID: {client_id}, Balance: ₱{balance[0]}")
            else:
                print("Account not found.")
        except mysql.connector.Error as err:
            print(f"Error displaying account balance: {err}")
    
            
    # BANK ACCOUNT MANAGEMENT - DEPOSIT MONEY
    def depositAccount(self, account_id, amount):
        ''' Responsible for depositing money into a bank account. '''
        try:
            query = "UPDATE account SET Balance = Balance + %s WHERE AccountID = %s"
            self.cursor.execute(query, (amount, account_id))
            self.db_connection.commit()
            print(f"${amount} deposited successfully to Account ID: {account_id}")
        except mysql.connector.Error as err:
            print(f"Error depositing money: {err}")



    # BANK ACCOUNT MANAGEMENT - WITHDRAW MONEY
    def withdrawAccount(self, account_id, amount):
        ''' Responsible for withdrawing money from a bank account. '''
        try:
            # Retrieve the current account balance
            query = "SELECT Balance FROM account WHERE AccountID = %s"
            self.cursor.execute(query, (account_id,))
            balance = self.cursor.fetchone()[0]

            if balance < amount:
                print("Insufficient funds!")
            else:
                # Update the account balance after withdrawal
                query = "UPDATE account SET Balance = Balance - %s WHERE AccountID = %s"
                self.cursor.execute(query, (amount, account_id))
                self.db_connection.commit()
                print(f"${amount} withdrawn successfully from Account ID: {account_id}")
        except mysql.connector.Error as err:
            print(f"Error withdrawing money: {err}")

                
    # BANK ACCOUNT MANAGEMENT - CLOSE ACCOUNT
    def closeAccount(self, account_id):
        ''' Responsible for closing a bank account. '''
        try:
            query = "DELETE FROM account WHERE AccountID = %s"
            self.cursor.execute(query, (account_id,))
            self.db_connection.commit()
            print(f"Account ID: {account_id} closed successfully!")
        except mysql.connector.Error as err:
            print(f"Error closing account: {err}")
        
    
    # MAIN MENU MANAGEMENT
    def mainMenu(self):
        ''' Responsible for managing the main menu of the program. '''
        try:
            while True:
                print('PREVIOUS_MENU: ', self.previous_menu)
                print('CURRENT_MENU: ', self.current_menu)
                
                print(f"\n{invoke_access.HEADER.get('HEADER_08').title()}")
                for key, value in invoke_access.MAIN_MENU_CHOICES.items():
                    print(f"[{key}] {value}")
                choice = input(f"\n{invoke_access.FIELD_LABEL_PROMPTS.get('PROMPT_11').title()}")

                # client management menu
                if choice == '1':
                    self.previous_menu = self.current_menu
                    self.current_menu = 'client'
                    self.clientManagementMenu()
                elif choice == '2':
                    self.previous_menu = self.current_menu
                    self.current_menu = 'account'
                    self.accountManagementMenu()
                elif choice.lower() == 'q': # avoids mismatch
                    print(f"\n{invoke_access.FIELD_LABEL_PROMPTS.get('PROMPT_02')}")
                    break
                else:
                    self.previous_menu = self.current_menu
                    self.current_menu = 'main_menu'
                    print(invoke_access.ERROR_MESSAGES['ERROR_02'])
        except Exception as e:
            print(f"{invoke_access.ERROR_MESSAGES.get('ERROR_13')} {e}")
            self.previous_menu = self.current_menu
            self.current_menu = 'main_menu'

    # CLIENT MENU MANAGEMENT
    def clientManagementMenu(self):
        ''' Responsible for managing client-related operations. '''
        try:
            while True:
                print('PREVIOUS_MENU: ', self.previous_menu)
                print('CURRENT_MENU: ', self.current_menu)
                print(f"\n{invoke_access.HEADER.get('HEADER_06').upper()}")

                for key, value in invoke_access.CLIENT_MENU_CHOICES.items():
                    print(f"[{key}] {value}")

                try:
                    choice = int(input(f"{invoke_access.FIELD_LABEL_PROMPTS.get('PROMPT_11').title()}"))

                    if choice not in invoke_access.CLIENT_MENU_CHOICES:
                        print(f"{invoke_access.ERROR_MESSAGES.get('ERROR_02')}")
                        continue

                    # creating new entry for a client
                    if choice == 1:
                        print(invoke_access.HEADER.get('HEADER_03').upper())

                        while True:
                            try:
                                client_id = int(input(f"\n{invoke_access.FIELD_LABEL_PROMPTS.get('PROMPT_12').title()}"))

                                existing_client = self.findClient(client_id)

                                if existing_client:
                                    print(f"{invoke_access.ERROR_MESSAGES.get('ERROR_23')} {client_id} {invoke_access.ERROR_MESSAGES.get('ERROR_24')}")
                                else:

                                    first_name = None
                                    while first_name is None or not first_name.strip():
                                        first_name = input(f"{invoke_access.FIELD_LABEL_PROMPTS.get('PROMPT_13').title()}")
                                        if not first_name.strip():
                                            print(f"{invoke_access.ERROR_MESSAGES.get('ERROR_14').title()} ")

                                    middle_name = input(f"{invoke_access.FIELD_LABEL_PROMPTS.get('PROMPT_14').title()}")

                                    last_name = None
                                    while last_name is None or not last_name.strip():
                                        last_name = input(f"{invoke_access.FIELD_LABEL_PROMPTS.get('PROMPT_15').title()}")
                                        if not last_name.strip():
                                            print(f"{invoke_access.ERROR_MESSAGES.get('ERROR_15').title()} ")

                                    date_of_birth = None
                                    while date_of_birth is None:
                                        date_str = input(f"{invoke_access.FIELD_LABEL_PROMPTS.get('PROMPT_16')}")
                                        try:
                                            date_of_birth = datetime.strptime(date_str, "%Y-%m-%d").date()

                                            if date_of_birth.year > datetime.now().year:
                                                print(f"{invoke_access.ERROR_MESSAGES.get('ERROR_16').title()} ")
                                                date_of_birth = None
                                                continue

                                            if date_of_birth > date.today():
                                                print(f"{invoke_access.ERROR_MESSAGES.get('ERROR_17').title()} ")
                                                date_of_birth = None
                                                continue

                                        except ValueError:
                                            print(f"{invoke_access.ERROR_MESSAGES.get('ERROR_18').upper()}")

                                    homeAddress = None
                                    while homeAddress is None or not homeAddress.strip():
                                        homeAddress = input(f"{invoke_access.FIELD_LABEL_PROMPTS.get('PROMPT_17').title()}")
                                        if not homeAddress.strip():
                                            print(f"{invoke_access.ERROR_MESSAGES.get('ERROR_19').title()}") 

                                    contact = None
                                    while contact is None:
                                        contact = input(f"{invoke_access.FIELD_LABEL_PROMPTS.get('PROMPT_18')}")
                                        
                                        if not contact.isdigit(): # must be a digit
                                            print(f"{invoke_access.ERROR_MESSAGES.get('ERROR_20').title()}")
                                            contact = None

                                        elif len(contact) != 11: # must be equal to 11
                                            print(f"{invoke_access.ERROR_MESSAGES.get('ERROR_27').title()}")
                                            contact = None
                                        
                                    email_address = None
                                    while email_address is None or not email_address.strip() or not re.match(r"[^@]+@[^@]+\.[^@]+", email_address):
                                        email_address = input(f"{invoke_access.FIELD_LABEL_PROMPTS.get('PROMPT_19').title()}")
                                        
                                        if not email_address.strip() or not re.match(r"[^@]+@[^@]+\.[^@]+", email_address): # email validation
                                            print(f"{invoke_access.ERROR_MESSAGES.get('ERROR_21').title()}")
                                            email_address = None

                                    new_client = BankClient(client_id, first_name.upper(), middle_name.upper(), last_name.upper(), date_of_birth, homeAddress, contact, email_address)
                                    self.createNewClient(new_client)
                                    break

                            except ValueError:
                                print(f"{invoke_access.ERROR_MESSAGES.get('ERROR_05')}")
                                    # ... end of client creation block code

                    # FIND THE CLIENT AND DISPLAY ITS DETAILS
                    elif choice == 2:
                        print(f"{invoke_access.HEADER.get('HEADER_05').upper()}")

                        try:
                            client_id = int(input(f"\n{invoke_access.FIELD_LABEL_PROMPTS.get('PROMPT_20').title()}"))
                            found_client = self.findClient(client_id)

                            if found_client:
                                found_client.printDetails()
                                print(f"{invoke_access.UI_ELEMENTS.get('ELEMENT_01')}")
                            else:
                                print(f"{invoke_access.UI_ELEMENTS.get('ELEMENT_01')}")

                        except ValueError:
                            print(f"Invalid input! Please enter a registered Client ID.")
                    # ... end of find client block code
                    

                    # UPDATES CLIENTS DETAILS
                    elif choice == 3:
                        print(f"{invoke_access.HEADER.get('HEADER_04').upper()}")
                        isTrue = True
                        while isTrue:
                            try:
                                client_id = int(input(f"{invoke_access.FIELD_LABEL_PROMPTS.get('PROMPT_21').title()}"))
                                
                                # Check if the entered client ID exists in the database
                                existing_client = self.findClient(client_id)

                                if existing_client:
                                    new_info = self.get_new_client_info()
                                    self.updateClientInformation(client_id, new_info)
                                    isTrue = False  # Exit the loop when the client ID is valid
                                else:
                                    print(f"Client with ID {client_id} not found. Please enter a valid client ID.")
                            
                            except ValueError:
                                print("Invalid input! Please enter a valid client ID.")
                    # ... end of update client details


                    # SHOWS ALL CLIENTS WITH THEIR DETAILS
                    elif choice == 4:
                        print(f"\n{invoke_access.HEADER.get('HEADER_01').upper()}")
                        self.listAllClients()
                    # ... endline of showing all clients


                    # REMOVE CLIENT
                    elif choice == 5:
                        print(f"\n{invoke_access.HEADER.get('HEADER_02').upper()}")

                        try:
                            client_id = int(input(f"{invoke_access.FIELD_LABEL_PROMPTS.get('PROMPT_34')} "))
                            self.removeClient(client_id)

                        except ValueError:
                            print(f"Invalid input! Please enter a valid client ID.")
                    # ... end of the remove client removal.


                    # GO BACK TO THE MAIN MENU
                    elif choice == 6:
                        if self.previous_menu == 'main_menu':
                            self.previous_menu = self.current_menu
                            self.current_menu = 'main_menu'
                            break
                        elif self.previous_menu == 'account':
                            self.previous_menu = self.current_menu
                            self.current_menu = 'account'
                            self.accountManagementMenu()
                            break

                except Exception as e:
                    print(f"An unexpected error occurred: {e}")
                    if self.previous_menu == 'main_menu':
                        self.previous_menu = self.previous_menu
                        self.current_menu = 'client'
                    elif self.previous_menu == 'account':
                        self.previous_menu = 'account'
                        self.current_menu = 'client'
        except Exception as main_menu_error:
            print(f"An unexpected error occurred in the main menu: {main_menu_error}")
    
    # ACCOUNT MANAGEMENT MENU
    def accountManagementMenu(self):
        ''' Responsible for managing account-related operations. '''
        
        # Create a dictionary to map choices to functions
        account_functions = {
            1: self.handle_listing,     # Lists accs with associated client ids
            2: self.handle_show_bal,    # Modular handling of showing balance
            3: self.handle_deposit,     # Modular handling of deposits
            4: self.handle_withdraw,    # Modular handling of withdrawal
            5: self.handle_open_acc,    # Modular handling of opening accs
            6: self.handle_close_acc,   # Modular handling of closing accs
            7: self.handle_exit  # Exit function or back to main menu
        }

        while True:
            print('PREVIOUS_MENU: ', self.previous_menu)
            print('CURRENT_MENU: ', self.current_menu)

            print(f"\n{invoke_access.HEADER.get('HEADER_07').upper()}")
            for key, value in invoke_access.ACCOUNT_MENU_CHOICES.items():   # UI for account_menu
                print(f"[{key}] {value}")
            try:
                choice = int(input(f"\n{invoke_access.FIELD_LABEL_PROMPTS.get('PROMPT_11').title()}"))

                # Call the corresponding function based on the user's input
                selected_function = account_functions.get(choice, None)
                if selected_function:
                    selected_function()
                else:
                    print(f"{invoke_access.ERROR_MESSAGES.get('ERROR_02')}")
            except ValueError:
                print(f"{invoke_access.ERROR_MESSAGES.get('ERROR_05')}")
                if self.previous_menu == 'main_menu':
                    self.previous_menu == 'main_menu'
                    self.current_menu == 'account'


    def handle_open_acc(self):
        ''' Handles the few necessary setups for opening a new account '''
        print(f"{invoke_access.HEADER.get('HEADER_09').upper()}")

        for key, value in invoke_access.OPEN_ACCOUNT_DIALOG.items():
            print(f"[{key}] {value}")

        try:
            # Ask user if they're new or existing client
            isNew = int(input(f"\n{invoke_access.FIELD_LABEL_PROMPTS.get('PROMPT_11').title()}"))
            match isNew:
                case 1: # if client is new to the system
                    print(f"\n{invoke_access.FIELD_LABEL_PROMPTS.get('PROMPT_35')}")
                    self.previous_menu = self.current_menu
                    self.current_menu = 'client'
                    self.clientManagementMenu()
                case 0: # if client chooses existing
                    client_id = int(input("Enter Client ID: "))
                    account_id = int(input("Enter Account ID: "))
                    initial_balance = float(input("Enter Initial Balance: "))
                    self.openAccount(account_id, client_id, initial_balance)
                case _:
                    print(f"{invoke_access.ERROR_MESSAGES.get('ERROR_02')}")
                    #self.previous_menu = self.current_menu
                    self.current_menu = 'account'
        except:
            print("An error occurred in the match statement.")

    def handle_listing(self):
        ''' Responsible for showing all accounts and associated clients with it in the database. '''
        query = "SELECT * FROM ACCOUNT"
        print(f"{invoke_access.HEADER.get('HEADER_10').upper()}")
        self.showAllAccounts(query)


    def showAllAccounts(self, query):
        try:
            self.cursor.execute(query)
            all_accounts_data = self.cursor.fetchall()
            num_rows = len(all_accounts_data)  # Get the number of rows

            if num_rows > 0:
                header_format = "{:<15} {:<}".format('\nAccount ID', 'Client ID') # adjusts the header mid gaps
                print(header_format)
                print('-' * (len(header_format) + 5)) #


                max_name_length = max(len(str(account_data[1])) for account_data in all_accounts_data)
                name_format = "{:<14} {:<" + str(max_name_length) + "}" # adjust the mid gaps between the data entries


                for account_data in all_accounts_data:
                    account_id = str(account_data[0])
                    account_name = account_data[1]

                    # Print the data in the dynamically determined column width
                    print(name_format.format(account_id, account_name))
                    print('-' * (29 + max_name_length))

                # Prints the total number of accounts found after the query.
                print(f"{invoke_access.FIELD_LABEL_PROMPTS.get('PROMPT_09')} {num_rows} {invoke_access.FIELD_LABEL_PROMPTS.get('PROMPT_9.6')}\n")  # Print the total number of accounts
                print('=' * len(invoke_access.HEADER.get('HEADER_10')))

            else:
                # No accounts found
                if 'account'.upper() in query:
                    invoke_access.drawNotAvailable(type_menu='account(s)')
                    print('=' * len(invoke_access.HEADER.get('HEADER_10')))

        except mysql.connector.Error as mySQLErr:
                # Handles MySQL errors
            error_code = mySQLErr.errno
            error_msg = mySQLErr.msg

            if error_code == 1045:
                print(f"Access denied: {error_msg}")

            elif error_code == 1049:
                print(f"Database does not exist: {error_msg}")

            else:
                print(f"Database error: {error_msg} (Error code: {error_code})")

        except Exception as e:
            # Handles other unexpected errors
            print(f"Unexpected error: {e}")

            

    def handle_show_bal(self):
        # Handles the displaying of account balance
        account_id = int(input("Enter Account ID: "))
        client_id = int(input("Enter Client ID: "))
        self.showAccountBalance(account_id, client_id)

    def handle_deposit(self):
        # Handles depositing money into an account
        account_id = int(input("Enter Account ID: "))
        amount = float(input("Enter Amount to Deposit: "))
        self.depositAccount(account_id, amount)

    def handle_withdraw(self):
        # Handles withdrawing money from an account
        account_id = int(input("Enter Account ID: "))
        amount = float(input("Enter Amount to Withdraw: "))
        self.withdrawAccount(account_id, amount)

    def handle_close_acc(self):
        # Handles closing an account
        account_id = int(input("Enter Account ID to Close: "))
        self.closeAccount(account_id)

    def handle_exit(self):
    # This function does nothing and serves as an exit point for the loop
        try:
            self.previous_menu = self.current_menu
            self.current_menu = 'main_menu'
            self.mainMenu()
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    try:
        bank_system = BankSystem()
        bank_system.mainMenu()
    except KeyboardInterrupt:
        print("Program terminated by user.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")