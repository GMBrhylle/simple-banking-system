class BankClient:
    def __init__(self, client_id, first_name, middle_name, last_name, date_of_birth, homeAddress, contact, email_address):
        self.client_id = client_id
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.homeAddress = homeAddress
        self.contact = contact
        self.email_address = email_address
        self.type_of_id_1 = None
        self.type_of_id_2 = None

    def printDetails(self):
        print(f"\nClient ID: {self.client_id}")
        print(f"Name: {self.first_name} {'' if self.middle_name == 'NULL' else self.middle_name} {self.last_name}")
        print(f"Date of Birth: {self.date_of_birth}")
        print(f"Address: {self.homeAddress}")
        print(f"Contact Number: {self.contact}")
        print(f"Email Address: {self.email_address}")
        print(f"Type of ID 1: {self.type_of_id_1}")
        print(f"Type of ID 2: {self.type_of_id_2}")
