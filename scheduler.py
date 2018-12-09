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
        self.events_list = []

    def total(self):
        return sum([event[1] for event in self.events_list])


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

    def overlapping_events(self, start, end, schedule):

        section_duration = 0

        events = []

        for event in schedule.events_list:
            section_duration += event[1]
            if section_duration > start:
                events.append(event)
            if section_duration >= end:
                break

        return events

    def scheduler(self, teams):

        activities = self.file_parser('activities.txt')

        schedules = []

        lunch = ('Lunch', 60)

        for _ in range(teams):
            schedules.append(Schedule())

        for index, schedule in enumerate(schedules):
            while schedule.total() < 420:
                if schedule.total() > 150 and lunch not in schedule.events_list:
                    schedule.events_list.append(lunch)
                    continue
                act = random.choice(activities.items())
                others = schedules[:index]+schedules[index+1:]
                if act not in schedule.events_list:
                    if act not in [self.overlapping_events(schedule.total(), schedule.total()+act[1], s) for s in others]:
                        schedule.events_list.append(act)
                    else:
                        break
                    # elif s[-1] != act and s[-1][1] >= act[1]:
                    #     schedule.append(act)

                    # for s in schedules[index:] + schedules[:index + 1]:
                    #     if sum([event[1] for event in schedule]) > sum([event[1] for event in s]):
                    #         schedule.append(act)
                    #     elif s[-1] != act and s[-1][1] >= act[1]:
                    #         schedule.append(act)


        # for schedule in schedules:
        #     activity_pool = activities
        #     while sum([event[1] for event in schedule]) < 420:
        #         try:
        #             new_item = activity_pool.popitem()
        #             if new_item not in schedule:
        #                 schedule.append(new_item)
        #         except KeyError as e:
        #             break

        # while sum([event[1] for event in s for s in schedules]) < 420:
        #     if 135 < sum([event[1] for event in schedule for schedule in schedules]) < 180:
        #         schedule.append(('Lunch', 60))
        #     elif sum([event[1] for event in schedule for schedule in schedules]) < 120:
        #         schedule.append(activities.popitem())


        return schedules

a = Scheduler()

activities = a.file_parser('activities.txt')

sch = Schedule()

teams = 6

b = a.scheduler(teams)

for i in b:
    print i.events_list, i.total()



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