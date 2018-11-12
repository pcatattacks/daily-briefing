#user_profile.py



class User:
    name = "Andre Ehrlich"
    school = "Northwestern"
    timezone = "gmt-8:00"


    def __init__(self, name, school, timezone):
        self.name = name
        self.school = school
        self.timezone = timezone


Andre = User()

print(Andre)
