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

class Scheduler():

    def file_parser(self, path):

        with open(path) as file:
            content = file.readlines()

        activities = {}

        for line in content:
            components = re.split('\s(\w+)$', line)  # get the last term, e.g. '60min'
            if components[1] == 'sprint':
                activities[components[0]] = 15
            else:
                activities[components[0]] = int(re.findall(r'\d+',components[1])[0])  # get the numbers only

        return activities

    def schedule(self, teams):

        activities = self.file_parser('activities.txt')

        schedules = []
        for _ in range(teams):
            schedules.append([])

        for schedule in schedules:
            schedule.append(random.choice(activities.items()))

        for index, schedule in enumerate(schedules):
            while sum([event[1] for event in schedule]) < 420:
                act = random.choice(activities.items())
                if act not in schedule:
                    for s in schedules[index:] + schedules[:index + 1]:
                        if sum([event[1] for event in schedule]) > sum([event[1] for event in s]):
                            schedule.append(act)
                        elif s[-1] != act and s[-1][1] >= act[1]:
                            schedule.append(act)

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

a.file_parser('activities.txt')


