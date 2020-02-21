import pandas as pd
from models import OrbitPath, NearEarthObject


class NEODatabase(object):
    """
    Object to hold Near Earth Objects and their orbits.

    To support optimized date searching, a dict mapping of all orbit date paths to the Near Earth Objects
    recorded on a given day is maintained. Additionally, all unique instances of a Near Earth Object
    are contained in a dict mapping the Near Earth Object name to the NearEarthObject instance.
    """

    def __init__(self, filename):
        """
        :param filename: str representing the pathway of the filename containing the Near Earth Object data
        """
        # TODO: What data structures will be needed to store the NearEarthObjects and OrbitPaths?
        # TODO: Add relevant instance variables for this.
        self.filename = filename
        self.orbit_dict = {}
        self.neo_earth_dict = {}

    def load_data(self, filename=None):
        """
        Loads data from a .csv file, instantiating Near Earth Objects and their OrbitPaths by:
           - Storing a dict of orbit date to list of NearEarthObject instances
           - Storing a dict of the Near Earth Object name to the single instance of NearEarthObject

        :param filename:
        :return:
        """

        if not (filename or self.filename):
            raise Exception('Cannot load data, no filename provided')

        filename = filename or self.filename

        # TODO: Load data from csv file.
        # TODO: Where will the data be stored?
        neo_df = pd.read_csv(filename)
        temp_dict = {}
        orbit = []
        for ind in neo_df.index:
            for column in neo_df.columns:
                temp_dict[column] = neo_df[column][ind]
            try:

                near_earth_object = NearEarthObject(**temp_dict)
                near_earth_object.update_orbits(orbit)
            except Exception as e:
                print(e)
            orbit_path = OrbitPath(**temp_dict)

            temp_dict.clear()

            if neo_df['close_approach_date'][ind] in self.orbit_dict.keys():
                self.orbit_dict[neo_df['close_approach_date'][ind]].append(near_earth_object)

            else:
                self.orbit_dict[neo_df['close_approach_date'][ind]] = []
                self.orbit_dict[neo_df['close_approach_date'][ind]].append(near_earth_object)

            if neo_df['name'][ind] not in self.orbit_dict.keys():
                self.neo_earth_dict[neo_df['name'][ind]] = orbit_path
