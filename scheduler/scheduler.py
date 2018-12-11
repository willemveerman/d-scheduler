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

        events = []

        for schedule in schedules:
            section_duration = 0
            for event in schedule.events:
                section_duration += event[1]
                if section_duration > start:
                    events.append(event)
                if section_duration >= end:
                    break

        return events

    def scheduler(self, teams, path, risky=False):
        """
        Produces schedules for n teams from an activities file.
        The activities in each team's schedule don't overlap with those of any other.

        :param teams: int
        :param path: str
        :param risky: bool
        :return: list
        """

        if teams > 9 and not risky:
            raise ValueError("""Scheduling for 10 or more teams with the current set of activities 
                                can cause performance problems.
                                Scheduling for more than 13 is impossible (wihtout gaps)
                                Remove this warning by passing risky=True.""")

        activities = self.file_parser(path)

        act_copy = activities.items()

        lunch = ('Lunch Break', 60)

        schedules = []

        for _ in range(teams):
            schedules.append(Schedule())

        for index, schedule in enumerate(schedules):
            while schedule.total() <= 420:
                if schedule.total() > 120 and lunch not in schedule.events:
                    schedule.events.append(lunch)
                try:
                    event = activities.popitem()  # ensure that every activity is tried at least once
                except KeyError:
                    event = random.choice(act_copy)
                others = schedules[:index]+schedules[index+1:]  # every schedule except the one in the loop
                if event not in schedule.events:
                    if event not in self.overlaps(schedule.total(), schedule.total()+event[1], others):
                        schedule.events.append(event)
                    else:
                        pass

        return schedules

    def make_schedule(self, schedule):
        """
        Produces a formatted schedule from a Schedule() object

        :param schedule: Schedule()
        :return: list
        """

        nine = dt.datetime(2018,12,10,9)  # 9AM

        elapsed = 0

        formatted_schedules = []

        for event in schedule.events:
            time = nine + dt.timedelta(minutes=elapsed)
            elapsed += event[1]
            if event[1] == 15:
                event = (event[0], "sprint")
            else:
                event = (event[0], str(event[1])+"min")
            formatted_schedules.append(time.strftime('%I:%M %p : ') + event[0] + " " + event[1])

        five = dt.datetime(2018, 12, 10, 17)  # 5PM
        formatted_schedules.append(five.strftime('%I:%M %p : ') + "Staff Motivation Presentation")

        return formatted_schedules


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

