# Elisha Hu Zi Qian
# TP065197

import os

# function to return menu list 
def getMenu(type):
    menu = []
    match type:
        case 'main':
            menu = [
                'Select an option from below: ',
                '\t1. Show inventory, supplier, or hospital details',
                '\t2. Update item supplies',
                '\t3. Update miscellaneous details',
                '\t4. Search distribution details',
                '\t5. Exit program\n'
            ]
        case 'details':
            menu = [
                'Select an option from below: ',
                '\t1. Inventory',
                '\t2. Suppliers',
                '\t3. Hospitals',
                '\t4. Sorted Inventory',
                '\t5. Stocks < 25\n'
            ]
        case 'misc':
            menu = [
                'Select an option from below: ',
                '\t1. Suppliers',
                '\t2. Hospitals\n'
            ]
        case 'misc2':
            menu = [
                'Enter new name: ',
                'Enter code: '
            ]
        case 'item':
            menu = [
                'Enter item code: ',
                'Enter type of change (+ for receiving, - for distributing): ',
                'Enter the amount: ',
                'Enter the hospital code (leave blank if receiving): '
            ]
        case 'search':
            menu = [
                'Enter item code: '
            ]
    
    return menu

# create file if file doesnt exist, then return true to indicate initial file creation
# if file exists, return file as r+, then return false to indicate file exists
def setupFile(path):
    file = ''
    first = True
    try:
        # exclusive creation, will throw exception if file already exists
        file = open(path, 'x')
    except:
        # read and write if file already exists
        file = open(path, 'r+')
        first = False
        
    return file, first

# clear screen
def clear():
    # ansi escape code https://en.wikipedia.org/wiki/ANSI_escape_code
    print('\033[H\033[2J', end='')

# prompts user to enter hospital details on initial file creation then returns file
# otherwise just returns file
def createHospitals():
    hosps, first = setupFile('./data/hospitals.txt')

    if first:
        hospitals = [
            'Hospital Name\tHospital Code\n'
        ]
        clear()
        hospTypes = hospitals[0].strip().split('\t')
        while True:
            hospital = ''
            for type in hospTypes:
                data = input(f'Enter the {type.lower()}: ')
                # ensure proper formatting in txt file and in cmd
                match hospTypes.index(type):
                    case 0:
                        hospital += f'{data.title()}\t'
                    case 1:
                        hospital += f'\t{data.upper()}\n'
            hospitals.append(hospital)

            con = input('Press <enter> to continue or type \'x\' to stop entering hospital details: ')
            if con.lower() == 'x':
                break

        hosps.writelines(hospitals)
        hosps.close()
        clear()
        hosps, first = setupFile('./data/hospitals.txt')

    return hosps

# prompts user to enter supplier details on initial file creation then returns file
# otherwise just returns file
def createSuppliers():
    sups, first = setupFile('./data/suppliers.txt')

    if first:
        suppliers = [
            'Supplier Name\tSupplier Code\n'
        ]
        clear()
        supTypes = suppliers[0].strip().split('\t')
        while True:
            supplier = ''
            for type in supTypes:
                data = input(f'Enter the {type.lower()}: ')
                # ensure proper formatting in txt file and in cmd
                match supTypes.index(type):
                    case 0:
                        supplier += f'{data.title()}\t'
                    case 1:
                        supplier += f'\t{data.upper()}\n'
            suppliers.append(supplier)

            con = input('Press <enter> to continue or type \'x\' to stop entering supplier details: ')
            if con.lower() == 'x':
                break

        sups.writelines(suppliers)
        sups.close()
        sups, first = setupFile('./data/suppliers.txt')

    return sups

# prompts user to enter item details on initial file creation then returns file
# otherwise just returns file
def createPPE():
    if not os.path.exists('data'):
        os.makedirs('data')
        
    ppe, first = setupFile('./data/ppe.txt')

    if first:
        items = [
            'Item Code\tItem Name\tStock\tSupplier\n'
        ]
        clear()
        print('Initial setup is starting. Please enter the relevant details.\n')
        itemTypes = items[0].strip().split('\t')
        while True:
            item = ''
            for type in itemTypes:
                data = input(f'Enter the {type.lower()}: ')
                # ensure proper formatting in txt file and in cmd
                match itemTypes.index(type):
                    case 0:
                        item += f'{data.upper()}\t\t'
                    case 1:
                        # 4 space = 1 tab, make everything uniform
                        if len(data) == 4:
                            item += f'{data.title()}    \t'
                        elif len(data) == 6:
                            item += f'{data.title()}  \t'
                        else:
                            item += f'{data.title()}\t'
                    case 2:
                        item += f'{data}\t'
                    case 3:
                        item += f'{data.upper()}\n'
            items.append(item)

            con = input('Press <enter> to continue or type \'x\' to stop entering item details: ')
            if con.lower() == 'x':
                break

        ppe.writelines(items)
        ppe.close()
        ppe, first = setupFile('./data/ppe.txt')

    return ppe

