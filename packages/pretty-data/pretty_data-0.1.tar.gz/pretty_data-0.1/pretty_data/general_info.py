import pandas as pd


# main class
class GeneralInfo:
    """This class contains functions of pandas
    Main purpose of the class is a task for data science preprocessing"""

    # const
    def __init__(self, dataframe=None):
        # variables
        self.dataframe = dataframe

    # head and tail
    def head_and_tail(self):
        """this method shows us to head and tail of dataframe"""

        if isinstance(self.dataframe, pd.DataFrame):
            print("Head:", self.dataframe.head(), sep="\n")
            print("\nTail:", self.dataframe.tail(), sep="\n")
        else:
            raise TypeError("Data must be dataframe")

    # describe, info
    def describe_and_info(self):
        """This method gives information of describe method and info method"""

        if isinstance(self.dataframe, pd.DataFrame):
            print("Describe of the data:\n {}\n".format(self.dataframe.describe()))
            print("İnfo of the Data\n")
            self.dataframe.info()
        else:
            raise TypeError("Data must be dataframe")

    # duplicated data and null data
    def duplicated_and_null(self):
        """This method gives information of duplicated values and null values"""

        if isinstance(self.dataframe, pd.DataFrame):
            print("\nDuplicated data", self.dataframe[self.dataframe.duplicated()], sep="\n")
            print("\nNull values", self.dataframe.isna().sum(), sep="\n")
        else:
            raise TypeError("Data must be dataframe")

    # object datatypes idx-max, idx min, unique values
    def object_processor(self):
        """This method gives information of idxmax and idxmin of object columns and value counts and unique values"""

        if isinstance(self.dataframe, pd.DataFrame):

            # select object dtypes
            columns = self.dataframe.select_dtypes(include=object)

            # print idx max and idx min val
            print("\nİdx Maxes", columns.idxmax(), sep="\n")
            print("\nİdx Mins", columns.idxmin(), sep="\n")

            # print unique values
            for col in columns.columns:

                # eval
                print(f"\nColumn name: {col}\t unique values")
                eval(f"print(self.dataframe.{col}.unique())")

            # print value counts
            print("\nValue Counts", columns.value_counts(), sep="\n")

        else:
            raise TypeError("Data must be dataframe")

    # all functions in one function
    def report_general_info(self):
        """This method runs the others"""

        # run the other functions
        self.head_and_tail()
        print("\n" + "-" * 30 + "\n")
        self.describe_and_info()
        print("\n" + "-" * 30 + "\n")
        self.duplicated_and_null()
        print("\n" + "-" * 30 + "\n")
        self.object_processor()
        print("\n" + "-" * 30 + "\n")
