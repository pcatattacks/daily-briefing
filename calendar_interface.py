# Daily Breifing: Functional Architecture for Google Calendar

# Each Calendar is a list of Events
class Calendar:

    # events is a dictionary, of arrays
    events = {
        "daily": [], # List of events
        # "weekly": [], # list of days
        # "monthly": [] # list of weeks
        }

    # Reads out events of the Day
    # Time, Title, (maybe, Description and participants, or leave out til they ask)
    def get_daily_briefing(self):
        return 0

    # Keyword match to events in daily calendar.
    def tell_me_more_about_event(self, keywords_to_match, part_of_event):
        return 0


# Event is an object
class Event:

    time = "" # what format is time? UTC
    title = ""
    location = "" # (address)
    description = ""
    link = ""
    participants = []

    def __init__(self, time, title, location, description, link, participants):
        if time:
            self.time = time
        if title:
            self.title = title
        if location:
            self.location = location
        if description:
            self.description = description
        if link:
            self.link = link
        if participants:
            self.participants = participants
