import cmd
import pickle
import re
import doctest
import matplotlib.pyplot as plt
import numpy as np
import os


class MyFileExistsError(Exception):
    def __init__(self):
        Exception.__init__(self, "file alreadys exists, try again with a \
        different name or location")


class Model():
    id_list = list()
    gender_list = list()
    age_list = list()
    sales_list = list()
    bmi_list = list()
    income_list = list()

    def get_data():
        """
        Check correct data has entered list at correct index.
        loadData_Bad.txt scenario.

        >>> Model.id_list[3] is None
        True

        >>> Model.gender_list[3]
        'F'
        """
        filename = input("Enter the destination/filename. \
        Eg: D:/data/load_data.txt")
        try:
            with open(filename, 'r') as f:
                for line in f:
                    raw_line_data = line
                    i = 0
                    for element in raw_line_data.split():
                        if i == 0:
                            v = Validate_ID()
                            v.check_if_valid(element)
                        elif i == 1:
                            v = Validate_Gender()
                            v.check_if_valid(element)
                        elif i == 2:
                            v = Validate_Age()
                            v.check_if_valid(element)
                        elif i == 3:
                            v = Validate_Sales()
                            v.check_if_valid(element)
                        elif i == 4:
                            v = Validate_BMI()
                            v.check_if_valid(element)
                        elif i == 5:
                            v = Validate_Income()
                            v.check_if_valid(element)
                        else:
                            print("error in get_data() raw_line_data")
                        i += 1

        except IOError:
            print("IO error, not reading file. Try entering filename again")


class Validate(object):
    def check_if_valid(self, element):
        match_param = self.get_match_param()
        match = self.run_match(match_param, element)
        self.add_result(match)

    def get_match_param(self):
        raise NotImplementedError

    def run_match(self, match_param, element):
        if re.match(match_param, element):
            return element

    def add_result(self, match):
        raise NotImplementedError


class Validate_ID(Validate):
    def get_match_param(self):
        return '[A-Z][0-9]{3}'

    def add_result(self, match):
        Model.id_list.append(match)


class Validate_Gender(Validate):
    def get_match_param(self):
        return '(M|F)'

    def add_result(self, match):
        Model.gender_list.append(match)


class Validate_Age(Validate):
    def get_match_param(self):
        return '[0-9]{2}'

    def add_result(self, match):
        Model.age_list.append(match)


class Validate_Sales(Validate):
    def get_match_param(self):
        return '[0-9]{3}'

    def add_result(self, match):
        Model.sales_list.append(match)


class Validate_BMI(Validate):
    def get_match_param(self):
        return '(Normal|Overweight|Obesity|Underweight)'

    def add_result(self, match):
        Model.bmi_list.append(match)


class Validate_Income(Validate):
    def get_match_param(self):
        return '[0-9]{2,3}'

    def add_result(self, match):
        Model.income_list.append(match)


