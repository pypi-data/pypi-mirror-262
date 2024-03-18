import os
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


# exploratory data analysis class
class Eda:
    """This class contains exploratory data analysis sections. The main purpose of the class is
    to perform one-by-one analysis, bivariate analysis, and plotting operations."""

    # const
    def __init__(self, dataframe=None):

        # dataframe
        self.dataframe = dataframe

        # desktop path
        self.desktop_path = None

        # run the desktop finder
        self.find_system_desktop()

    # methods
    def find_system_desktop(self):
        """This method finds the desktop path of pc"""

        # find the desktop path
        self.desktop_path = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')

        # printing the desktop path
        print("Desktop Path :", self.desktop_path, sep="\t")

    # one by one analysis
    def one_by_one_countplots(self):
        """This method includes countplots"""

        if isinstance(self.dataframe, pd.DataFrame):

            # length of cols
            col_len = len(self.dataframe.columns)

            fig, ax = plt.subplots(col_len, 1)

            # count plots
            for num, col in enumerate(self.dataframe.columns):
                sns.countplot(data=self.dataframe, x=col, ax=ax[num], native_scale=True)

            # arrange and show
            plt.tight_layout()
            plt.show()

            # save on the desktop
            fig.savefig(self.desktop_path+"/one_by_one_countplots.png")
            print("One by One countplots saved on the desktop location")

        else:
            TypeError("Data type must be dataframe")

    # histplot
    def one_by_one_histplot(self):
        """This method includes countplots"""

        if isinstance(self.dataframe, pd.DataFrame):

            # length of cols
            col_len = len(self.dataframe.columns)

            fig, ax = plt.subplots(col_len, 1, figsize=(5, 8))

            # count plots
            for num, col in enumerate(self.dataframe.columns):
                sns.histplot(data=self.dataframe, x=col, ax=ax[num], kde=True)

            # arrange and show
            plt.tight_layout()
            plt.show()

            # save on the desktop
            fig.savefig(self.desktop_path + "/one_by_one_histplot.png")
            print("One by One histplot saved on the desktop location")

        else:
            TypeError("Data type must be dataframe")

    # bivariate analysis
    def bivariate_analysis(self, x: str):
        """This method includes bar plot and reg-plots,
        reg-plots draw on only int or float dtypes so describe columns valid"""
        # control
        if isinstance(self.dataframe, pd.DataFrame):

            # bar plot
            bar = sns.barplot(data=self.dataframe)
            plt.title("bar Plot")

            # show and save
            plt.show()
            bar.figure.savefig(self.desktop_path + "/barplot.png")
            print("Bar plot saved on the desktop location")

            # regression plots

            # x column control
            if x in self.dataframe.describe().columns:

                # reg-plots
                for num, col in enumerate(self.dataframe.describe().columns):

                    # col and x control
                    if col != x:
                        regression_plot = sns.regplot(data=self.dataframe, x=x, y=col)

                        # arrange and show
                        plt.tight_layout()
                        plt.title("Regression plot")
                        plt.show()

                        # save
                        regression_plot.figure.savefig(self.desktop_path+f"/{col}_reg-plot.png")
                        print(f"Regression plot {num} saved on the desktop")

            # x column control 1
            else:
                raise AttributeError("Invalid column name (column dtype must be int or float)")

        # type control else
        else:
            TypeError("Data type must be dataframe")

    # corr analysis
    def corr_analyzer(self):
        """This method analyzes correlation with pandas ,
        only int or float dtype acceptable"""

        # type control
        if isinstance(self.dataframe, pd.DataFrame):

            # corr plot
            corr_plot = sns.heatmap(self.dataframe[self.dataframe.describe().columns].corr(), annot=True)

            # title
            plt.title("Correlation")
            plt.tight_layout()
            plt.show()

            # save
            corr_plot.figure.savefig(self.desktop_path+"/corr_plot.png")
            print("Correlation plot saved on the Desktop")

        # type control else
        else:
            raise TypeError("Data type must be Dataframe")

    # general eda report
    def give_eda_report(self, x: str):
        """This method runs the others"""
        self.one_by_one_countplots()
        self.one_by_one_histplot()
        self.bivariate_analysis(x=x)
        self.corr_analyzer()