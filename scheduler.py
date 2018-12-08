import argparse
import re

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
            components = re.split('\s(\w+)$', line) #get the last term, e.g. '60min'
            if components[1] == 'sprint':
                activities[components[0]] = 15
            else:
                activities[components[0]] = int(re.findall(r'\d+',components[1])[0]) #get the numbers only

        return activities

    def schedule(self, teams):

        activities = self.file_parser('activities.txt')

        schedules = []
        for _ in range(teams):
            schedules.append([])

        for schedule in schedules:
            schedule.append(activities.popitem())

        for schedule in schedules:
            activity_pool = activities
            while sum([event[1] for event in schedule]) < 420:
                try:
                    new_item = activity_pool.popitem()
                    if new_item not in schedule:
                        schedule.append(new_item)
                except KeyError as e:
                    break

        # while sum([event[1] for event in s for s in schedules]) < 420:
        #     if 135 < sum([event[1] for event in schedule for schedule in schedules]) < 180:
        #         schedule.append(('Lunch', 60))
        #     elif sum([event[1] for event in schedule for schedule in schedules]) < 120:
        #         schedule.append(activities.popitem())


        return schedules

a = Scheduler()

print a.file_parser('activities.txt')


