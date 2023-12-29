class StringConstant:

    UI_ELEMENTS = {
    }

    def drawLine(type_of_line, total):
        ''' A reusable function to draw a series of line for UI. '''
        draw_results = type_of_line * total + ''
        return draw_results

    # Generate repetitive dashes and assign them to each respective dictionary "keys"
    UI_ELEMENTS['ELEMENT_01'] = drawLine('-', 38) # long dash line
    UI_ELEMENTS['ELEMENT_02'] = drawLine('=', 7) # header short dash lines
    UI_ELEMENTS['ELEMENT_03'] = drawLine('-', 7) # short dash line
    UI_ELEMENTS['ELEMENT_04'] = drawLine('=', 21) # header long dash lines
    UI_ELEMENTS['ELEMENT_05'] = drawLine('-', 24)
    UI_ELEMENTS['ELEMENT_06'] = drawLine(' ', 4) # spaces
    UI_ELEMENTS['ELEMENT_07'] = drawLine(' ', 12)

    def drawNotAvailable(type_menu):
        box_size = 5
        text_to_display = f"No {type_menu} are found."

        # Calculate left padding to center the box
        left_padding = (30 - box_size * 4) // 2  # Assuming terminal width is 30 characters
        print("\n")
        for i in range(box_size):
            # Print left padding
            print(" " * left_padding, end="")

            for j in range(box_size):
                if i == j or i + j == box_size - 1:
                    print("XXXX", end="")
                else:
                    print(" ", end="")  # Four spaces

            # Print text ONLY in the center row
            if i == box_size // 2:
                print(f"{text_to_display}", end="")

            print("")
        print("\n")

    

    HEADER = {
        'HEADER_01': f'\n{UI_ELEMENTS.get("ELEMENT_04")} displaying all clients {UI_ELEMENTS.get("ELEMENT_04")}',
        'HEADER_02': f'\n{UI_ELEMENTS.get("ELEMENT_02")} removing clients {UI_ELEMENTS.get("ELEMENT_02")}',
        'HEADER_03': f'\n{UI_ELEMENTS.get("ELEMENT_02")} creating client entry {UI_ELEMENTS.get("ELEMENT_02")}',
        'HEADER_04': f'\n{UI_ELEMENTS.get("ELEMENT_02")} updating client entry {UI_ELEMENTS.get("ELEMENT_02")}',
        'HEADER_05': f'\n{UI_ELEMENTS.get("ELEMENT_02")} searching client entry {UI_ELEMENTS.get("ELEMENT_02")}',
        'HEADER_06': f'\n--> client management <--',
        'HEADER_07': f'\n--> account management <--',
        'HEADER_08': f'\t⌂ main menu ⌂',
        'HEADER_09': f'{UI_ELEMENTS.get("ELEMENT_04")} opening an account {UI_ELEMENTS.get("ELEMENT_04")}',
        'HEADER_10': f'\n{UI_ELEMENTS.get("ELEMENT_02")} displaying all accounts {UI_ELEMENTS.get("ELEMENT_02")}',
        'HEADER_11': f'{UI_ELEMENTS.get("ELEMENT_06")}→ automatic assign id ←{UI_ELEMENTS.get("ELEMENT_06")}',
    }

    FIELD_LABEL_PROMPTS = {
        'PROMPT_01': 'Select a Type of ID:',
        'PROMPT_02': 'Terminating the program...',
        'PROMPT_03': 'One (1) valid ID is acceptable if the ID is a Passport, Driver’s License, PRC ID, UMID, SSS ID, PhilSys ID, or School ID (for minors).',
        'PROMPT_04': 'Enter the number corresponding to the Type of ID: ',
        'PROMPT_05': 'Please provide at least one more valid ID from the accepted list:',
        'PROMPT_06': 'Enter the number corresponding to the Type of ID: ',
        'PROMPT_07': 'Client added successfully!',
        'PROMPT_08': 'Client information updated successfully!',
        'PROMPT_09': 'A total of',
        'PROMPT_9.5': 'client(s) is FOUND.',
        'PROMPT_9.6': 'account(s) is FOUND',
        'PROMPT_10': 'Client with an ID [',
        'PROMPT_10.5': '] has been removed successfully!',
        'PROMPT_11': 'enter your choice: ',
        'PROMPT_12': 'Enter Client ID * : ',
        'PROMPT_13': 'Enter First Name * : ',
        'PROMPT_14': 'Enter Middle Name : ',
        'PROMPT_15': 'Enter Last Name * : ',
        'PROMPT_16': 'Enter Date of Birth (YYYY-MM-DD) * : ',
        'PROMPT_17': 'Enter your Home Address * : ',
        'PROMPT_18': 'Enter Contact Number * :  ',
        'PROMPT_19': 'Enter Email Address * : ',
        'PROMPT_20': 'Enter Client ID to FIND: ',
        'PROMPT_21': 'Enter Client ID to UPDATE: ',
        'PROMPT_22': 'Enter the information you want to UPDATE (leave blank if not updating): ',
        'PROMPT_23': 'Client with ID',
        'PROMPT_24': 'not found in the database.',
        'PROMPT_25': 'No FIELDS are UPDATED.',
        'PROMPT_26': 'Client with an ID',
        'PROMPT_27': 'updated successfully.',
        'PROMPT_28': 'New First Name',
        'PROMPT_29': 'New Middle Name',
        'PROMPT_30': 'New Last Name',
        'PROMPT_31': 'New Home Address',
        'PROMPT_32': 'New Contact Number',
        'PROMPT_33': 'New Email',
        'PROMPT_34': 'Enter Client ID to REMOVE:',
        'PROMPT_35': UI_ELEMENTS.get('ELEMENT_07') + 'select "1" to create '.title() + 'your client id'.upper() + UI_ELEMENTS.get('ELEMENT_07'),
        'PROMPT_36': 'press'.title() + 'esc'.upper() + 'to cancel'.title(),
        'PROMPT_37': 'This' + " decision".upper() + " cannot be " + "reversed : ".upper(),
        'PROMPT_38': 'Y : ' + 'yes'.title() + ' to ' + 'confirm'.upper(),
        'PROMPT_39': 'any'.title() + ' : Key to ' + 'cancel'.upper(),
        'PROMPT_40': 'operation'.title() + ' has been ' + 'cancelled'.upper(),
        'PROMPT_41':'Turn ON the AUTOMATIC ASSIGN of ID?"',
        'PROMPT_42': 'Enter Account ID * : ',
        'PROMPT_43': '(autofilled by system)',
        'PROMPT_44' : 'Input mismatch occured, please try again.',
    }
    
    ERROR_MESSAGES = {
        'ERROR_01': 'Error:',
        'ERROR_02': 'Invalid choice. Please try again.',
        'ERROR_03': 'Invalid selection. Client creation failed.',
        'ERROR_04': 'Invalid selection. Please enter a valid number.',
        'ERROR_05': 'Error: Number only is PERMITTED.',
        'ERROR_06': 'Error inserting client data: ',
        'ERROR_07': 'Error fetching accepted ID types: ',
        'ERROR_08': 'Error searching for client: ',
        'ERROR_09': 'Client with an ID:',
        'ERROR_9.5': 'not found, and IS AVAILABLE.',
        'ERROR_10': 'Error updating client information:',
        'ERROR_11': 'Something went wrong when displaying CLIENTS',
        'ERROR_12': 'Caught an error WHILE REMOVING ClientID (',
        'ERROR_12.5': ') on the SYSTEM:',
        'ERROR_13': 'An unexpected error occurred:',
        'ERROR_14': 'REQUIRED: Please enter your First Name',
        'ERROR_15': 'REQUIRED: Please enter your Last Name',
        'ERROR_16': 'Error: The year should not be greater than the current year',
        'ERROR_17': 'Error: The date should not be greater than the current date',
        'ERROR_18': 'ERROR: FORMAT SHOULD BE YYYY-MM-DD',
        'ERROR_19': 'Error: Please enter your HOME ADDRESS',
        'ERROR_20': 'Error: Contact Number expects an integer',
        'ERROR_21': 'Error: Please ENTER a VALID Email Address "@"',
        'ERROR_22': 'Error: Error updating client information:',
        'ERROR_23': 'Dupe found: '.upper() + 'your input('.capitalize(),
        'ERROR_24': ') is' + ' not available'.upper(),
        'ERROR_25': 'REQUIRED: Please enter your Middle Name',
        'ERROR_26': 'invalid email error: '.upper() + ' Please enter a valid email.',
        'ERROR_27': 'Length ' + 'must '.upper() + ' be 11 digits.',
        'ERROR_28': 'Error',
        'ERROR_29': 'Input has been' + ' interrupted, '.upper() + 'please try again.'.lower(),
        'ERROR_30': 'Only "Y" and "N" (not case-sensitive)',
        'ERROR_31': 'Error executing such query:',
        # Add more error messages here as needed
    }
    
    MAIN_MENU_CHOICES = {
        '1': 'Client Management',
        '2': 'Account Management',
        'Q': 'Quit'
    }

    CLIENT_MENU_CHOICES = {
        1: 'Create/Add New Client',
        2: 'Find Client',
        3: 'Update Client Information',
        4: 'List All Client',
        5: 'Remove Client',
        6: 'Back to Main Menu'
    }

    ACCOUNT_MENU_CHOICES = {
        1: "Show All Accounts",
        2: 'Show Account Balance',
        3: 'Deposit Money',
        4: 'Withdraw Money',
        5: 'Open Account',
        6: 'Close Account', 
        7: 'Back to Main Menu'
    }

    OPEN_ACCOUNT_DIALOG = {
        0: 'EXISTING Client', 
        1: 'NEW Client',
    }

    YES_OR_NO_DIALOG = {
        'Y': 'Yes',
        'N': 'No'
    }

    QUERIES = {
        1: "SELECT COUNT(*) FROM client WHERE clientID = %s",
        2: "SELECT COUNT(*) FROM account WHERE AccountID = %s",
        3: "SELECT * FROM ACCOUNT",
        4: "SELECT MAX(AccountID) FROM account",
        5: "SELECT MIN(AccountID) FROM account WHERE AccountID NOT IN (SELECT AccountID FROM Account)",
        6: "SELECT AccountID FROM account",
        7: "DELETE FROM account WHERE AccountID = %s"
    }