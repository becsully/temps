import datetime
import csv
import copy


def create_dict():
    temp_dict = {}
    with open('temps.csv') as tempfile:
        reader = csv.DictReader(tempfile)
        for row in reader:
            idnum = row['ID']
            if idnum in temp_dict:
                new_contract = {
                    'EffectiveDate': row['EffectiveDate'], 
                    'EndDate': row['EndDate'], 
                    '# days': row['# days'],
                    'Department': row['Department'],
                    'JobTitle': row['JobTtitle'], #note the type in the original CSV
                    'Rate': row['Rate']
                        }
                temp_dict[idnum]['Contracts'].append(new_contract)
            else: 
                temp_dict[idnum] = {
                    'Gender': row['Gender'],
                    'Ethnicity': row['Ethnicity'],
                    'Contracts': [{
                        'EffectiveDate': row['EffectiveDate'], 
                        'EndDate': row['EndDate'], 
                        '# days': row['# days'],
                        'Department': row['Department'],
                        'JobTitle': row['JobTtitle'], #note the type in the original CSV
                        'Rate': row['Rate']
                            }]
                        }
    return temp_dict



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


def test():
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


if __name__ == '__main__':
    test()
