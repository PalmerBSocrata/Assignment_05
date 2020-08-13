#------------------------------------------#
# Title: CDInventory.py
# Desc: Script CDINventory to store CD Inventory data
# Change Log: (Who, When, What)
# DBiesinger, 2020-Jan-01, Created File
# PBandy, 2020-Aug-11, Added code to load data from file into memory
# PBandy, 2020-Aug-11, Added code to display data from file
# PBandy, 2020-Aug-12, Added code to add CD data into dict structure
# PBandy, 2020-Aug-12, Added code to merge user-entered data with data from file
# PBandy, 2020-Aug-12, Added code to save data to file
# PBandy, 2020-Aug-12, Added code to refresh data from file
#------------------------------------------#

from os import path

# Declare variables

strChoice = '' # User input
lstTblFromFile = []  # list of dicts to hold data loaded from file
dictRowFromFile = {}  # dict of data row loaded from file
lstTbl = [] # list of dicts to hold data user-entered data in memory
dictRow = {}  # dict of user-entered data
strFileName = 'CDInventory.txt'  # data storage file
objFile = None  # file object

# This creates the CDInventory.txt file with the desired schema, unless
# it already exists.
if not path.exists('CDInventory.txt'):
    inventory = open('CDInventory.txt', 'a')
    inventory.close()

# Let's go ahead and load file data into memory at program start
objFile = open(strFileName, 'r')
for row in objFile.readlines():
    strRow = row.strip().split(',')
    dictRowFromFile = { 'cd_id': strRow[0], 'cd_title': strRow[1], 'cd_artist': strRow[2] }
    lstTblFromFile.append(dictRowFromFile)
objFile.close()

# Get user Input
print('The Magic CD Inventory\n')
while True:
    # 1. Display menu allowing the user to choose:
    print('[l] Load Inventory from File\n[a] Add CD\n[i] Display Current Inventory')
    print('[d] Delete CD from Inventory\n[s] Save Inventory to File\n[x] Exit')
    strChoice = input('l, a, i, d, s or x: ').lower()  # convert choice to lower case at time of input
    print()

    if strChoice == 'x':
        # 5. Exit the program if the user chooses so
        break
    if strChoice == 'l':
        print('ID | CD Title | Artist')
        for row in lstTblFromFile:
            print('{} | {} | {}'.format(row['cd_id'], row['cd_title'], row['cd_artist']))
        print()
    elif strChoice == 'a':
        # 2. Add data to the _in memory_ table (2d-list) each time 
        # the user wants to add data
        strID = input('Enter an ID: ')
        strTitle = input('Enter the CD\'s Title: ').capitalize()
        strArtist = input('Enter the Artist\'s Name: ').capitalize()
        intID = int(strID)
        dictRow = { 'cd_id': intID, 'cd_title': strTitle, 'cd_artist': strArtist }
        lstTbl.append(dictRow)
        print()
    elif strChoice == 'i':
        # 3. Display the current data that would be saved to disk 
        # each time the user wants to display the data
        print('ID | CD Title | Artist')
        mergedList = lstTbl + lstTblFromFile
        for row in mergedList:
            print('{} | {} | {}'.format(row['cd_id'], row['cd_title'], row['cd_artist']))
        print()
    elif strChoice == 'd':
        # Deleting an entry
        deletion_id = input('What is the ID of the CD you would like to delete? ')
        for row in lstTblFromFile:
            if int(deletion_id) == int(row['cd_id']):
                lstTblFromFile.remove(row)
                print()
                print('Deleted ID #{} from in-memory data\n'.format(row['cd_id']))
                print('Please "Save Inventory to File" to delete this from the file')
                print()
            else:
                print('ID #{} not found'.format(row['cd_id']))
        for row in lstTbl:
            if int(deletion_id) == int(row['cd_id']):
                lstTbl.remove(row)
                print()
                print('Deleted ID #{} from in-memory data\n'.format(row['cd_id']))
                print('Please "Save Inventory to File" to delete this from the file')
                print()
            else:
                print('ID #{} not found'.format(row['cd_id']))
    elif strChoice == 's':
        # 4. Save the data to a text file CDInventory.txt if the user chooses so
        # Merge the user-entered data with the data loaded from the file
        mergedList = lstTbl + lstTblFromFile

        # Because we already have existing data from file plus the user-entered 
        # data in memory now, let's truncate the file before we write our data to it
        objFile = open(strFileName, 'w')
        objFile.truncate()
        objFile.close()
        
        # Now write the pre-existing plus newly-entered data to file
        for row in mergedList:
            strRow = '{},{},{}\n'.format(row['cd_id'], row['cd_title'], row['cd_artist'])
            objFile = open(strFileName, 'a')
            objFile.write(strRow)
            objFile.close()
        print('=====Saved to file=====')

        # Since we just saved new data to disk, let's clear out in-memory data
        lstTbl.clear()
        lstTblFromFile.clear()

        # And since we now have new data on disk, we should refresh the in memory data
        # because we loaded that on program start, but we're still in the loop here
        # so a user could keep doing things without issue :fingers-crossed:
        objFile = open(strFileName, 'r')
        for row in objFile.readlines():
            strRow = row.strip().split(',')
            dictRowFromFile = { 'cd_id': strRow[0], 'cd_title': strRow[1], 'cd_artist': strRow[2] }
            lstTblFromFile.append(dictRowFromFile)
        objFile.close()
    else:
        print('Please choose either l, a, i, d, s or x')
