import pandas as pd


# class for manipulating operations
class Manipulator:
    """This class contains operations of the manipulations"""
    def __init__(self, dataframe=None):

        self.dataframe = dataframe

    # basic regex manipulation
    def select_w_regex(self, only_numbers=True, only_strings=False, specific=False,
                       s_parameter=None, value=None) -> pd.DataFrame:
        """This method selects only string or numbers
        if u want to select specific, set specific parameter True to implement the specific regex
        s_parameter must be regex string and value will be replaced with regex"""

        # control
        if isinstance(self.dataframe, pd.DataFrame):

            # control system
            if specific is False:

                if only_numbers is True and only_strings is False:
                    return self.dataframe.replace("[a-zA-Z]", "", regex=True)
                elif only_numbers is False and only_strings is True:
                    return self.dataframe.replace("[^a-zA-Z]", "", regex=True)
                else:
                    raise AttributeError("Only numbers and only strings parameters can't be the same")

            else:
                return self.dataframe.replace(s_parameter, value, regex=True)

        else:
            raise TypeError("Data type must be dataframe")

    # date time parser
    def datetime_parser(self, column_name: str, as_index: bool, parse_and_sep: bool) -> pd.DataFrame:
        """This method parses datetime and gives options to manipulate
        ex set as index and parse and separate the columns"""

        # control
        if isinstance(self.dataframe, pd.DataFrame):

            # parse dates
            parsed_data_frame = pd.to_datetime(self.dataframe[column_name])

            # assign the same column
            self.dataframe[column_name] = parsed_data_frame

            indexes = pd.DatetimeIndex(self.dataframe[column_name])
            # control 2
            if as_index is True:

                if parse_and_sep is True:
                    self.dataframe["year"] = indexes.year
                    self.dataframe["month"] = indexes.month
                    self.dataframe["day"] = indexes.day

                    # returning parsed
                    return self.dataframe.set_index(column_name)

                # returning set index
                return self.dataframe.set_index(column_name)

            # returning only dates parsed and assign the same col
            return self.dataframe

        else:
            raise TypeError("Data type must be dataframe")

    # searching values
    def search_string(self, column_name: str, keywords: list, method=0):
        """This method search the strings on given column name by str. contains method
        Keywords must be list type."""

        # control
        if isinstance(self.dataframe, pd.DataFrame):

            # column name existence and dtype
            if column_name in self.dataframe.columns and self.dataframe[column_name].dtype == object:

                # method control
                if method == 0:
                    "contains method"
                    return self.dataframe[self.dataframe[column_name].str.contains('|'.join(keywords))]

                else:
                    raise AttributeError("Invalid Method")

            # column existence else
            else:
                raise AttributeError("Invalid column Name or column dtype")

        # type equivalent else
        else:
            raise TypeError("Data type must be dataframe")
