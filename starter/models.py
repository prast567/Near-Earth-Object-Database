class NearEarthObject(object):
    """
    Object containing data describing a Near Earth Object and it's orbits.

    # TODO: You may be adding instance methods to NearEarthObject to help you implement search and output data.
    """

    def __init__(self, **kwargs):
        """
        :param kwargs:    dict of attributes about a given Near Earth Object, only a subset of attributes used
        """
        # TODO: What instance variables will be useful for storing on the Near Earth Object?
        self.orbit_info = kwargs
        self.id = kwargs['id']
        self.name = kwargs['name']
        self.diameter_min_km = kwargs['estimated_diameter_min_kilometers']
        self.is_potentially_hazardous_asteroid = kwargs['is_potentially_hazardous_asteroid']
        self.close_approach_date = kwargs['close_approach_date']
        self.miss_distance_kilometers = kwargs['miss_distance_kilometers']

    def update_orbits(self, orbit):
        """
        Adds an orbit path information to a Near Earth Object list of orbits

        :param orbit: OrbitPath
        :return: None
        """

        # TODO: How do we connect orbits back to the Near Earth Object?
        self.orbits = OrbitPath(**self.orbit_info)


class OrbitPath(object):
    """
    Object containing data describing a Near Earth Object orbit.

    # TODO: You may be adding instance methods to OrbitPath to help you implement search and output data.
    """

    def __init__(self, **kwargs):
        """
        :param kwargs:    dict of attributes about a given orbit, only a subset of attributes used
        """
        # TODO: What instance variables will be useful for storing on the Near Earth Object?
        self.orbitpath_data = kwargs
        self.neo_name = kwargs['name']
        self.close_approach_date = kwargs['close_approach_date']
        self.miss_distance_kilometers = kwargs['miss_distance_kilometers']
