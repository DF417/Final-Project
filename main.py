from logic import *

def main():
    application=QApplication([])
    window=Logic()
    window.show()
    application.exec()


'''
    while True:
        list_sets()
        selection = input('please select what you want:\nPractice sets\nNew set\nadd to set\nDelete set\n(p/n/e/d) ')
        
        if selection == 'p':
            user_file = validate_db()
            practice(user_file)
        
        elif selection == 'e':
            user_file = validate_db()
            edit_db(user_file)
            
            selection = input('would you like to practice your edited set? y/n ')
            if selection == 'n':
                break
            
            practice(user_file)
        
        elif selection == 'n':
            user_file = create_csv()
            
            selection = input('would you like to practice your new set? y/n ')
            if selection == 'n':
                break
            
            practice(user_file)
        
        elif selection == 'd':
            delete_set()
            '''
if __name__ == '__main__':
    main()