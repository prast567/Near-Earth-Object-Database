from collections import namedtuple,defaultdict
from enum import Enum
import re
from exceptions import UnsupportedFeature
from logger import logger
from models import NearEarthObject, OrbitPath


class DateSearch(Enum):
    """
    Enum representing supported date search on Near Earth Objects.
    """
    between = 'between'
    equals = 'equals'

    @staticmethod
    def list():
        """
        :return: list of string representations of DateSearchType enums
        """
        return list(map(lambda output: output.value, DateSearch))


class Query(object):
    """
    Object representing the desired search query operation to build. The Query uses the Selectors
    to structure the query information into a format the NEOSearcher can use for date search.
    """

    Selectors = namedtuple('Selectors', ['date_search', 'number', 'filters', 'return_object', \
                                         'start_date', 'end_date'])
    DateSearch = namedtuple('DateSearch', ['type', 'values'])
    ReturnObjects = {'NEO': NearEarthObject, 'Path': OrbitPath}

    def __init__(self, **kwargs):
        """
        :param kwargs: dict of search query parameters to determine which SearchOperation query to use
        """
        # TODO: What instance variables will be useful for storing on the Query object?
        self.return_object = None
        self.date = None
        self.start_date = None
        self.end_date = None
        self.number = None
        self.filters = None
        if 'return_object' in kwargs.keys():
            self.return_object = kwargs['return_object']
        if 'date' in kwargs.keys():
            self.date = kwargs['date']
        if 'start_date' in kwargs.keys():
            self.start_date = kwargs['start_date']
        if 'end_date' in kwargs.keys():
            self.end_date = kwargs['end_date']
        if 'number' in kwargs.keys():
            self.number = kwargs['number']
        if 'filter' in kwargs.keys():
            self.filters = kwargs['filter']

    def build_query(self):
        """
        Transforms the provided query options, set upon initialization, into a set of Selectors that the NEOSearcher
        can use to perform the appropriate search functionality

        :return: QueryBuild.Selectors namedtuple that translates the dict of query options into a SearchOperation
        """

        # TODO: Translate the query parameters into a QueryBuild.Selectors object
        selector = Query.Selectors(self.date, self.number, self.filters, self.return_object, \
                                   self.start_date, self.end_date)
        return selector


class Filter(object):
    """
    Object representing optional filter options to be used in the date search for Near Earth Objects.
    Each filter is one of Filter.Operators provided with a field to filter on a value.
    """
    Options = {
        # TODO: Create a dict of filter name to the NearEarthObject or OrbitalPath property
        # 'diameter': NearEarthObject.diameter_min_km,
        # 'distance': NearEarthObject.miss_distance_kilometers,
        # 'is_hazardous': NearEarthObject.is_potentially_hazardous_asteroid

    }

    Operators = {
        # TODO: Create a dict of operator symbol to an Operators method, see README Task 3 for hint
    }

    def __init__(self, field, object, operation, value):
        """
        :param field:  str representing field to filter on
        :param field:  str representing object to filter on
        :param operation: str representing filter operation to perform
        :param value: str representing value to filter for
        """
        self.field = field
        self.object = object
        self.operation = operation
        self.value = value

    @staticmethod
    def create_filter_options(filter_options):
        """
        Class function that transforms filter options raw input into filters

        :param input: list in format ["filter_option:operation:value_of_option", ...]
        :return: defaultdict with key of NearEarthObject or OrbitPath and value of empty list or list of Filters
        """

        # TODO: return a defaultdict of filters with key of NearEarthObject or OrbitPath and value of empty list or list of Filters
        filter_dict = defaultdict()
        filter_dict[filter_options[filter_options.pop()]] = filter_options
        return filter_dict

    def apply(self, results):
        """
        Function that applies the filter operation onto a set of results

        :param results: List of Near Earth Object results
        :return: filtered list of Near Earth Object results
        """
        # TODO: Takes a list of NearEarthObjects and applies the value of its filter operation to the results
        neo_container = []

        if self.field.lower() == 'diameter':
            logger.info("Filtering neo based on diameter")
            if self.operation == '>=':
                for item in results:
                    if item.diameter_min_km >= float(self.value):
                        neo_container.append(item)
            elif self.operation == '>':
                for item in results:
                    if item.diameter_min_km > float(self.value):
                        neo_container.append(item)

            elif self.operation == '<=':
                for item in results:
                    if item.diameter_min_km <= float(self.value):
                        neo_container.append(item)
            elif self.operation == '<':
                for item in results:
                    if item.diameter_min_km < float(self.value):
                        neo_container.append(item)
            else:
                for item in results:
                    if item.diameter_min_km == float(self.value):
                        neo_container.append(item)
            logger.info(f"Neo Filtered based on diameter {[item.name for item in neo_container]}")

        elif self.field.lower() == 'distance':
            logger.info("Filtering neo based on distance")
            if self.operation == '>=':
                for item in results:
                    if item.miss_distance_kilometers >= float(self.value):
                        neo_container.append(item)
            elif self.operation == '>':
                for item in results:
                    if item.miss_distance_kilometers > float(self.value):
                        neo_container.append(item)
            elif self.operation == '<=':
                for item in results:
                    if item.miss_distance_kilometers <= float(self.value):
                        neo_container.append(item)
            elif self.operation == '<':
                for item in results:
                    if item.miss_distance_kilometers < float(self.value):
                        neo_container.append(item)
            else:
                for item in results:
                    if item.miss_distance_kilometers == float(self.value):
                        neo_container.append(item)
            logger.info(f"Neo Filtered based on distance {[item.name for item in neo_container]}")

        elif self.field.lower() == 'is_hazardous':
            logger.info("Filtering neo based on is_hazardous")
            if self.value.lower() == 'false':
                for item in results:
                    if item.is_potentially_hazardous_asteroid == False:
                        neo_container.append(item)
            else:
                for item in results:
                    if item.is_potentially_hazardous_asteroid == True:
                        neo_container.append(item)
            logger.info(f"Neo Filtered based on is_hazardous {[item.name for item in neo_container]}")

        return neo_container


