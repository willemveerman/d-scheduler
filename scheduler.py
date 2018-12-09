import argparse
import re
import random

parser = argparse.ArgumentParser(description=
                                 """
                                 Takes a text file listing activities 
                                 and a number as input 
                                 and produces a schedule 
                                 for said number of teams.
                                 """)
class Schedule():

    def __init__(self):
        self.events = []

    def total(self):
        return sum([event[1] for event in self.events])

class Scheduler():

    def file_parser(self, path):

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

    def scheduler(self, teams):

        activities = self.file_parser('activities.txt')

        schedules = []

        lunch = ('Lunch Break', 60)

        for _ in range(teams):
            schedules.append(Schedule())

        for index, schedule in enumerate(schedules):
            while schedule.total() < 420:
                if schedule.total() > 150 and lunch not in schedule.events:
                    schedule.events.append(lunch)
                event = random.choice(activities.items())
                others = schedules[:index]+schedules[index+1:]
                if event not in schedule.events:
                    if event not in self.overlaps(schedule.total(), schedule.total()+event[1], others):
                        schedule.events.append(event)

        return schedules


a = Scheduler()

activities = a.file_parser('activities.txt')

sch = Schedule()

teams = 12

b = a.scheduler(teams)

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