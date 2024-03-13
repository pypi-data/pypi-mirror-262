import requests

from datetime import datetime
from timetools.timeutil import TimeUtil
from math import radians, sin, cos, sqrt, atan2


class PositionUtil:

    @staticmethod
    def testDependency():
        current = datetime.now()
        return TimeUtil.get_start_of_date(current)

    @staticmethod
    def is_coordinate_in_china(latitude, longitude):
        china_latitude_range = (3.86, 53.55)
        china_longitude_range = (73.66, 135.05)

        if china_latitude_range[0] <= latitude <= china_latitude_range[1] and \
                china_longitude_range[0] <= longitude <= china_longitude_range[1]:
            return True
        else:
            return False
        
    @staticmethod
    def haversine_distance(lat1, lon1, lat2, lon2):
        R = 6371.0
        
        lat1 = radians(lat1)
        lon1 = radians(lon1)
        lat2 = radians(lat2)
        lon2 = radians(lon2)
        
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        
        distance = R * c
        return distance
