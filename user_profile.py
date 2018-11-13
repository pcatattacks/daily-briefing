#user_profile.py



class User:
    name = "Andre Ehrlich"
    school = "Northwestern"
    timezone = "-6:00"


    def __init__(self, name, school, timezone):
        self.name = name
        self.school = school
        self.timezone = timezone

    def __repr__(self):
        return """ {}, {}""".format(self.name, self.school) #, self.timezone)

user_dict = {
    "Andre": User("Andre Ehrlich", "Northwestern", "-6:00"),
    "Joe": User("Joe Chookaszian", "Northwestern", "-8:00"),
}

# print(user_dict['Andre'])
