import re
import random
import datetime as dt

class Schedule:
    """
    A schedule for a single team
    """

    def __init__(self):
        self.agenda = []

    def total(self):
        """
        Returns the total duration of all activities in the schedule

        :return: int
        """
        return sum([event[1] for event in self.agenda])


class Scheduler:

    def __init__(self):
        self.recursion_count = 0

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
            for event in schedule.agenda:
                section_duration += event[1]
                if section_duration > start:
                    events.append(event)
                if section_duration >= end:
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
        activities = self.file_parser(path).items()

        if teams > 14 and len(activities) == 20 and ('Archery', 45) in activities:
            raise ValueError("Scheduling for more than 14 teams with the current set of activities is impossible.")

        random.shuffle(activities)
        
        lunch = ('Lunch Break', 60)

        schedules = []

        for _ in range(teams):
            schedules.append(Schedule())

        for index, schedule in enumerate(schedules):
            while schedule.total() <= 420:
                if schedule.total() > 120 and lunch not in schedule.agenda:
                    schedule.agenda.append(lunch)
                for activity in activities:
                    overlapping_events = self.overlaps(schedule.total(), schedule.total()+activity[1], schedules[:index])
                    if activity not in schedule.agenda and activity not in overlapping_events:
                        schedule.agenda.append(activity)
                        break
                else:
                    self.recursion_count += 1
                    if self.recursion_count > 990:
                        raise OverflowError("""The operation recursed 990 times and hence it was stopped
                                                as it was in danger of exceeding python's recursion
                                                depth limit of 1000 and crashing.""")
                    return self.scheduler(teams, path)

        return schedules

    def make_schedule(self, schedule):
        """
        Produces a formatted schedule from a Schedule() object

        :param schedule: Schedule()
        :return: list
        """

        time = dt.datetime(2018,12,10,9)  # 9AM

        formatted_schedules = []

        for event in schedule.agenda:
            duration = event[1]
            if event[1] == 15:
                event = (event[0], "sprint")
            else:
                event = (event[0], str(event[1])+"min")
            formatted_schedules.append(time.strftime('%I:%M %p : ') + event[0] + " " + event[1])
            time = time + dt.timedelta(minutes=duration)

        formatted_schedules.append('05:00 PM : Staff Motivation Presentation')

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
