#user_profile.py



class User:
    name = "Andre Ehrlich"
    school = "Northwestern"
    timezone = "-6:00"


    def __init__(self, name, email, school, timezone):
        self.name = name
        self.school = school
        self.timezone = timezone
        self.emailaddress = email
    def __repr__(self):
        return """ {}, {}""".format(self.name, self.school) #, self.timezone)

user_dict = {
    "Andre": User("Andre Ehrlich", "ehrlichandre@gmail.com", "Northwestern", "-6:00"),
    "Joe": User("Joe Chookaszian", "joeisdumb@gmail.com", "Northwestern", "-8:00"),
}

# print(user_dict['Andre'])
