import argparse
import re
import random
import datetime as dt

parser = argparse.ArgumentParser(description=
                                 """
                                 Takes as input a text file listing activities 
                                 and a number,  
                                 and produces an activity schedule 
                                 for said number of teams.
                                 """)
class Schedule():
    """A class for storing a schedule for a single team"""
    def __init__(self):
        self.events = []

    def total(self):
        """Returns the total duration of all activities in the object"""
        return sum([event[1] for event in self.events])

class Scheduler():

    def file_parser(self, path):
        """Parse a file and return a dict of str(activity):int(duration)"""
        with open(path) as f:
            content = f.readlines()

        activities = {}

        for line in content:
            components = re.split('\s(\w+)$', line)  # get the last term, e.g. '60min'
            if components[1] == 'sprint':
                activities[components[0]] = 15
            else:
                activities[components[0]] = int(re.findall('\d+',components[1])[0])  # get the numbers only

        return activities

    def overlaps(self, start, end, schedules):
        """Find in schedules all activities that overlap with a given start and end time"""
        section_duration = 0

        events = []

        for schedule in schedules:
            for event in schedule.events:
                section_duration += event[1]
                if section_duration > start:
                    events.append(event)
                if section_duration >= end:
                    section_duration = 0
                    break

        return events

    def scheduler(self, teams, activities):
        """Given n teams and a list of activites and their durations, produce a schedule
           for each team that does not overlap with that of any other team"""
        if teams > 13:
            return "You cannot divide into more than 13 teams without overlaps (if you want to avoid gaps)"

        act_copy = activities.items()

        schedules = []

        lunch = ('Lunch Break', 60)

        for _ in range(teams):
            schedules.append(Schedule())

        for index, schedule in enumerate(schedules):
            while schedule.total() < 420:  # arbitrary
                if schedule.total() > 150 and lunch not in schedule.events:  # arbitrary
                    schedule.events.append(lunch)
                try:
                    event = activities.popitem()  # ensure that every activity is tried at least once
                except KeyError:
                    event = random.choice(act_copy)
                others = schedules[:index]+schedules[index+1:]  # every schedule except the one in the loop
                if event not in schedule.events:
                    if event not in self.overlaps(schedule.total(), schedule.total()+event[1], others):
                        schedule.events.append(event)

        return schedules

    def output(self, schedules):

        def make_schedule(schedule):

            time = dt.time(9)

            lines = []

            for event in schedule.events:
                lines.append(time+dt.time.min(), event[0], event[1])



a = Scheduler()

teams = 14

b = a.scheduler(teams, a.file_parser('activities.txt'))

for i in b:
    print i.events, i.total()


# schedules = []
# for _ in range(teams):
#     instance = Schedule()
#     schedules.append(instance)
# for schedule in schedules:
#     act = random.choice(activities.items())
#     schedule.events_list.append(act)
#
# for b in schedules:
#     print b.events_list


# def iterator(schedule):
#