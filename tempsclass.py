import csv
import copy
import numpy
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
import datetime
from pprint import pprint


class TempDict(object):
    # a class to help easily make/manage the giant list of employees and their temp contracts. 
    def __init__(self):
        self.temps = {}
        with open('temps.csv') as tempfile:
            reader = csv.DictReader(tempfile)
            for row in reader:        
                idnum = row['ID']
                if idnum in self.temps: 
                    self.temps[idnum].add_contract(row)
                else:
                    self.temps[idnum] = Employee(row)

    def print_all(self):
        for temp in self.temps:
            self.temps[temp].print_all()
            print("")


class Employee(object):
    # An employee who has had at least one temporary contract. Attributes include some anonymized info 
    # about the person (ID number, basic demographic info) and a dictionary {int: Contract} of their contracts. 

    def __init__(self, row): #accepts a row, in dictionary form, from the temps.csv file
        self.idnum = row['ID']
        self.gender = row['Gender']
        self.ethnicity = row['Ethnicity']
        self.contracts = {0: Contract(row)}

    def add_contract(self, row):
        numlist = []
        for contract in self.contracts:
            numlist.append(contract)
        i = max(numlist) + 1
        self.contracts[i] = Contract(row)

    def __repr__(self):
        return("Employee #{0.idnum} ({0.gender},{0.ethnicity})".format(self))

    def print_all(self):
        print(self)
        for contract in self.contracts:
            print(f"{contract}."),
            print(self.contracts[contract])

    def has_department(self, dept_name):
        match_bool = False
        matches = []
        for contract in self.contracts:
            if self.contracts[contract].department == dept_name:
                match_bool = True
                matches.append(self.contracts[contract])
            else:
                pass
        return match_bool, matches


class Contract(object):
    # A temporary work contract. Contains start/end dates, department, job title, and pay rate.

    def __init__(self, row):
        self.start_date = datetime.datetime.strptime(row['EffectiveDate'], "%m/%d/%Y").date()
        self.start_date_str = row['EffectiveDate']
        self.end_date = datetime.datetime.strptime(row['EndDate'], "%m/%d/%Y").date()
        self.end_date_str = row['EndDate']
        self.department = row['Department'] #string
        self.days_worked = int(row['# days']) #int
        self.title = row['JobTtitle'] #string. note the typo in the original CSV
        self.rate = float(row['Rate'].replace("$","").replace(" ","")) #float
        self.employee_id = row['ID']

    def __repr__(self):
        return("Dates: {0.start_date_str} to {0.end_date_str} ({0.days_worked} days)\n"
               "Department: {0.department}\nJob Title: {0.title}\nPay Rate: ${0.rate}".format(self))

    def get_weeks(self): 
        days = []
        if self.days_worked >= 4:
            for x in range(self.days_worked - 1):
                date = self.start_date + datetime.timedelta(days=x)
                if date.weekday() == 3: #if the day is a thursday
                    days.append(date)
                else:
                    pass
        return days


def get_dept(temps, dept_name):
    # takes Temps.temps, a dictionary of {ID number: Employee object}
    match_bool = False
    contracts = []
    for temp_id in temps:
        temp = temps[temp_id]
        match_bool, matches = temp.has_department(dept_name)
        if match_bool:
            for match in matches:
                contracts.append(match)
    return contracts # returns list of Contract objects


def refine_title(contracts, titles): #list of Contracts, list of titles by string
    matches = []
    for contract in contracts: 
        if contract.title in titles:
            matches.append(contract)
        else:
            pass
    return matches


def make_dw_dict(contracts): #takes list of Contract objects and creates dictionary of dates: # workers
    dw_dict = {} #keys are dates, values are int# of workers whose contracts that match that date

    # populate the dictionary with pairs of dates + how many workers on each date
    for contract in contracts: 
        for date in contract.get_weeks(): 
            if date in dw_dict:
                dw_dict[date] += 1
            else: 
                dw_dict[date] = 1

    if bool(dw_dict) is False:
        return None
    else:
        return dw_dict


def earliest_latest(dw_dicts): #takes a dict {position: date-worker dict}
    # find the earliest and latest date in the date dictionaries
    temp_earliest = datetime.date.max
    temp_latest = datetime.date.min

    for d in dw_dicts:
        position = dw_dicts[d]
        for date in position: 
            if date < temp_earliest:
                temp_earliest = date
            elif date > temp_latest:
                temp_latest = date
            else:
                pass

    date_list = []
    while temp_earliest <= temp_latest:
        date_list.append(temp_earliest)
        temp_earliest = temp_earliest + datetime.timedelta(days=7)

    return date_list


