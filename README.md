Scheduler
========

A pair of python classes for generating a schedule for *n* teams from an activities file.

### Usage


To use the scheduler in another python file, place scheduler.py in an adjacent directory (e.g. `../scheduler/`), it can then be imported and used as follows.

```python
from scheduler import scheduler

s = scheduler.Scheduler()
```

Create a set of schedules by passing a number of teams and the path to an activities text file to the `scheduler` method:

```python
schedule_set = s.scheduler(5,'activities.txt')
```

The `make_schedule` method formats each schedule into a list of event strings whose formatting matches that of the case study.

For convenience, an `output` method is also provided which prints the properly-formatted set of schedules to the console.

```python
s.output(schedule_set)
```

To test the `Scheduler()` class, run the `test-scheduler.py` file.

### Quick Example
The test file, `test-scheduler.py`, will print a set of six schedules to the console - note that the `activities.txt` file must be in the same directory.

```bash
$ python test-scheduler.py
```

### Discussion

The case-study stated that lunch is served at noon, however in the provided example lunch did not occur at noon exactly but rather it was served at or before noon and not thereafter. I decided to make use of this apparent flexibility.

The case-study did not stipulate the number of teams that would be participating. My scheduling function accepts a number of teams as a parameter. 

~~In my testing I found that it was not possible to schedule for more than 13 teams, and scheduling for more than 10 teams sometimes ran into issues in which the script would hang. I'm not sure of the numerical reasons for this - presumably it's because the script attempts to add events randomly and consequently gets into a state in which it cannot proceed without an overlap occurring. I think that this could be overcome by sorting the order in which events are added, possibly in combination with a generator, but I did not have time to pursue this.~~

~~The code will throw an error if the user tries to create schedules for more than nine teams, but this can be deactivated.~~

The script will not schedule an event that overlaps with lunch or the end-of-day presentation, but this comes at a cost of gaps. A potential improvement would be to write a filler function which inserts shorter activities when `11am < schedule running total < 12pm` and `4pm < schedule running total < 5pm`.

## Update 13/12/2019

I found a bug in my code. I have now fixed it by adding a recursive statement. With the activities provided in the case-study it is possible to create a rota for 14 teams or less; the code will throw an error if the user tries to create schedules for more than 14 teams using the provided acitivities.

Because of the random approach that I have taken, when scheduling for 14 teams, the function can make hundreds of attempts before it finds a set of schedules which don't overlap. Hence, I have inserted a catch to prevent the code from reaching python's recursion limit and crashing, although this comes at a cost of occasionally not providing the output sought by the user. Python's recursion limit can be altered - one potential addition to this script would be to offer a mechanism to effect that.