class View():
    pass

    """ def scatter_plot(x, xName, y, yName):

        arrayX = np.array(x)
        arrayY = np.array(y)

        plt.bar(x, y)

        plt.xlabel('x')
        plt.ylabel('y')
        plt.title('Interesting graph\nCheck it out')
        plt.legend()
        plt.show()"""

    def pie_chart_gender():
        m_count = 0
        f_count = 0
        all_valid_count = 0
        for element in Model.gender_list:
            if element == 'F':
                f_count += 1
                all_valid_count += 1
            elif element == 'M':
                m_count += 1
                all_valid_count += 1
        try:
            m_percentage = m_count / all_valid_count * 100
        except ZeroDivisionError:
            m_percentage = 0
        try:
            f_percentage = f_count / all_valid_count * 100
        except ZeroDivisionError:
            f_percentage = 0

        labels = 'Female', 'Male'
        sizes = f_percentage, m_percentage
        colors = 'pink', 'blue'

        plt.title('Employee Gender Percentages')
        plt.pie(sizes, labels=labels, colors=colors,
                autopct='%1.1f%%', shadow=True, startangle=90)
        plt.axis('equal')
        plt.show()

    def pie_chart_bmi():
        obesity_count = 0
        overweight_count = 0
        normal_count = 0
        underweight_count = 0
        all_valid_count = 0

        for element in Model.bmi_list:
            if element == 'Obesity':
                print('ob')
                obesity_count += 1
                all_valid_count += 1
            elif element == 'Overweight':
                print('ov')
                overweight_count += 1
                all_valid_count += 1
            elif element == 'Normal':
                print('norm')
                normal_count += 1
                all_valid_count += 1
            elif element == 'Underweight':
                print('und')
                underweight_count += 1
                all_valid_count += 1

        try:
            ob_percent = obesity_count / all_valid_count * 100
            print('obese ' + str(ob_percent))
        except ZeroDivisionError:
            ob_percent = 0
        try:
            ov_percent = overweight_count / all_valid_count * 100
            print('over ' + str(ov_percent))
        except ZeroDivisionError:
            ov_percent = 0
        try:
            norm_percent = normal_count / all_valid_count * 100
            print('norm ' + str(norm_percent))
        except ZeroDivisionError:
            norm_percent = 0
        try:
            und_percent = underweight_count / all_valid_count * 100
            print("und " + str(und_percent) + ' ' + str(underweight_count))
        except ZeroDivisionError:
            und_percent = 0

        print(all_valid_count)
        labels = 'Obesity', 'Overweight', 'Normal', 'Underweight'
        sizes = ob_percent, ov_percent, norm_percent, und_percent
        colors = 'red', 'orange', 'green', 'orange'

        plt.title("Percentage of Employees in Each BMI Category")
        plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
                shadow=True, startangle=90)
        plt.axis('equal')
        plt.show()


class Controller(cmd.Cmd):

    def do_load_file(self, args):
        """
        :method: load_file or lf
        :description: Gets employee data from a text file. This method will
        prompt the user to enter the location/text file name. Text file must
        contain lines of data (id gender age sales bmi income)like this - A111
        F 32 300 Normal 500 - with each employee on a new line. Any invalid
        data will be inputted as 0 or None. Once this is run the data will be
        loaded and ready to analyse or save in pickle.
        :param: self, args
        :return: Data into correct format to be saved or analysed in the app.
        """
        Model.get_data()

    def do_save_data(self, args):
        """
        :method: save_data
        :description: Saves data as a serialised file to access later.
        :param: self, args
        :return: Data saved in a serialised file
        """
        Model.serialise_data()

    def do_load_saved_file(self, args):
        """
        :method: load_saved_file
        :description: If data has been saved previously it can be reloaded.
        This is not for text files, but for serialised data.
        :param: self
        :return: Data reloaded from a previously saved file.
        """
        Model.load_serialised_data()

    def do_display_gender_data(self, args):
        """
        :method: display_gender_data or dg
        :description: If data has been loaded into the app it will show a pie
        chart of the percentage of Male and Female employees. If data has not
        already been loaded the user will be prompted to enter the
        location/filename of data to be loaded.
        :param: self
        :return: A pie chart of genders of employees
        """

        if not Model.gender_list:
            print("No data loaded, please enter data location")
            Model.get_data()
            if Model.gender_list:
                View.pie_chart_gender()
        else:
            View.pie_chart_gender()

    def do_display_bmi_data(self, args):
        """
        :method: display_bmi_data or db
        :description: If data has been loaded into the app it will show a pie
        chart of the percentage of Obese, Overweight, Normal and Underweight
        employees. If data has notalready been loaded the user will be
        prompted to enter the location/filename of data to be loaded.
        :param: self
        :return: A pie chart of bmi categories of employees.
        """
        if not Model.bmi_list:
            print("No data loaded, please enter data location")
            Model.get_data()
            if Model.bmi_list:
                View.pie_chart_bmi()
        else:
            View.pie_chart_bmi()

    def do_quit(self, args):
        """
        :method: quit or q
        :description: Quit the application. Will prompt the user as to
        whether the user would like to save the data serialised.
        :param: self
        :return: Will exit the app.
        """

        print('Quitting...')
        raise SystemExit

    do_q = do_quit
    do_db = do_display_bmi_data
    do_dg = do_display_gender_data
    do_lf = do_load_file


def main():
    pass

if __name__ == '__main__':
    main()

controller = Controller()
controller.prompt = ':) '
controller.cmdloop('Starting prompt...')
