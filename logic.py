from PyQt6.QtWidgets import *
from gui import *
import os
import csv
import random

class Logic(QMainWindow, Ui_MainWindow): #matches gui class
    def __init__(self) -> None:
        super().__init__() #uses QMainWindow constructor
        self.setupUi(self)

        self.list_sets()
        #self.list_flashcards.setCurrentRow(0)
        self.loaded_cards: set = []
        self.current_card: set = []
        self.card_side: bool = 1

        self.button_newset.clicked.connect(lambda : self.create_csv())
        self.button_addto.clicked.connect(lambda : self.add_to())
        self.button_reload.clicked.connect(lambda : self.list_sets())
        self.button_delete.clicked.connect(lambda : self.delete_set())
        self.button_practice.clicked.connect(lambda : self.load_set())
        self.button_flip_2.clicked.connect(lambda : self.display_cards())
        self.button_next_2.clicked.connect(lambda : self.next_card())

    def list_sets(self) -> None:
        '''
        Displays all CSV files in the current directory
        '''
        with os.scandir(os.getcwd()) as entries:
            flashcard_list: set = []
            for entry in entries:
                entry_name: str = entry.name[0:-4]
                entry_type: str = entry.name[-4:]

                if os.path.isfile(entry) == True and entry_type == '.csv':
                    flashcard_list.append(entry_name)
            self.list_flashcards.clear()
            self.list_flashcards.addItems(flashcard_list)

    def create_csv(self) -> None:
        '''
        Creates a csv file with the name in the textbox
        '''
        filename: str = self.lineEdit_setname.text().strip()
        csv_file: str = self.file_name(filename)
        
        try:
            if os.path.isfile(csv_file):
                raise FileExistsError
            elif not filename:
                raise NameError
            
        except FileExistsError:
            self.label_display.setText('File already exists')
        except NameError:
            self.label_display.setText('Name cannot be blank')

        else:
            with open(csv_file, 'w', newline='') as file:
                field_names = ['Front', 'Back']
                writer = csv.DictWriter(file, fieldnames=field_names, delimiter='\t')
                writer.writeheader()

            self.label_display.setText(f'Database file "{csv_file}" created successfully!')
            self.list_sets()

    def file_name(self, name_of_file: str) -> str:
        '''
        Ensures the name of a file includes the filetype .csv and returns the name of the file

        :param: name to be checked
        :return: name of the csv file with '.csv' at the end
        '''
        if name_of_file[-4:] != '.csv':
            name_of_file = f'{name_of_file}.csv'
                
        return name_of_file

    def load_set(self) -> set:
        '''
        Opens the selected CSV file, shuffles the contents, and loads the pairs into memory
        '''
        self.label_display.clear()
        
        
        try:
            db: str = f'{self.get_selection()}.csv'
            with open(db, 'r', newline='') as input_file:
                reader = csv.reader(input_file, delimiter='\t')
                lines = list(reader)
                shuffled_cards: set = []
                
                if not self.csv_verify(lines.pop(0)):
                    raise TypeError
                elif not lines:
                    raise ValueError
        
        except TypeError:
            self.label_display.setText('Error reading set')
        except ValueError:
            self.label_display.setText('Set empty')
        except FileNotFoundError:
            self.label_display.setText('No such file')
        except IndexError:
            self.label_display.setText('No set selected')

        else:
            while lines:
                random_card = lines.pop(random.randint(0,len(lines)-1))
                shuffled_cards.append(random_card)
            
            self.loaded_cards = shuffled_cards
            self.card_side = 1
            self.next_card()
                
    def display_cards(self) -> None:
        '''
        Switches between the front and back of a flashcard
        '''
        try:
            self.card_side = not self.card_side
            self.label_display.setText(self.current_card[self.card_side])

        except IndexError:
            self.label_display.setText('No more cards')
            self.clear_cards()

    def next_card(self) -> None:
        '''
        Displays the next card
        '''
        try:    
            card = self.loaded_cards.pop(0)
            self.current_card = card
            self.display_cards()

        except IndexError:
            self.label_display.setText('No more cards')
            self.clear_cards()

    def csv_verify(self, header: set) -> bool:
        '''
        Verifies if the CSV file contains the right headers
        :return: bool
        '''
        if header[0] != 'Front' and header[1] != 'Back':
            return False
        
        else:
            return True
    
    def get_selection(self) -> str:
        '''
        gets the name of the currently hightlighted set
        :return: the name of the currently hightlighted set
        '''
        try:
            current_row: int = self.list_flashcards.currentRow()
            if current_row < 0:
                raise ValueError
            current_selection = self.list_flashcards.item(current_row).text()
        
        except ValueError:
            self.label_display.setText('No set selected')
            raise IndexError
        
        else:
            return current_selection

    def add_to(self) -> None:
        '''
        Inserts a line into the current csv
        '''
        front: str = self.textedit_front.toPlainText().strip()
        back: str = self.textedit_back.toPlainText().strip()
        

        try:
            db: str = f'{self.get_selection()}.csv'

            if not front or not back:
                raise ValueError
        
        except ValueError:
            self.label_display.setText('Cards cannot be empty')
        except IndexError:
            self.label_display.setText('Please select a set')

        else:
            with open(db, 'a+', newline='') as card_set:
                writer = csv.DictWriter(card_set, fieldnames=['Front', 'Back'], delimiter='\t')
                writer.writerow({'Front': front, 'Back': back})

            self.label_display.setText(f'Card {front} added to set!')
            self.textedit_front.clear()
            self.textedit_back.clear()

    def confirmation(self) -> bool:
        '''
        Creates a confirmation box and returns the result with a bool
        :return: True or false (yes or no)
        '''
        window = QMessageBox()
        window.setWindowTitle('Confirmation')
        window.setText('Are you sure you want to delete this set?')
        window.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
        
        if window.exec() == QMessageBox.StandardButton.Ok:
            return True
        
        else:
            return False
        
    def clear_cards(self) -> None:
        '''
        Clears cards from memory
        '''
        self.loaded_cards = []
        self.current_card = []

    def delete_set(self) -> None:
        '''
        Deletes the currently selected set
        '''
        try:
            selection: str = self.get_selection()
            confirm = self.confirmation()
            if confirm:
                os.remove(f'{selection}.csv')
                self.clear_cards()
                self.label_display.setText('Flashcards deleted!')
            else:
                self.label_display.setText('Deletion cancelled')

        except FileNotFoundError:
            self.label_display.setText('No file selected')
        except IndexError:
            self.label_display.setText('No set selected')

        self.list_sets()