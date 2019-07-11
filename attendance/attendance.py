from enum import Enum
import random, time
## used to check in or check out a user

class StatusValues(Enum):
    In=0
    Out=1
    Error=2

class Attendance:
    """
    The attendance class performs checkin/checkout of users of a worplace/event/etc
    """

    def __init__(self):
        pass
    
    def checkin_checkout(self,identifier):
        pass


class MockAttendance:
    """
    This class performs an emulated version of the Attendance class, for testing the rest of the app
    """

    def __init__(self):
        pass

    def checkin_checkout(self,identifier):
        time.sleep(0.500)
        return random.choice([StatusValues.In,StatusValues.Out,StatusValues.Error])

