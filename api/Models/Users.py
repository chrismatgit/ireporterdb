class User:
    accounts = []
    def __init__(self, firstname, lastname, othernames, email, phone_number, username, password, registered, user_id):
            self.user_id = user_id
            self.firstname = firstname
            self.lastname = lastname
            self.othernames = othernames
            self.email = email
            self.phone_number = phone_number
            self.username = username
            self.password = password
            self.registered = registered
            self.isadmin = False