class NEOSearcher(object):
    """
    Object with date search functionality on Near Earth Objects exposed by a generic
    search interface get_objects, which, based on the query specifications, determines
    how to perform the search.
    """

    def __init__(self, db):
        """
        :param db: NEODatabase holding the NearEarthObject instances and their OrbitPath instances
        """
        self.db = db
        # TODO: What kind of an instance variable can we use to connect DateSearch to how we do search?
        self.orbit_dict = db.orbit_dict
        self.neo_earth_dict = db.neo_earth_dict

    def get_objects(self, query):
        """
        Generic search interface that, depending on the details in the QueryBuilder (query) calls the
        appropriate instance search function, then applys any filters, with distance as the last filter.

        Once any filters provided are applied, return the number of requested objects in the query.return_object
        specified.

        :param query: Query.Selectors object with query information
        :return: Dataset of NearEarthObjects or OrbitalPaths
        """
        # TODO: This is a generic method that will need to understand, using DateSearch, how to implement search
        # TODO: Write instance methods that get_objects can use to implement the two types of DateSearch your project
        # TODO: needs to support that then your filters can be applied to. Remember to return the number specified in
        # TODO: the Query.Selectors as well as in the return_type from Query.Selectors
        try:
            logger.info("Starting a new search")
            neo_container = []
            if query.date_search!=None:
                logger.info("Filtering neo based on date")
                if query.date_search in self.orbit_dict.keys():
                    neo_container.extend(self.orbit_dict[query.date_search])
                    logger.info(f"Neo filtered based on date are {[item.name for item in neo_container]}")

            elif (query.start_date !=None and query.end_date == None) or \
                (query.start_date == None and query.end_date != None):
                pass
            elif (query.start_date !=None and query.end_date != None):
                logger.info("Filtering neo based on start_date and end date")
                for neo in self.orbit_dict.keys():
                    if neo >= query.start_date and neo<= query.end_date:
                         neo_container.extend(self.orbit_dict[neo])
                logger.info(f"Neo filtered based on date are {[item.name for item in neo_container]}")

            object = neo_container
            if query.filters != None:
                for item in query.filters:
                    filter = re.findall(r'(.*):(.*):(.*)', item)
                    field = filter[0][0]
                    operation = filter[0][1]
                    value = filter[0][2]
                    filter_obj = Filter(field, object, operation, value)
                    object = filter_obj.apply(object)

            final_obj = []

            if query.number == None:
                return object
            else:
                logger.info("Filtering neo based on number")
                if len(object) > query.number:
                    for item in range(query.number):
                        final_obj.append(object[item])
                    logger.info(f"Filtered neo based on number are {[item.name for item in final_obj]}")
                    return final_obj
                logger.info(f"Filtered neo based on number are {[item.name for item in object]}")
                return object
        finally:
            logger.info("Search ended!!!")
