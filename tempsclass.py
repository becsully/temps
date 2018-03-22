import datetime
import csv
import copy


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
        self.start_date = row['EffectiveDate'] #string in format MM/DD/YYYY
        self.end_date = row['EndDate'] #string in format MM/DD/YYYY
        self.department = row['Department'] #string
        self.days_worked = int(row['# days']) #int
        self.title = row['JobTtitle'] #string. note the typo in the original CSV
        self.rate = float(row['Rate'].replace("$","").replace(" ","")) #float
        self.employee_id = row['ID']


    def __repr__(self):
        return("Dates: {0.start_date} to {0.end_date} ({0.days_worked} days)\nDepartment: {0.department}\n"
               "Job Title: {0.title}\nPay Rate: ${0.rate}".format(self))

    # function to tabulate workweeks within the contract

""""
def temp_test(temp,args):

    new_temp = copy.deepcopy(temp)

    if args['JobTitle'] is not None: 
        number_deleted = 0
        for i in range(len(temp['Contracts'])): #for item in list
            contract = temp['Contracts'][i]
            if contract['JobTitle'] == args['JobTitle']:
                pass
            else:
                new_temp['Contracts'].pop(i-number_deleted)
                number_deleted += 1
        if new_temp['Contracts'] == []:
            return False, None

    if args['Ethnicity'] and temp['Ethnicity'] not in args['Ethnicity']:
        return False, None

    if args['Gender'] and temp['Gender'] != args['Gender']:
        return False, None

    return True, new_temp


def contract_test(contract,args):
    if contract["JobTitle"] in args["Job Title"]:
        return True
    else: 
        return False


def average_pay(raw_temps,gend=None,ethn=None,jobtitle=None):

    days_total = 0
    weighted_pay_total = 0

    if ethn == "POC":
        ethn = "BLA"

    args = {
        'Ethnicity': ethn,
        'Gender': gend,
        'JobTitle': jobtitle
            }

    temps_to_eval = {}

    for temp in raw_temps: #for key in dictionary
        temp_bool, new_temp = temp_test(raw_temps[temp],args)
        if temp_bool:
            temps_to_eval[temp] = new_temp

    for temp in temps_to_eval:
        for contract in temps_to_eval[temp]["Contracts"]: #for item in list
            weighted_pay_total += float(contract['Rate'])*int(contract['# days'])
            days_total += int(contract['# days'])

    try:
        result = weighted_pay_total/days_total
    except ZeroDivisionError:
        result = "there were no results for this combination!"

    return result


def pay_calc():
    temps = create_dict()

    keep_going = True

    while keep_going:
        print("find average pay based on: ")
        print("1. gender")
        print("2. race/ethnicity")
        print("3. job title")

        gender = None
        ethn = None
        jobtitle = None

        choices = input("type 1, 2, 3, or any combo thereof ->")
        if "1" in choices:
            gender = input("which gender? M or F ->")
        if "2" in choices:
            ethn = input("which race? W(hite), B(lack), A(sian/Middle Eastern), L(atino/a), or POC(all POCs) ->")
        if "3" in choices:
            jobtitle = input("which position? Production Assistant, Producer 1, Reporter US, etc: ->")

        result = average_pay(temps,gender,ethn,jobtitle)

        if isinstance(result, str):
            print(result)
        else: 
            print('${0:.2f}'.format(result))

        kg_input = input("Run another search? Y/N ->")
        if kg_input != 'Y' and kg_input != 'y':
            keep_going = False
"""


def get_dept(temps, dept_name):
    match_bool = False
    contracts = []
    for temp_id in temps:
        temp = temps[temp_id]
        match_bool, matches = temp.has_department(dept_name)
        if match_bool:
            for match in matches:
                print(match)
                contracts.append(match)
    return contracts # returns list of Contract objects


def test():
    temps = TempDict().temps
    matches = get_dept(temps, "All Things Considered")
    print(contract for contract in matches)


if __name__ == '__main__':
    test()