# creates distribution file then returns file 
# if initial file creation, write the categories to the file
def createDis():
    dis, first = setupFile('./data/distribution.txt')

    if first:
        types = 'Item Code\tType\tAmount\tHospital Code\n'
        dis.write(types)
        dis.close()
        dis, first = setupFile('./data/distribution.txt')

    return dis

# print menu, get inputs, then return inputs as a list
def getInputs(menu):
    inputs = []
    for line in menu:
        inputs.append(input(line).strip())

    return inputs

# ask if user wants to retry, then return true if yes, otherwise return false
def retry(txt):
    retry = input(txt)
    if retry.strip().lower() == 'yes':
        return True
    return False

# read file then return a 2d list
# the 2d list is a list containing the rows in the files as lists with the columns as the elements
def readFile(file):
    file.seek(0)
    linesList = []

    for line in file:
        entry = line.strip().split('\t')
        # filter entry's elements that are not equal to '' then add everything in a list if entry contains '', otherwise dont change
        entry = list(filter(('').__ne__, entry)) if '' in entry else entry
        linesList.append(entry)
    
    return linesList

# replace lines that contain old data with new data, but only the first one
# after all lines are done, rewrite file with new lines
def updateFile(file, id, old, new):
    file.seek(0)
    newLines = ''
    for line in file:
        # replace first old data in line with new if id is in line, otherwise dont change
        newLine = line.replace(old, new, 1) if id.lower() in line.lower() else line
        newLines += newLine
    file.close()

    # open file in w+ to update file
    file = open(file.name, 'w+')
    file.write(newLines)

    return file

# update supplier and hospital details
def updateMisc(file):
    menu = getMenu('misc2')
    items = readFile(file)
    while True:
        clear()
        file.seek(0)
        print(file.read())
        inputs = getInputs(menu)
        # get list of elements in items that contain inputs[1].upper()
        item = [i for i in items if inputs[1].upper() in i]

        if item:
            item = item[0]
        else:
            re = retry('Invalid code. Returning to main menu. Type "yes" if you want to re-enter: ')
            if re:
                continue
            else:
                break
        
        file = updateFile(file, inputs[1], item[0], inputs[0].title())
        print(file.read())
        print('Details have been updated.\n')
        break

# log inventory change details (receive and distribute)
# item code; receive or distribute with + or -; amount; hospital id if any, N/A is none
def saveLog(id, op, amount, hid):
    dis = createDis()
    dis.close()
    dis = open(dis.name, 'a+')
    hid = 'N/A' if not hid else hid.upper()
    dis.write(f'{id.upper()}\t\t{op}\t{amount}\t\t{hid}\n')
    dis.close()

# asks the user which item is updating, which type of change, the amount, and which hospital if any
# then calls the other functions to update the file and log the change 
def updateItem(ppe):
    operators = ['+', '-']
    menu = getMenu('item')
    items = readFile(ppe)
    while True:
        clear()
        ppe.seek(0)
        print(ppe.read())

        # get list of elements in items where i[2] is '0'
        zero = [i for i in items if i[2] == '0']
        if zero:
            for item in zero:
                print(f'{item[1].strip()} ({item[0]}) is out of stock.')
            print()

        inputs = getInputs(menu)

        try:
            inputs[2] = int(inputs[2])
        except:
            re = retry('Invalid input. Returning to main menu. Type "yes" if you want to re-enter: ')
            if re:
                continue
            else:
                break

        if inputs[1] not in operators or inputs[2] < 0:
            re = retry('Invalid input. Returning to main menu. Type "yes" if you want to re-enter: ')
            if re:
                continue
            else:
                break
        
        # get list of elements in items that contain inputs[0].upper()
        item = [i for i in items if inputs[0].upper() in i]
        if item:
            item = item[0]
        else:
            re = retry('Invalid item code. Returning to main menu. Type "yes" if you want to re-enter: ')
            if re:
                continue
            else:
                break

        amount = int(item[2])
        # calculate the amount of items after receiving or distributing items
        newAmount = eval(f'{amount} {inputs[1]} {inputs[2]}')
        if newAmount < 0:
            re = retry('Not enough stock. Returning to main menu. Type "yes" if you want to re-enter: ')
            if re:
                continue
            else:
                break

        ppe = updateFile(ppe, inputs[0], str(amount), str(newAmount))
        saveLog(inputs[0], inputs[1], inputs[2], inputs[3])
        print('Stock has been updated.\n')
        break

