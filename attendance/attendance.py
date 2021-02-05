from enum import Enum
import random, time, pymssql, os
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
        """
        Checkin / Checkout from the back end system using the SIGNIN_ username/password/server/database details in environment
        this executes a spro called spCheckinCheckout with a unique identifier, and then returns a returnValue that matches the values in StatusValues
        """
        username = os.environ['SIGNIN_USERNAME']
        password = os.environ['SIGNIN_PASSWORD']
        server = os.environ['SIGNIN_SERVER']
        database = os.environ['SIGNIN_DATABASE']

        if username is None or password is None or server is None or database is None:
            print("Could not find necessary environment variables for backend connection.")
            return StatusValues.Error

        with pymssql.connect(server=server, user=username, password=password, database=database) as conn:
            with conn.cursor() as cursor:                   
                cursor.callproc('dbo.spCheckinCheckout', (identifier,))
                for row in cursor:
                    return row['returnValue']


class MockAttendance:
    """
    This class performs an emulated version of the Attendance class, for testing the rest of the app
    """

    def __init__(self):
        pass

    def checkin_checkout(self,identifier):
        """
        Returns a random statusvalue, and random name, after 0.5s delay
        """
        time.sleep(0.500)
        return (random.choice([StatusValues.In,StatusValues.Out,StatusValues.Error]),random.choice(["Bob","Joe","Fred","Julie","Suzie"]))

