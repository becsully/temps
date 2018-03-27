import csv
import copy
import numpy
import matplotlib.pyplot as plt
import datetime


class TempDict(object):

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
    """An employee who has had at least one temporary contract. Attributes include some anonymized info 
    about the person (ID number, basic demographic info) and a [list? dictionary?] of their contracts. 
    """

    def __init__(self, row): #accepts a row, in dictionary form, from the temps.csv file
        self.idnum = row['ID']
        self.gender = row['Gender']
        self.ethnicity = row['Ethnicity']
        self.contracts = {1: Contract(row)}

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
    """A temporary work contract. Contains start/end dates, department, job title, and pay rate."""

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
    match_bool = False
    contracts = []
    for temp_id in temps:
        temp = temps[temp_id]
        match_bool, matches = temp.has_department(dept_name)
        if match_bool:
            for match in matches:
                contracts.append(match)
    return contracts # returns list of Contract objects


def refine_title(contracts, titles):
    matches = []
    for contract in contracts: 
        if contract.title in titles:
            matches.append(contract)
        else:
            pass
    return matches


def get_x_y(contracts):

    dates_workers_dict = {} #keys are dates, values are int of contracts that match that date

    # populate the dictionary with pairs of dates + how many workers on each date
    for contract in contracts: 
        for date in contract.get_weeks(): 
            if date in dates_workers_dict:
                dates_workers_dict[date] += 1
            else: 
                dates_workers_dict[date] = 1

    # now see if there are any dates with 0 temps
    # find the earliest and latest date in the date dictionary
    temp_earliest = datetime.date.max
    temp_latest = datetime.date.min
    for date in dates_workers_dict: 
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

    for date in date_list: 
        if date in dates_workers_dict:
            pass    
        else:
            dates_workers_dict[date] = 0

    return dates_workers_dict


def position_graph(dw_dicts): #takes list of dicts by position
    print("yay")
 



def simple_graph(dw_dict): #takes a single dict {date: # workers}

    plt.style.use('fivethirtyeight')
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
    temps = TempDict().temps
    matches = get_dept(temps, "All Things Considered")
    matches = refine_title(matches, ["News Assistant", "Production Assistant"])
    simple_graph(get_x_y(matches))


if __name__ == '__main__':
    test()
