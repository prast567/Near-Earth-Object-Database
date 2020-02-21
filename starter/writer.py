from enum import Enum
import pathlib
import datetime
import time

class OutputFormat(Enum):
    """
    Enum representing supported output formatting options for search results.
    """
    display = 'display'
    csv_file = 'csv_file'

    @staticmethod
    def list():
        """
        :return: list of string representations of OutputFormat enums
        """
        return list(map(lambda output: output.value, OutputFormat))


class NEOWriter(object):
    """
    Python object use to write the results from supported output formatting options.
    """

    def __init__(self):
        # TODO: How can we use the OutputFormat in the NEOWriter?
        self.options = OutputFormat.list()

    def write(self, format, data, **kwargs):
        """
        Generic write interface that, depending on the OutputFormat selected calls the
        appropriate instance write function

        :param format: str representing the OutputFormat
        :param data: collection of NearEarthObject or OrbitPath results
        :param kwargs: Additional attributes used for formatting output e.g. filename
        :return: bool representing if write successful or not
        """
        # TODO: Using the OutputFormat, how can we organize our 'write' logic for output to stdout vs to csvfile
        # TODO: into instance methods for NEOWriter? Write instance methods that write() can call to do the necessary
        # TODO: output format.
        try:
            header = "id name orbit_date miss_distance_kilometers"
            if format == self.options[0]:
                if len(data)!=0:
                    print(header)
                    for item in data:
                        print(item.id , ' ' , item.name , ' ', item.close_approach_date , ' ' , item.miss_distance_kilometers)
                else:print('No search result found')

            if format == self.options[1]:
                testruntimestamp = time.time()
                strtestruntimestamp = str(datetime.datetime.fromtimestamp(testruntimestamp))[:-3].replace('-','_').replace(
                    ' ', '_').replace(':', '_').replace('.', '_')  # creating timestamp
                path = pathlib.Path(__file__).parent
                output_csv_file = f'{path}/data/output_csv_file_{strtestruntimestamp}.csv'

                with open(output_csv_file, 'a') as csvfile:
                    # creating a csv writer object
                    csvfile.write(header+'\n')
                    for item in data:
                        a= str(item.id)+ ' '+ str(item.name)+ ' '+ str(item.close_approach_date)+ ' '+ str(item.miss_distance_kilometers)
                        csvfile.write(a)
                        csvfile.write('\n')
            return 1

        except:
            return 0