def remove_empty(temp_dw_dicts): # takes a dict of {position: date-worker dict}
    #dump dicts with no results
    dw_dicts = {}
    for position in temp_dw_dicts:
        if bool(temp_dw_dicts[position]): #checks to see if the dictionaries have content
            dw_dicts[position] = temp_dw_dicts[position]
        else: #if they're empty, they get dumped
            pass
    return dw_dicts


def fill_zeros(dw_dicts): # takes a dict of {position: date-worker dict}
    # add date: 0 to all dates with 0 temps
    date_list = earliest_latest(dw_dicts)
    for position in dw_dicts:
        p = dw_dicts[position]
        for date in date_list: 
            if date in p:
                pass    
            else:
                p[date] = 0
    return dw_dicts


def position_graph(dept_name, dw_dicts): # takes a dict of {position: date-worker dict}
    #makes a nice looking graph of all temps in a dept over a period of time. 
    colors = {
        'News Assistant': '#1B5A7A',
        'Production Assistant': '#1AA59A',
        'Assistant Producer': '#A6ED8E',
        'Associate Producer': '#F3FFB9',
        'Assoc Producer/Director': '#F3FFB9',
        'Editor I': '#57385C',
        'Editor II': '#A75265',
        'Editor III': '#F08E6B',
        'Senior Editor': '#FFFA9D',
        'Reporter US': '#C9D6DF',
        'Reporter': '#C9D6DF',
        'Librarian 1': '#36506C',
        'Librarian 2': '#A5DEF1',
        }

    ax = plt.subplot(111)
    ax.axvline(datetime.date(2017,3,1), linewidth=0.5, color='lightgrey', zorder=0) # vertical lines
    ax.axvline(datetime.date(2018,3,1), linewidth=0.5, color='lightgrey', zorder=0) # vertical lines

    dw_dicts = remove_empty(dw_dicts)
    dw_dicts = fill_zeros(dw_dicts)

    running_total = {} # a shadow dw_dict with a running total of workers added so far
    for date in dw_dicts[(list(dw_dicts)[0])]: # just a way of picking a single entry in the dict
        running_total[date] = 0

    i = 0
    for d in dw_dicts:
        position = dw_dicts[d]
        p = plt.bar([date for date in position], [position[date] for date in position], 
                    width=5, zorder=1, bottom=[running_total[date] for date in position], 
                    color=colors[d], label=d)
        i+=1
        for date in position:
            running_total[date] += position[date]

    ax.xaxis_date()
    date_format = mdates.DateFormatter("%b '%y")
    ax.xaxis.set_major_formatter(date_format)
    ax.set_axisbelow(False)
    loc = mticker.MultipleLocator(1)
    ax.yaxis.set_major_locator(loc)
    ax.yaxis.grid(color='white', linewidth=3, zorder=2)
    ax.xaxis.grid(False)
    ax.set_facecolor('white')
    plt.title(dept_name)
    plt.legend(loc='best').draggable()
    plt.show()


def simple_graph(dw_dict): #takes a single dict {date: # workers}
    ax = plt.subplot(111)
    ax.axvline(datetime.date(2017,3,1), linewidth=0.5, color='lightgrey', zorder=0) # vertical lines
    ax.axvline(datetime.date(2018,3,1), linewidth=0.5, color='lightgrey', zorder=0) # vertical lines
    ax.bar([key for key in dw_dict], [dw_dict[key] for key in dw_dict], width=5, zorder=1)
    ax.xaxis_date()
    ax.set_axisbelow(False)
    ax.yaxis.grid(color='white', linewidth=3, zorder=2)
    ax.xaxis.grid(False)
    ax.set_facecolor('white')
    plt.show()


def test():
    editors = ['Editor I', 'Editor II', 'Editor III', 'Senior Editor']
    producers = ['News Assistant', 'Production Assistant', 'Assistant Producer', 'Associate Producer']
    library = ['Librarian 1', 'Librarian 2']
    desk = ['Reporter US', 'Editor I', 'Editor II', 'Editor III', 'Senior Editor']
    all_news = ['News Assistant', 'Production Assistant', 'Assistant Producer', 'Associate Producer',
                'Reporter US', 'Reporter', 'Editor I', 'Editor II', 'Editor III', 'Senior Editor']
    
    #change these for graphs
    dept_name = 'Morning Edition'
    titles = editors

    temps = TempDict().temps
    matches = get_dept(temps, dept_name)
    t_matches = {}
    for t in titles:
        t_matches[t] = make_dw_dict(refine_title(matches, t))
    position_graph(dept_name, t_matches)


if __name__ == '__main__':
    test()
