import unittest
from scheduler import Scheduler, Schedule

class SchedulerTestCase(unittest.TestCase):
    def setUp(self):
        self.scheduler = Scheduler()

        self.schedules = self.scheduler.scheduler(10, 'activities.txt')

        self.schedules_1 = Schedule()
        self.schedules_2 = Schedule()

        self.schedules_1.agenda = [('Giant Puzzle Dinosaurs', 30), ('Enigma Challenge', 45), ('Human Table Football', 30)]
        self.schedules_2.agenda = [('Salsa & Pickles', 15), ('Indiano Drizzle', 45), ('Buggy Driving', 30)]

class TestSchedulerFileParser(SchedulerTestCase):
    def test_file_parser_type(self):
        self.assertTrue(isinstance(self.scheduler.file_parser('../scheduler/activities.txt'), dict))

    def test_file_parser_parse(self):
        self.assertTrue(self.scheduler.file_parser('../scheduler/activities.txt')['Time Tracker'] == 15)

class TestSchedulerOverlaps(SchedulerTestCase):
    def test_overlaps_positive(self):
        self.assertTrue(self.scheduler.overlaps(31, 75, [self.schedules_1, self.schedules_2]) == [
            ('Enigma Challenge', 45),
            ('Indiano Drizzle', 45), ('Buggy Driving', 30)])

class TestSchedulerMakeSchedule(SchedulerTestCase):
    def test_make_schedules_findOverlaps(self):

        for minute in range(450):
            event_set = set()
            overlaps = self.scheduler.overlaps(minute, minute, self.schedules)
            overlaps = filter(lambda a: a != ('Lunch Break', 60), overlaps)
            for event in overlaps:
                event_set.add(event)
            self.assertTrue(len(overlaps) == len(event_set))

a=Scheduler()
b=a.scheduler(6,'activities.txt')
a.output(b)

if __name__ == '__main__':
    unittest.main()
