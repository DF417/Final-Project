import os
import csv
import random

def validate_db():
    
    while True:
        in_file = file_name(input('Input file name: ').strip())
        
        if os.path.isfile(in_file) == False:
            new_file_prompt = input('File does not exist! Create file?\n Enter (y/n): ')

            if new_file_prompt == 'y':
                new_file = create_csv(in_file)
                return new_file
        else:
            return in_file

def create_csv(file_title=False):
    '''creates from menu or prompt'''
    
    if file_title:
        csv_file = file_name(file_title)
    
    else:
        csv_file = file_name(input('Name your flashcards: '))
        
    with open(csv_file, 'w', newline='') as file:
        field_names = ['Front', 'Back']
        writer = csv.DictWriter(file, fieldnames=field_names, delimiter='\t')
        writer.writeheader()

    print(f'Database file "{csv_file}" created successfully!')
    edit_db(csv_file)
    return csv_file

def file_name(name_of_file):
    
    if name_of_file[-4:] == '.csv':
        csv_file_name = name_of_file
    
    else:
        csv_file_name = f'{name_of_file}.csv'
    
    return csv_file_name

def practice(db):
    with open(db, 'r', newline='') as input_file:
        reader = csv.reader(input_file, delimiter='\t')
        lines = list(reader)
        lines.pop(0) #removes header

        while lines:
            random_card = lines.pop(random.randint(0,len(lines)-1))

            next = False
            while next == False:
                print(random_card[0])
                input('enter any key to see answer ')
                print(random_card[1])
                review_confirmation = input('Review, next, or exit? r/n/x ')
                if review_confirmation == 'n':
                    next = True
                    if not lines:
                        input('practice done! enter any key to return to menu ')
                elif review_confirmation == 'x':
                    lines = False
                    break


def edit_db(db):
    newfile = os.path.isfile(db)

    with open(db, 'a+', newline='') as input_file:
        field_names = ['Front', 'Back']
        writer = csv.DictWriter(input_file, fieldnames=field_names, delimiter='\t')

        continue_input = True
        while continue_input == True:
            front_input = input('Front: ')
            back_input = input('Back: ')
            writer.writerow({'Front': front_input, 'Back': back_input})
            newline_prompt = input('Add new line? y/n: ')

            if newline_prompt == 'n':
                continue_input = False

    print('Database edited!')

def list_sets():
    with os.scandir(os.getcwd()) as entries:
        for entry in entries:
            if os.path.isfile(entry) == True and entry.name[-4:] == '.csv':
                print(entry.name[0:-4])

def delete_set():
    while True:
        in_file = file_name(input('Set to delete: ').strip())
        
        if os.path.isfile(in_file) == False:
            new_file_prompt = input('File does not exist! press any key to enter a different set or x to cancel ')
            if new_file_prompt == 'x':
                break
        else:
            selection = input(f'are you sure you want to delete {in_file}? y/n ')
            if selection == 'y':
                os.remove(in_file)
                print('Flashcards deleted!')
                break
            else:
                print('deletion cancelled')
                break

