import argparse
import re
import random
import datetime as dt

class Schedule():
    """
    A schedule for a single team
    """

    def __init__(self):
        self.events = []

    def total(self):
        """
        Returns the total duration of all activities in the schedule

        :return: int
        """
        return sum([event[1] for event in self.events])


class Scheduler():

    def file_parser(self, path):
        """
        Returns a dict of str(activity):int(duration) from a file of activities

        :param path: str
        :return: dict
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
        Returns all activities in schedules that overlap with a given start and end time

        :param start: int
        :param end: int
        :param schedules: list
        :return: list
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

    def scheduler(self, teams, path):
        """
        Produces schedules for n teams from an activities file.
        The activities in each team's schedule don't overlap with those of any other.

        :param teams: int
        :param path: str
        :return: list
        """

        activities = self.file_parser(path)

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

    def make_schedule(self, schedule):
        """
        Produces a formatted schedule from a Schedule() object

        :param schedule: Schedule()
        :return: list
        """

        nine = dt.datetime(2018,12,10,9)  # 9AM

        elapsed = 0

        agenda_strings = []

        for event in schedule.events:
            time = nine + dt.timedelta(minutes=elapsed)
            elapsed += event[1]
            if event[1] == 15:
                event = (event[0], "sprint")
            else:
                event = (event[0], str(event[1])+"min")
            agenda_strings.append(time.strftime('%I:%M %p : ') + event[0] + " " + event[1])

        five = dt.datetime(2018, 12, 10, 17)  # 5PM
        agenda_strings.append(five.strftime('%I:%M %p : ') + "Staff Motivation Presentation")

        return agenda_strings


    def output(self, schedules):
        """
        Prints a list of formatted schedules

        :param schedules: list
        """

        for index, schedule in enumerate(schedules):
            print
            print "Team "+str(index+1)+":"
            for activity in self.make_schedule(schedule):
                print activity



a = Scheduler()

teams = 12

b = a.scheduler(teams, 'activities.txt')

#print a.output(b)

print a.make_schedule(b[1])


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