# sorting key
# returns item code
def getCode(elem):
    return elem[0]

# sorts lists with sorting key and returns list of formatted strings
def itemString(list, func):
    types = list.pop(0)
    list.sort(key=func)
    newItems = []
    for item in list:
        newItems.append(f'{item[0]}\t\t{item[1]}\t{item[2]}\t{item[3]}')
    newItems.insert(0, '\t'.join(types))

    return newItems

# sorting key
# returns amount
def less25(elem):
    return int(elem[2])

# prints sorted inventory
# code for sorting by item code in ascending order
# 25 to sort for items with less than 25 stock
def printModInv(ppe, type):
    items = readFile(ppe)
    newItems = ''

    if type == 'code':
        newItems = itemString(items, func=getCode)
    elif type == '25':
        lessList = []
        lessList.append(items.pop(0))
        # get list of elements in items where int(i[2]) < 25
        less = [i for i in items if int(i[2]) < 25]

        if less:
            lessList += less
            newItems = itemString(lessList, func=less25)
        else:
            print('No stock less than 25.\n')
            return

    for item in newItems:
        print(item)
    print()

# sorting key
# returns hospital code
def getHos(elem):
    return elem[3]

# lets user search distribution log with item code
def search():
    dis = createDis()

    while True:
        clear()
        items = readFile(dis)
        newList = []
        newList.append(items.pop(0))
        code = getInputs(getMenu('search'))[0].upper()
        # get list of elements in items that contain code
        entries = [i for i in items if code in i]

        if not entries:
            re = retry('Item code does not exist in distribution file. Returning to main menu. Type "yes" if you want to re-enter: ')
            if re:
                continue
            else:
                break
        
        for entry in entries:
            # get list of elements in newList that contain entry[3]
            hasCode = [i for i in newList if entry[3] in i]
            if hasCode:
                num = int(hasCode[0][2])
                num += int(entry[2])
                # get the existing number within the list then set it to the new number
                newList[newList.index(hasCode[0])][2] = str(num)
            else:
                newList.append(entry)
        
        newItems = itemString(newList, func=getHos)
        clear()
        for item in newItems:
            print(item)
        print()
        dis.close()
        break

# displays options then prompts for input, returns input if input is int
def options(menu):
    while True:
        for line in menu:
            print(line)

        option = input('Choose an option: ')
        try:
            option = int(option)
            return option
        except:
            clear()
            print('Invalid input.\n')

# displays the main menus
# will keep looping unless user chooses to stop
# creates and closes the file objects every loop
def menu():
    clear()
    menu = getMenu('main')

    while True:
        ppe = createPPE()
        suppliers = createSuppliers()
        hospitals = createHospitals()
        option = options(menu)

        match option:
            # check details
            case 1:
                clear()
                op = options(getMenu('details'))
                clear()
                match op:
                    # ppe details
                    case 1:
                        print(ppe.read())
                    # supplier details
                    case 2:
                        print(suppliers.read())
                    # hospital details
                    case 3:
                        print(hospitals.read())
                    # sort by item code
                    case 4:
                        printModInv(ppe, 'code')
                    # show stock less than 25
                    case 5:
                        printModInv(ppe, '25')
            # update items
            case 2:
                clear()
                updateItem(ppe)
            # update misc
            case 3:
                clear()
                op = options(getMenu('misc'))
                clear()
                match op:
                    case 1:
                        updateMisc(suppliers)
                    case 2:
                        updateMisc(hospitals)
            # search
            case 4:
                clear()
                search()
            # end program
            case 5:
                clear()
                print('Program will now exit. Goodbye.')        
                ppe.close()
                suppliers.close()
                hospitals.close()
                break
            # invalid operation
            case _:
                clear()
                print('Invalid operation. Please choose a valid operation.\n')
        
        # close files after using them
        ppe.close()
        suppliers.close()
        hospitals.close()

menu()