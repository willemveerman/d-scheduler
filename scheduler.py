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

parser.add_argument('-i', '--input',
                    help='path to the input file')

parser.add_argument('-r', '--region',
                    default='eu-west-2',
                    help='AWS region')

parser.add_argument('-n', '--name',
                    default='*',
                    help='EC2 instance name')

class Schedule():
    """A schedule for a single team"""
    def __init__(self):
        self.events = []

    def total(self):
        """The total duration of all activities in the schedule"""
        return sum([event[1] for event in self.events])

class Scheduler():

    def file_parser(self, path):
        """
        Returns a dict of str(activity):int(duration)

        Parameters
        ----------
        path : str
        """
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
        """
        Find in schedules all activities that overlap with a given start and end time

        Parameters
        ----------
        start, end : int
        schedules : list
        """
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
        """
        Given n teams and a dict of activites and their durations, produce a schedule
        for each team that does not overlap with that of any other team

        Parameters
        ----------
        teams : int
        activities : dict
        """
        if teams > 13:
            return "You cannot divide into more than 13 teams without overlaps (if you want to avoid gaps)"

        act_copy = activities.items()

        lunch = ('Lunch Break', 60)

        schedules = []

        for _ in range(teams):
            schedules.append(Schedule())

        for index, schedule in enumerate(schedules):
            while schedule.total() < 420:  # arbitrary
                if schedule.total() > 120 and lunch not in schedule.events:  # arbitrary
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

teams = 6

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