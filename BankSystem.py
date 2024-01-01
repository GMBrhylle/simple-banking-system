import re
import sys
import mysql.connector
import prettytable as pt
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
                database="banking_system"
            )
            self.cursor = self.db_connection.cursor()

            # Initialize menu flags
            self.current_menu = 'main_menu'
            self.previous_menu = None

            self.selected_section = None

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
                    selected_id_index = int(
                        input(invoke_access.FIELD_LABEL_PROMPTS.get('PROMPT_04')))
                    if 1 <= selected_id_index <= len(accepted_id_types):
                        selected_id = accepted_id_types[selected_id_index - 1]
                        client.type_of_id_1 = selected_id

                        if selected_id not in ['Passport', "Driver's License", 'Professional Regulations Commission (PRC) ID', 'UMID', 'SSS ID', 'PhilSys ID', 'School ID (for minors)']:
                            accepted_id_types = [
                                id_type for id_type in accepted_id_types if id_type != selected_id]

                            print(f"\n", invoke_access.FIELD_LABEL_PROMPTS.get(
                                'PROMPT_05'))
                            accepted_id_types = [id_type for id_type in accepted_id_types if id_type not in [
                                'Passport', "Driver's License", 'Professional Regulations Commission (PRC) ID', 'UMID', 'SSS ID', 'PhilSys ID', 'School ID (for minors)']]
                            for i, id_type in enumerate(accepted_id_types, start=1):
                                print(f"{i}. {id_type}")

                            selected_id_index = int(
                                input(f"\n{invoke_access.FIELD_LABEL_PROMPTS.get('PROMPT_06')}"))

                            if 1 <= selected_id_index <= len(accepted_id_types):
                                selected_id = accepted_id_types[selected_id_index - 1]
                                client.type_of_id_2 = selected_id
                            else:
                                print(invoke_access.ERROR_MESSAGES.get('ERROR_03'))
                        break
                    else:
                        print(f"\n", invoke_access.ERROR_MESSAGES.get('ERROR_04'))
                except ValueError as ve:
                    print(
                        f"\n{invoke_access.ERROR_MESSAGES.get('ERROR_05')} {ve}")

            try:
                self.cursor.execute(query, (
                    client.client_id, client.first_name, client.middle_name, client.last_name,
                    client.date_of_birth, client.homeAddress, client.contact, client.email_address,
                    client.type_of_id_1, client.type_of_id_2
                ))
                self.db_connection.commit()
                print(f"\n{invoke_access.FIELD_LABEL_PROMPTS.get('PROMPT_07')}")
                print("=" * len(invoke_access.HEADER.get('HEADER_03')))

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
                print(
                    f"\n{invoke_access.ERROR_MESSAGES.get('ERROR_09')} {client_id} {invoke_access.ERROR_MESSAGES.get('ERROR_9.5')}")
                return None
        except mysql.connector.Error as err:
            print(f"\n{invoke_access.ERROR_MESSAGES.get('ERROR_08')}{err}")

    # UPDATE CLIENT DATABASE MANAGEMENT

    def updateClientInformation(self, client_id, new_info):
        ''' The query happens within this function. '''
        if not new_info:
            print(f"\n{invoke_access.FIELD_LABEL_PROMPTS.get('PROMPT_25')}")
            return

        columns_to_update = ', '.join(
            [f"{key} = '{value}'" for key, value in new_info.items()])
        query = f"UPDATE CLIENT SET {columns_to_update} WHERE ClientID = {client_id}"

        try:
            self.cursor.execute(query)
            self.db_connection.commit()
            print(f"\n{invoke_access.FIELD_LABEL_PROMPTS.get('PROMPT_26')} {client_id} {invoke_access.FIELD_LABEL_PROMPTS.get('PROMPT_27').upper()}")
        except mysql.connector.Error as err:
            print(
                f"\n{invoke_access.ERROR_MESSAGES.get('ERROR_22').capitalize()} {err}")

    def get_new_client_info(self):
        ''' This is a chain process of updateClientInformation(), replaces the old value with new ones. '''
        new_info = {}
        fields = [
            ('FirstName',
             f"{invoke_access.FIELD_LABEL_PROMPTS.get('PROMPT_28').title()} "),
            ('MiddleName',
             f"{invoke_access.FIELD_LABEL_PROMPTS.get('PROMPT_29').title()} "),
            ('LastName',
             f"{invoke_access.FIELD_LABEL_PROMPTS.get('PROMPT_30').title()} "),
            ('homeAddress',
             f"{invoke_access.FIELD_LABEL_PROMPTS.get('PROMPT_31').title()} "),
            ('Contact',
             f"{invoke_access.FIELD_LABEL_PROMPTS.get('PROMPT_32').title()} "),
            ('EmailAddress',
             f"{invoke_access.FIELD_LABEL_PROMPTS.get('PROMPT_33').title()} ")
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

                # controls the internal padding of table
                header_format = "{:<15} {:<}".format('\nClient ID', 'Name')
                print(header_format)
                # controls the length of dashes in the header.
                print('-' * (len(header_format) + 41))

                # Print the data
                max_name_length = max(len(
                    f"{client_data[1]} {client_data[2]} {client_data[3]}") for client_data in all_clients_data)
                # controls the content padding of the table.
                name_format = "{:<14} {:<" + str(max_name_length) + "}"

                # Print the data
                for client_data in all_clients_data:
                    client_id = str(client_data[0])
                    first_name = client_data[1]
                    # if the column contains null values, print a whitespace as a string to display.
                    middle_name = client_data[2] if client_data[2] and client_data[2] != 'NULL' else ''
                    last_name = client_data[3]

                    name = f"{first_name} {middle_name} {last_name}"

                    # Print the data in the dynamically determined column width
                    print(name_format.format(client_id, name))
                    # controls the length of the dashes inside the table
                    print('-' * (20 + max_name_length))

                # Prints the total number of clients found after the query.
                # Print the total number of client2s
                print(
                    f"{invoke_access.FIELD_LABEL_PROMPTS.get('PROMPT_09')} {num_rows} {invoke_access.FIELD_LABEL_PROMPTS.get('PROMPT_9.5')}\n")
        
            else:
                # No clients found
                if 'client'.upper() in query:
                    invoke_access.drawNotAvailable(type_menu='client(s)')

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
                print(
                    f"\n\t{invoke_access.FIELD_LABEL_PROMPTS.get('PROMPT_38')}")
                print(f"\t{invoke_access.FIELD_LABEL_PROMPTS.get('PROMPT_39')}")
                is_confirm = str(
                    input(f"{invoke_access.FIELD_LABEL_PROMPTS.get('PROMPT_37')}").strip().upper())

                if is_confirm == 'Y':
                    # Client ID found, proceed with deletion AFTER CONFIRMATION.
                    self.cursor.execute(delete_query, (client_id,))
                    self.db_connection.commit()
                    print(
                        f"{invoke_access.FIELD_LABEL_PROMPTS.get('PROMPT_10')}{client_id}{invoke_access.FIELD_LABEL_PROMPTS.get('PROMPT_10.5')}")
                else:
                    # operation cancelled
                    print(f"{invoke_access.FIELD_LABEL_PROMPTS.get('PROMPT_40')}")
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
            self.cursor.execute(
                query, (account_id, client_id, account_type, balance))
            self.db_connection.commit()
            print("Account opened successfully!")
        except mysql.connector.Error as err:
            print(f"Error opening account: {err}")

    # BANK ACCOUNT MANAGEMENT - SHOW ACCOUNT BALANCE

    def showAccountBalance(self, account_id, client_id, query):
        ''' Responsible for displaying the balance of a bank account. '''
        try:
            self.cursor.execute(query, (account_id, client_id))
            balance = self.cursor.fetchone()

            if balance is not None:
                # Print the balance in a table
                query = invoke_access.QUERIES.get(9)

                # "SELECT FirstName, MiddleName, LastName FROM client WHERE ClientID = %s" where s is the substitution value for client_ID
                self.cursor.execute(query, (client_id,))
                full_name_tuple = self.cursor.fetchone()

                # THere will always be one result, but for the bug-proof code, I put if
                if full_name_tuple:

                    # Extract elements from the tuple
                    first_name, middle_name, last_name = full_name_tuple

                    # Handle the case where middle_name is 'NULL'
                    if middle_name == 'NULL':
                        middle_name = None

                    # Concatenate full name using an if-else statement to include middle_name only if it is not None
                    full_name = f"{first_name} {middle_name} {last_name}" if middle_name else f"{first_name} {last_name}"

                else:
                    # should catch the all NULL client values.
                    print(f"No client details found for ClientID #{client_id}")

                table = pt.PrettyTable()
                table.field_names = ["Account ID",
                                     "Client ID", "Full Name", "Balance"]
                table.add_row(
                    [account_id, client_id, full_name, f"₱{balance[0]:,.2f}"])
                print(table)

            else:  # No AccID is associated on the specified ClientID.
                print(
                    f"No ASSOCIATED AccountID #{account_id} on ClientID #{client_id}")

        except mysql.connector.Error as err:
            print(f"Error displaying account balance: {err}")

    # BANK ACCOUNT MANAGEMENT - DEPOSIT AND WITHDRAW MONEY MODULE (they both update balance from db so...)
    def updateBalance(self, account_id, amount, update_type):
        ''' Responsible for depositing and withdrawing of money into a bank account (fused withdraw and deposit func). '''
        try:
            # Fetch the balance before the update for later use.
            balance_before_query = invoke_access.QUERIES.get(11)
            self.cursor.execute(balance_before_query, (account_id,))
            balance_before = self.cursor.fetchone()

            if update_type == 'deposit':
                # deposit always "adds" on system, as a general rule of thumb
                operator = "+"
                update_method = 'deposited'.upper()

            elif update_type == 'withdraw':
                # deposit always "subtracts" on system, as a general rule of thumb
                operator = "-"
                update_method = 'withdrawn'.upper()

            # update the query method based on chosen W or D
            invoke_access.QUERIES[10] = f"UPDATE account SET Balance = Balance {operator}" + \
                " %s WHERE AccountID = %s"

            # Execute the deposit query (which is the query for updating entry on DB)
            update_balance_query = invoke_access.QUERIES.get(10)
            self.cursor.execute(update_balance_query, (amount, account_id))

            # Again, fetch using the same technique
            balance_after_query = invoke_access.QUERIES.get(11)
            self.cursor.execute(balance_after_query, (account_id,))
            balance_after = self.cursor.fetchone()

            # Fetch the client ID of who deposited.
            client_id_query = invoke_access.QUERIES.get(12)
            self.cursor.execute(client_id_query, (account_id,))
            client_id = self.cursor.fetchone()

            # Fetch the full name from the client table using a JOIN
            full_name_query = invoke_access.QUERIES.get(13)
            self.cursor.execute(full_name_query, (account_id,))
            full_name_result = self.cursor.fetchone()

            # Commit the changes.
            self.db_connection.commit()

            # Check if full_name_result is not None
            if full_name_result is not None:
                first_name, middle_name, last_name = full_name_result

                # Handle the case where middle_name is 'NULL'
                if middle_name == 'NULL':
                    middle_name = None

                full_name = f"{first_name} {middle_name} {last_name}" if middle_name else f"{first_name} {last_name}"
            else:
                # Handle the case where no full name is found
                full_name = "N/A"  # You can set a default value or handle it as needed

            # Display the operations in a table (digital receipt)
            table = pt.PrettyTable()
            table.field_names = ["Field Name", "Value"]
            table.add_row(["Account ID", account_id])
            table.add_row(["Client ID", client_id[0]])
            table.add_row(["Full Name", full_name])
            table.add_row(["Balance Before", f"₱{balance_before[0]:,.2f}"])
            table.add_row([f"Amount {update_method}",
                          f"({operator}) ₱{amount:,.2f}"])
            table.add_row(
                ["Balance After", f"(=) ₱{balance_after[0]:,.2f}"])

            print(table)
            print(
                f"\n₱{amount} has been {update_method} successfully to Account ID #{account_id}")

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
                print(
                    f"${amount} withdrawn successfully from Account ID: {account_id}")
        except mysql.connector.Error as err:
            print(f"Error withdrawing money: {err}")

    # BANK ACCOUNT MANAGEMENT - CLOSE ACCOUNT

    def closeAccount(self, account_id):
        ''' Responsible for closing a bank account. '''
        try:
            query = invoke_access.QUERIES.get(7)
            self.cursor.execute(query, (account_id,))
            self.db_connection.commit()
            print(
                f"\n{invoke_access.UI_ELEMENTS.get('ELEMENT_09')}\nAccount ID #{account_id} HAS BEEN CLOSED successfully!")

        except mysql.connector.Error as err:
            print(f"Error CLOSING Account due to : {err}")

    # MAIN MENU MANAGEMENT

    def mainMenu(self):
        ''' Responsible for managing the main menu of the program. '''
        try:
            while True:
                print('\n\nPREVIOUS_MENU: ', self.previous_menu)
                print('CURRENT_MENU: ', self.current_menu)

                print(f"\n{invoke_access.HEADER.get('HEADER_08').title()}")
                for key, value in invoke_access.MAIN_MENU_CHOICES.items():
                    print(f"[{key}] {value}")
                choice = input(
                    f"\n{invoke_access.FIELD_LABEL_PROMPTS.get('PROMPT_11').title()}")

                # client management menu
                if choice == '1':
                    self.previous_menu = self.current_menu
                    self.current_menu = 'client'
                    self.clientManagementMenu()
                elif choice == '2':
                    self.previous_menu = self.current_menu
                    self.current_menu = 'account'
                    self.accountManagementMenu()
                elif choice.lower() == 'q':  # avoids mismatch
                    print(
                        f"\n{invoke_access.FIELD_LABEL_PROMPTS.get('PROMPT_02')}")
                    break

                else:
                    self.previous_menu = self.current_menu
                    self.current_menu = 'main_menu'
                    print(invoke_access.ERROR_MESSAGES['ERROR_02'])

            # exits the program entirely if loop has been broken by "q".
            print("\n\n")
            sys.exit(0)
        except Exception as e:
            print(f"{invoke_access.ERROR_MESSAGES.get('ERROR_13')} {e}")
            self.previous_menu = self.current_menu
            self.current_menu = 'main_menu'

    # CLIENT MENU MANAGEMENT
    def clientManagementMenu(self):
        ''' Responsible for managing client-related operations. '''
        try:
            while True:
                print('\n\nPREVIOUS_MENU: ', self.previous_menu)
                print('CURRENT_MENU: ', self.current_menu)
                print(f"\n{invoke_access.HEADER.get('HEADER_06').upper()}")

                for key, value in invoke_access.CLIENT_MENU_CHOICES.items():
                    print(f"[{key}] {value}")

                try:
                    choice = int(
                        input(f"\n{invoke_access.FIELD_LABEL_PROMPTS.get('PROMPT_11').title()}"))

                    if choice not in invoke_access.CLIENT_MENU_CHOICES:
                        print(f"{invoke_access.ERROR_MESSAGES.get('ERROR_02')}")
                        continue

                    # creating new entry for a client
                    if choice == 1:
                        print(invoke_access.HEADER.get('HEADER_03').upper())

                        while True:
                            try:
                                client_id = int(
                                    input(f"\n{invoke_access.FIELD_LABEL_PROMPTS.get('PROMPT_12').title()}"))

                                existing_client = self.findClient(client_id)

                                if existing_client:
                                    print(
                                        f"{invoke_access.ERROR_MESSAGES.get('ERROR_23')} {client_id} {invoke_access.ERROR_MESSAGES.get('ERROR_24')}")
                                else:

                                    first_name = None
                                    while first_name is None or not first_name.strip():
                                        first_name = str(input(
                                            f"{invoke_access.FIELD_LABEL_PROMPTS.get('PROMPT_13')}")).upper()

                                        if not first_name.strip():
                                            print(
                                                f"{invoke_access.ERROR_MESSAGES.get('ERROR_14')} ")

                                    middle_name = str(input(
                                        f"{invoke_access.FIELD_LABEL_PROMPTS.get('PROMPT_14').title()}")).upper()

                                    last_name = None
                                    while last_name is None or not last_name.strip():
                                        last_name = str(input(
                                            f"{invoke_access.FIELD_LABEL_PROMPTS.get('PROMPT_15')}")).upper()
                                        if not last_name.strip():
                                            print(
                                                f"{invoke_access.ERROR_MESSAGES.get('ERROR_15').title()} ")

                                    date_of_birth = None
                                    while date_of_birth is None:
                                        date_str = input(
                                            f"{invoke_access.FIELD_LABEL_PROMPTS.get('PROMPT_16')}")
                                        try:
                                            date_of_birth = datetime.strptime(
                                                date_str, "%Y-%m-%d").date()

                                            if date_of_birth.year > datetime.now().year:
                                                print(
                                                    f"{invoke_access.ERROR_MESSAGES.get('ERROR_16').title()} ")
                                                date_of_birth = None
                                                continue

                                            if date_of_birth > date.today():
                                                print(
                                                    f"{invoke_access.ERROR_MESSAGES.get('ERROR_17').title()} ")
                                                date_of_birth = None
                                                continue

                                        except ValueError:
                                            print(
                                                f"{invoke_access.ERROR_MESSAGES.get('ERROR_18').upper()}")

                                    homeAddress = None
                                    while homeAddress is None or not homeAddress.strip():
                                        homeAddress = str(input(
                                            f"{invoke_access.FIELD_LABEL_PROMPTS.get('PROMPT_17')}")).title()
                                        if not homeAddress.strip():
                                            print(
                                                f"{invoke_access.ERROR_MESSAGES.get('ERROR_19').title()}")

                                    contact = None
                                    while contact is None:
                                        contact = input(
                                            f"{invoke_access.FIELD_LABEL_PROMPTS.get('PROMPT_18')}")

                                        if not contact.isdigit():  # must be a digit
                                            print(
                                                f"{invoke_access.ERROR_MESSAGES.get('ERROR_20').title()}")
                                            contact = None

                                        # must be equal to 11 (PH standard +63)
                                        elif len(contact) != 11:
                                            print(
                                                f"{invoke_access.ERROR_MESSAGES.get('ERROR_27').title()}")
                                            contact = None

                                    email_address = None
                                    while email_address is None or not email_address.strip() or not re.match(r"[^@]+@[^@]+\.[^@]+", email_address):
                                        email_address = str(input(
                                            f"{invoke_access.FIELD_LABEL_PROMPTS.get('PROMPT_19')}"))

                                        # email validation
                                        if not email_address.strip() or not re.match(r"[^@]+@[^@]+\.[^@]+", email_address):
                                            print(
                                                f"{invoke_access.ERROR_MESSAGES.get('ERROR_21').title()}")
                                            email_address = None

                                    new_client = BankClient(client_id, first_name.upper(), middle_name.upper(
                                    ), last_name.upper(), date_of_birth, homeAddress, contact, email_address)
                                    self.createNewClient(new_client)
                                    break

                            except ValueError:
                                print(
                                    f"{invoke_access.ERROR_MESSAGES.get('ERROR_05')}")
                                # ... end of client creation block code

                    # FIND THE CLIENT AND DISPLAY ITS DETAILS
                    elif choice == 2:
                        print(f"{invoke_access.HEADER.get('HEADER_05').upper()}")
                        while True:
                            try:
                                client_id = int(
                                    input(f"\n{invoke_access.FIELD_LABEL_PROMPTS.get('PROMPT_20').title()}"))
                                found_client = self.findClient(client_id)

                                if found_client:
                                    found_client.printDetails()
                                    print(
                                        f"{invoke_access.UI_ELEMENTS.get('ELEMENT_01')}\n")
                                    print("=" * len(invoke_access.HEADER.get('HEADER_05')))
                                    break
                                else:
                                    print(
                                        f"Invalid input! Please enter a registered Client ID.")
                                    print(
                                        f"{invoke_access.UI_ELEMENTS.get('ELEMENT_01')}\n")
                                    print("=" * len(invoke_access.HEADER.get('HEADER_05')))
                                    continue

                            except ValueError:
                                print(
                                    f"{invoke_access.FIELD_LABEL_PROMPTS.get('PROMPT_44')}")
                    # ... end of find client block code

                    # UPDATES CLIENTS DETAILS
                    elif choice == 3:
                        print(f"{invoke_access.HEADER.get('HEADER_04').upper()}")
                        isTrue = True
                        while isTrue:
                            try:
                                client_id = int(
                                    input(f"{invoke_access.FIELD_LABEL_PROMPTS.get('PROMPT_21').title()}"))

                                # Check if the entered client ID exists in the database
                                existing_client = self.findClient(client_id)

                                if existing_client:
                                    new_info = self.get_new_client_info()
                                    self.updateClientInformation(
                                        client_id, new_info)
                                    isTrue = False  # Exit the loop when the client ID is valid
                                    print(
                                        "=" * len(invoke_access.HEADER.get('HEADER_04')))
                                else:
                                    print(
                                        f"Client with ID {client_id} not found. Please enter a valid client ID.")
                                    print(
                                        "=" * len(invoke_access.HEADER.get('HEADER_04')))
                            except ValueError:
                                print(
                                    "Invalid input! Please enter a valid client ID.")
                    # ... end of update client details

                    # SHOWS ALL CLIENTS WITH THEIR DETAILS
                    elif choice == 4:
                        print(
                            f"\n{invoke_access.HEADER.get('HEADER_01').upper()}")
                        self.listAllClients()
                        print(
                            "=" * len(invoke_access.HEADER.get('HEADER_01')))
                    # ... endline of showing all clients

                    # REMOVE CLIENT
                    elif choice == 5:
                        print(
                            f"\n{invoke_access.HEADER.get('HEADER_02').upper()}")

                        while True:
                            try:
                                client_id = int(
                                    input(f"\n{invoke_access.FIELD_LABEL_PROMPTS.get('PROMPT_34')} "))
                                self.removeClient(client_id)
                                break

                            except ValueError:
                                print(
                                    f"Invalid input! Please enter a valid client ID.")
                                
                        print("\n")
                        print("=" * len(invoke_access.HEADER.get('HEADER_02')))
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
            print(
                f"An unexpected error occurred in the main menu: {main_menu_error}")

    # ACCOUNT MANAGEMENT MENU
    def accountManagementMenu(self):
        ''' Responsible for managing account-related operations. '''

        # Create a dictionary to map choices to functions
        account_functions = {
            1: self.handle_listing,     # Lists accs with associated client ids
            2: self.handle_show_bal,    # Modular handling of showing balance
            3: self.handle_depositWithdraw,     # Modular handling of deposits and withdraws
            4: self.handle_open_acc,     # Modular handling of opening accs
            5: self.handle_close_acc,   # Modular handling of closing accs
            6: self.handle_exit,   # # Exit function or back to main menu
        }

        while True:
            print('\n\nPREVIOUS_MENU: ', self.previous_menu)
            print('CURRENT_MENU: ', self.current_menu)

            print(f"\n{invoke_access.HEADER.get('HEADER_07').upper()}")

            for key, value in invoke_access.ACCOUNT_MENU_CHOICES.items():   # UI for account_menu
                print(f"[{key}] {value}")

            try:
                choice = int(
                    input(f"\n{invoke_access.FIELD_LABEL_PROMPTS.get('PROMPT_11').title()}"))

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

    def getClientID(self):
        ''' A function dedicated for getting client ID. '''
        while True:
            print(f"{invoke_access.UI_ELEMENTS.get('ELEMENT_08')}")

            try:
                # prompt user to enter client_id
                client_id = int(
                    input(f"{invoke_access.FIELD_LABEL_PROMPTS.get('PROMPT_12')}"))
                print(f"{invoke_access.UI_ELEMENTS.get('ELEMENT_08')}")

                # breaks loop and go back to handle_open_acc function.
                if self.findUnregisteredClientID(client_id):
                    return client_id

                # continues the loop until a registered ClientID (CID) is provided.
                else:
                    continue

            except ValueError as ve:
                print(f"{invoke_access.ERROR_MESSAGES.get('ERROR_05')} {ve}")

    def findUnregisteredClientID(self, client_id):
        # validate before returning
        if self.checkClientIDExistence(client_id):  # clientID is found
            print(f"\nYou are CURRENTLY USING ClientID: {client_id}")
            return client_id

        else:
            print(
                f"\nYou CANNOT USE ClientID: {client_id}, register it first!")
            return None  # Returning None to indicate that the client_id is not valid

    def checkClientIDExistence(self, client_id):
        ''' A function dedicated for validating whether the clientID is on the DB using query. '''
        try:

            query = invoke_access.QUERIES.get(1)
            self.cursor.execute(query, (client_id,))
            count = self.cursor.fetchone()[0]

            # Return True if the clientID exists, otherwise False
            return count > 0

        except Exception as e:
            print(f"{invoke_access.ERROR_MESSAGES.get('ERROR_31')} {e}")

    def handle_open_acc(self):
        ''' Handles the few necessary setups for opening a new account '''
        self.selected_section = "open_account"
        print(f"\n{invoke_access.HEADER.get('HEADER_09').upper()}\n")

        for key, value in invoke_access.OPEN_ACCOUNT_DIALOG.items():
            print(f"[{key}] {value}")

        try:
            # Ask user if they're new or existing client
            isNew = int(
                input(f"\n{invoke_access.FIELD_LABEL_PROMPTS.get('PROMPT_11').title()}"))
            print("\n")

            match isNew:

                case 1:  # if client is new to the system
                    print(
                        f"\n{invoke_access.FIELD_LABEL_PROMPTS.get('PROMPT_35')}")
                    self.previous_menu = self.current_menu
                    self.current_menu = 'client'
                    print("=" * len(invoke_access.HEADER.get('HEADER_09')))
                    self.clientManagementMenu()

                case 0:  # if client chooses existing
                    client_id = self.getClientID()

                    # check first whether the user wants to use the automatic assigning ID feature
                    userPref = self.getUserPreferences()

                    # set the AccID based on the preference user has GIVEN
                    account_id = self.isAutomaticOrManual(userPref)

                    initial_balance = float(input("Enter Initial Balance: "))
                    self.openAccount(account_id, client_id, initial_balance)
                    print("=" * len(invoke_access.HEADER.get('HEADER_09')))

                case _:
                    print(f"{invoke_access.ERROR_MESSAGES.get('ERROR_02')}")
                    # self.previous_menu = self.current_menu
                    self.current_menu = 'account'

        except EOFError:
            print(f"{invoke_access.ERROR_MESSAGES.get('ERROR_29')}")

        except ValueError:
            print("An INPUT MISMATCH has occured.")

    def isAutomaticOrManual(self, userPref):
        ''' This will be the function that will set account ID assigning (automatically or manually) '''
        if userPref.upper() == 'Y':  # Y means automatic

            # Generate a new account_id
            account_id = self.generateNewAccID()
            print(f"{invoke_access.FIELD_LABEL_PROMPTS.get('PROMPT_42')}{account_id} {invoke_access.FIELD_LABEL_PROMPTS.get('PROMPT_43')}")
            return account_id

        elif userPref.upper() == 'N':   # N means manual
            account_id = self.getAccountID()
            return account_id  # return whatever value of accound_id to the handle_open_acc

    def generateNewAccID(self):
        ''' This generates new Account ID based on existing db. '''
        try:
            query = invoke_access.QUERIES.get(5)  # minimum query for db
            self.cursor.execute(query)
            min_account_id = self.cursor.fetchone()[0]

            if min_account_id is not None:
                # If there are skipped and unused account_ids that is available on DB, use it.
                return min_account_id
            else:
                # If there no skipped and unused account_ids.
                query = invoke_access.QUERIES.get(4)  # maximum query for db
                self.cursor.execute(query)
                max_account_id = self.cursor.fetchone()[0]

                # If no existing account_id, start from 1; otherwise, increment by 1
                new_account_id = 1 if max_account_id is None else max_account_id + 1

                return new_account_id

        except Exception as e:
            print(f"{invoke_access.ERROR_MESSAGES.get('ERROR_31')} {e}")

    def getAccountID(self):
        ''' Gets the account ID manually through a PROMPT. '''
        while True:
            print(f"{invoke_access.UI_ELEMENTS.get('ELEMENT_08')}")

            try:
                # prompts user to enter account_id
                account_id = int(
                    input(f"{invoke_access.FIELD_LABEL_PROMPTS.get('PROMPT_42')}"))
                print(f"{invoke_access.UI_ELEMENTS.get('ELEMENT_08')}")

                # breaks loop and go back to handle_open_acc function.
                if self.findUnregisteredAccountID(account_id):
                    return account_id

                # continues the loop until a non-registered AccountID (AID) is provided.
                else:
                    continue

            except EOFError:
                print(f"{invoke_access.ERROR_MESSAGES.get('ERROR_29')}")

            except ValueError as ve:
                print(f"{invoke_access.ERROR_MESSAGES.get('ERROR_05')} {ve}")

    def findUnregisteredAccountID(self, account_id):
        ''' '''
        # validate inputted ID's before returning
        if self.checkAccountIDExistence(account_id):  # clientID is found (

            # since they both benefit from the module checkIDExistence())
            # returns false only if the section selected is open_acc...
            if self.selected_section == 'open_account':
                print(f"\nThis ACCOUNT ID: {account_id} is already TAKEN!!!")
                return None

            else:   # ... else return true
                print(f"\nAccount ID ({account_id}) Validated.")
                return account_id

        else:

            if self.selected_section == "open_account":
                print(f"\nYou've SELECTED AccountID No. {account_id}.")
                return account_id  # Returning None to indicate that the client_id is not valid

            else:
                print(
                    f"\nEntered AccountID {account_id} is NOT YET REGISTERED")
                return None

    def checkAccountIDExistence(self, account_id):
        ''' Check the availability of AccountID is already taken. '''
        try:

            query = invoke_access.QUERIES.get(2)
            self.cursor.execute(query, (account_id,))
            count = self.cursor.fetchone()[0]

            # Return True if the clientID exists, otherwise False
            return count > 0

        except Exception as e:
            print(f"{invoke_access.ERROR_MESSAGES.get('ERROR_31')} {e}")

    def getUserPreferences(self):
        ''' Prompt the user whether to fill the AccountID automatically, or manually. '''
        while True:
            try:
                # append the dictionary to a variable created from another class.
                yes_or_no = invoke_access.YES_OR_NO_DIALOG.items()

                # prints the UI
                print(f"\n{invoke_access.HEADER.get('HEADER_11').title()}")
                for key, value in yes_or_no:
                    # prints the specified UI Dialog
                    print(f"[{key}] : {value}")

                # present a prompt to the user
                choice = str(
                    input(f"\n{invoke_access.FIELD_LABEL_PROMPTS.get('PROMPT_41')} : "))

                # logic for the yes or no dialog
                if choice.upper() == 'Y':
                    # Trigger the switch for automatic assigning of AccID
                    userPref = choice
                    # go back to handle_open_acc mod with a returned value (y)
                    return userPref

                elif choice.upper() == 'N':
                    # Proceed with the manual selection of AccID
                    userPref = choice
                    # go back to handle_open_acc mod with a returned value (n)
                    return userPref

                else:
                    print(f'\n{invoke_access.ERROR_MESSAGES.get("ERROR_30")}')
                    # continues the loop until chose among valid choices.
                    continue

            except EOFError:
                # handles the instances where the user uses Ctrl + Keys on terminal.
                print(f"{invoke_access.ERROR_MESSAGES.get('ERROR_29')}")

            except Exception as e:
                # handle unexpected exceptions
                print(
                    f"{invoke_access.ERROR_MESSAGES.get('ERROR_13').capitalize()} {e}")

    def handle_listing(self):
        ''' Responsible for showing all accounts and associated clients with it in the database. '''
        self.selected_section = "list_all_accounts"
        query = invoke_access.QUERIES.get(3)
        print(f"{invoke_access.HEADER.get('HEADER_10').upper()}")
        self.showAllAccounts(query)

    def showAllAccounts(self, query):
        try:
            self.cursor.execute(query)
            all_accounts_data = self.cursor.fetchall()
            num_rows = len(all_accounts_data)  # Get the number of rows

            if num_rows > 0:
                header_format = "{:<15} {:<}".format(
                    '\nAccount ID', 'Client ID')  # adjusts the header mid gaps
                print(header_format)
                print('-' * (len(header_format) + 5))

                max_name_length = max(
                    len(str(account_data[1])) for account_data in all_accounts_data)
                # adjust the mid gaps between the data entries
                name_format = "{:<14} {:<" + str(max_name_length) + "}"

                for account_data in all_accounts_data:
                    account_id = str(account_data[0])
                    account_name = account_data[1]

                    # Print the data in the dynamically determined column width
                    print(name_format.format(account_id, account_name))
                    print('-' * (29 + max_name_length))

                # Prints the total number of accounts found after the query.
                # Print the total number of accounts
                print(
                    f"{invoke_access.FIELD_LABEL_PROMPTS.get('PROMPT_09')} {num_rows} {invoke_access.FIELD_LABEL_PROMPTS.get('PROMPT_9.6')}\n")
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
                print(
                    f"Database error: {error_msg} (Error code: {error_code})")

        except Exception as e:
            # Handles other unexpected errors
            print(f"Unexpected error: {e}")

    def handle_show_bal(self):
        ''' Handles the displaying of account balance '''
        self.selected_section = "show_acc_balance"

        print(f"{invoke_access.HEADER.get('HEADER_12').upper()}")

        query = invoke_access.QUERIES.get(8)    # query
        client_id = self.getClientID()  # module append to variable
        account_id = self.getAccountID()
        self.showAccountBalance(account_id, client_id, query)

        print('=' * len(invoke_access.HEADER.get('HEADER_12')))

    def handle_depositWithdraw(self):
        ''' Handles depositing and withdrawing of money into an account. '''
        self.selected_section = "deposit/withdraw"

        print(f"{invoke_access.HEADER.get('HEADER_13').upper()}")

        # create a module for getting input (deposit or withdraw)
        self.depositOrWithdraw()

        # this wil recursively get the accID until it is validated.
        account_id = self.getAccountID()

        # prompt to get how much money to deposit or withdraw.
        if self.selected_section == 'deposit_money':
            prompt_deposit = invoke_access.FIELD_LABEL_PROMPTS.get('PROMPT_45')
            amount = self.getAmount(prompt_deposit, account_id)
            self.updateBalance(account_id, amount, update_type='deposit')

        elif self.selected_section == 'withdraw_money':
            prompt_withdraw = invoke_access.FIELD_LABEL_PROMPTS.get(
                'PROMPT_46')
            amount = self.getAmount(prompt_withdraw, account_id)

            self.updateBalance(account_id, amount, update_type='withdraw')

        print("=" * len(invoke_access.HEADER.get('HEADER_13')))

    def getAmount(self, update_type_prompt, account_id):
        ''' A fully modular function for getting how much amount a user would want to deposit or withdraw. '''

        # Retrieve the current account balance
        query = invoke_access.QUERIES.get(11)
        self.cursor.execute(query, (account_id,))
        balance = self.cursor.fetchone()[0]

        balance = float(balance)

        while True:
            try:
                amount = float(input(f"{update_type_prompt}"))

                # this logic only accepts/returns positive float numbers (...)
                if amount > 0:

                    if self.selected_section == "withdraw_money" and float(balance) < amount:
                        print(
                            f"\n{invoke_access.FIELD_LABEL_PROMPTS.get('PROMPT_47')}")
                        continue

                    return amount   # returns only if amount is greater than 0.

                else:   # negative amount forbidden
                    print(f"{invoke_access.ERROR_MESSAGES.get('ERROR_32')}")
                    continue

            except ValueError as ve:
                print(f"\n{invoke_access.ERROR_MESSAGES.get('ERROR_05')} {ve}")
                continue

    def depositOrWithdraw(self):
        ''' Ask user to choose between two choices presented as dialog. '''
        for key, value in invoke_access.DEPOSIT_WITHDRAW_DIALOG.items():
            print(f"[{key}] : {value}")

        while True:

            try:
                choice = str(
                    input(f"\n{invoke_access.FIELD_LABEL_PROMPTS.get('PROMPT_11')}"))

                if choice.upper() == "D":
                    self.selected_section = 'deposit_money'
                    print(f"\n{invoke_access.HEADER.get('HEADER_14').upper()}")
                    break

                elif choice.upper() == "W":
                    self.selected_section = 'withdraw_money'
                    print(f"\n{invoke_access.HEADER.get('HEADER_15').upper()}")
                    break

                else:
                    print(invoke_access.ERROR_MESSAGES.get('ERROR_02'))
                    continue

            except EOFError as eofe:
                print(f"{invoke_access.ERROR_MESSAGES.get('ERROR_02')} {eofe}")
                continue

            except ValueError as ve:
                print(f"{invoke_access.ERROR_MESSAGES.get('ERROR_29')} {eofe}")
                continue

    def handle_close_acc(self):
        ''' Handles closing an account. '''
        self.selected_section = "close_account"
        print(f"{invoke_access.HEADER.get('HEADER_16').upper()}")

        while True:  # outer loop
            # get accID to delete.
            account_id = self.getAccountID()

            while True:  # inner loop
                # Let the user confirm their actions by employing a confirmation dialog and prompt.
                is_confirm = self.confirmDeletion(account_id)

                if is_confirm == 'CONFIRM':
                    # Check account balance first.
                    query = invoke_access.QUERIES.get(11)
                    self.cursor.execute(query, (account_id,))
                    balance = self.cursor.fetchone()[0]

                    if balance != 0:
                        print(
                            f"\n{invoke_access.UI_ELEMENTS.get('ELEMENT_09')}\nYou cannot CLOSE an ACCOUNT with REMAINING BALANCE : ₱{balance:,.2f}")
                        self.deleteAgain()

                        # break out the first loop (inner loop)
                        break

                    else:
                        # commence query for deletion after balance validation.
                        self.closeAccount(account_id)

                        # prompt if want to delete again.
                        self.deleteAgain()
                        break

                elif is_confirm.upper() == 'BACK':
                    # A back button to change Account To Be Deleted.
                    print(f"{invoke_access.UI_ELEMENTS.get('ELEMENT_09')}   ")
                    break

                elif is_confirm == 'confirm':
                    print(
                        f"\n{invoke_access.UI_ELEMENTS.get('ELEMENT_09')}\nPlease MAKE SURE to write all in CAPITAL LETTERS.")
                    continue

                else:
                    print(
                        f"\n{invoke_access.UI_ELEMENTS.get('ELEMENT_09')}\nPlease READ THOROUGHLY, before SMASHING. :)")
                    continue

            if self.selected_section == "get_account":
                continue

            elif self.selected_section == "account":
                print(f"=" * len(invoke_access.HEADER.get('HEADER_16')))
                break
        # self.closeAccount(account_id)

    def deleteAgain(self):
        ''' A function for telling the computer if deletion should continue or not. '''
        while True:

            print(str(f"\n{invoke_access.HEADER.get('HEADER_17')}").upper())
            for key, value in invoke_access.YES_OR_NO_DIALOG.items():
                print(f"{key} : {value}")

            try:
                choice = str(
                    input(f"\n{invoke_access.FIELD_LABEL_PROMPTS.get('PROMPT_11')}")).upper()

                if choice == 'Y':
                    self.selected_section = "get_account"
                    break

                elif choice == 'N':
                    self.selected_section = "account"
                    break

                else:
                    continue

            except EOFError as eofe:
                print(f"{invoke_access.ERROR_MESSAGES.get('ERROR_29')} {eofe}")

            except Exception as e:
                print(f"{invoke_access.ERROR_MESSAGES.get('ERROR_13')} {e}")

    def confirmDeletion(self, account_id):
        ''' Confirms the action of deletion. '''
        self.selected_function = "close_account"

        print(f"\n{invoke_access.UI_ELEMENTS.get('ELEMENT_06')}→ You are ABOUT TO DELETE AccountID #{account_id} ←{invoke_access.UI_ELEMENTS.get('ELEMENT_06')}\n")

        for key, value in invoke_access.CONFIRM_DELETION_DIALOG.items():
            if key == 3:
                print("\n")
            print(f"({key}.) : {value}")

        try:
            choice = str(input(
                f"\n[DELETING IN PROCESS] {invoke_access.FIELD_LABEL_PROMPTS.get('PROMPT_48')} : \n{invoke_access.UI_ELEMENTS.get('ELEMENT_09')}\n\n\t\t\t"))
            return choice

        except EOFError as eofe:
            print(f"\n{invoke_access.ERROR_MESSAGES.get('ERROR_13')} {eofe}")

        except Exception as e:
            print(f"\n{invoke_access.ERROR_MESSAGES.get('ERROR_13')} {e}")

    def handle_exit(self):
        '''This function does nothing and serves as an exit point for the loop. '''
        self.selected_section = "back_to_main_menu"

        try:
            self.previous_menu = self.current_menu
            self.current_menu = 'main_menu'
            self.mainMenu()
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    while True:
        try:
            bank_system = BankSystem()
            bank_system.mainMenu()
        except KeyboardInterrupt:
            print("Keyboard suddenly interrupted, but we're continuing :>")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
