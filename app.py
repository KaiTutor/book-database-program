# import models
from models import Base, session, Book, engine
import datetime
import csv
import time

def menu():
	while True:
		print('''
			\nPROGRAMMING BOOKS
			\r1) ADD BOOK
			\r2) VIEW ALL BOOKS
			\r3) SEARCH FOR BOOKS
			\r4) BOOK ANALYSIS
			\r5) EXIT
			\n''')
		choice = input('What would you like to do? ')
		if choice in ['1', '2', '3', '4', '5']:
			return choice
		else:
			input('''
				\rPlease choose one of the options above
				\rA number 1-5.
				\rPress enter to try again 
				\n''')

def submenu():
	while True:
		print('''
			\r1) EDIT BOOK
			\r2) DELETE BOOKS
			\r3) RETURN TO MENU 
			\n''')
		choice = input('What would you like to do? ')
		if choice in ['1', '2', '3']:
			return choice
		else:
			input('''
				\rPlease choose one of the options above
				\rA number 1-3.
				\rPress enter to try again 
				\n''')

# add books to database

# edit books

# delete books

# search 

# data cleaning 

# loop runs our program 


def clean_date(date_str):
	months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
	split_date = date_str.split(' ')

	try:
		month = int(months.index(split_date[0]) + 1)
		day = int(split_date[1].split(',')[0])
		year = int(split_date[2])
		return_date = datetime.date(year, month, day)
	except ValueError:
		input('''
			\n***** Date Error ****
			\r Date format should include a valid month, day, year
			\rEx: January 13, 2003
			\rPress enter to try again
			\r************************
			''')
		return
	else:
		return return_date

def clean_price(price_str):
	try:
		price_float = float(price_str)
		return_price = int(price_float * 100)
	except ValueError:
		input('''
			\n***** Price Error ****
			\r Price Format should be a number with no currency symbol
			\rEx: 10.99
			\rPress enter to try again
			\r************************
			''')
		return
	else:
		return return_price

def clean_id(id_str, options):
	try:
		book_id = int(id_str)

	except ValueError:
		input('''
			\n***** ID Error ****
			\r ID Format should be a number
			\rEx: 3
			\rPress enter to try again
			\r************************
			''')
		return
	else:
		if book_id in options:
			return book_id
		else:
			input('''
			\n***** ID Error ****
			\r ID should be number in options
			\rPress enter to try again
			\r************************
			''')
			return


def edit_check(column_name, current_value):
	print(f'\n *** EDIT {column_name} ***')
	if column_name == 'Price':
		print(f'\r Current Value: {current_value/100}')
	elif column_name == 'Date':
		print(f'\rCurrent Value: {current_value.strftime("%B %D, %y")}')
	else:
		print(f'\rCurrent Value: {current_value}')

	if column_name == 'Date' or column_name == 'Price':
		while True:
			changes = input('What would you like to change the value to? ')
			if column_name == 'Date':
				changes = clean_date(changes)
				if type(changes) == datetime.date:
					return changes
			if column_name == 'Price':
				changes = clean_price(changes)
				if type(changes) == int:
					return changes
	else:
		return input('What would you like to change the value to? ')



def add_csv():
	with open("suggested_books.csv") as csvfile:
		data = csv.reader(csvfile)

		for row in data:
			# checks if book is there returns none if not
			book_in_db = session.query(Book).filter(Book.title==row[0]).one_or_none()

			if book_in_db == None:
				title = row[0]
				author = row[1]
				date = clean_date(row[2])
				price = clean_price(row[3])
				new_book = Book(title=title, author=author, published_date=date, price=price)
				session.add(new_book)

		session.commit()


def app():
	app_running = True

	while app_running:
		choice = menu()

		if choice == '1':
			# add book
			title = input('Title: ')
			author = input('Author: ')

			date_error = True
			while date_error:
				date = input('Date Published (Ex: October 25, 2017): ')
				date = clean_date(date)
				if type(date) == datetime.date:
					date_error = False

			price_error = True
			while price_error:
				price = input('Price (Ex. 25.64): ')
				price = clean_price(price)
				if type(price) == int:
					price_error = False

			new_book = Book(title=title, author=author, published_date=date, price=price)
			session.add(new_book)
			session.commit()

			print('Book Added!')
			time.sleep(1.5)

		elif choice == '2':
			# view books
			for book in session.query(Book):
				print(f'\n{book.id} | {book.title} | {book.author}')
			input('\nPress enter to return to main menu.')

		elif choice == '3':
			# search for books
			id_options = []
			for book in session.query(Book):
				id_options.append(book.id)

			id_error = True
			while id_error:	
				id_choice = input(f'''
					\nId Options: {id_options}
					\rBook Id: ''')
				id_choice = clean_id(id_choice, id_options)
				if type(id_choice) == int:
					id_error = False

			the_book = session.query(Book).filter(Book.id==id_choice).first()
			print(f'''
				\n {the_book.title} by {the_book.author}
				\r Published$ {the_book.published_date}
				\r Price: ${the_book.price / 100}
				''')
			
			sub_choice = submenu()
			if sub_choice == '1':
				#edit
				the_book.title = edit_check('Title', the_book.title)
				the_book.author = edit_check('Author', the_book.author)
				the_book.published_date = edit_check('Published', the_book.published_date)
				the_book.price = edit_check('Price', the_book.price)
				session.commit()
				print(session.dirty)
				print('Book Updated')
				time.sleep(1.5)

			elif sub_choice == '2':
				# delete
				session.delete(the_book)
				session.commit()
				print('Book deleted')
				time.sleep(1.5)


		elif choice == '4':
			# book analysis
			oldest_book = session.query(Book).order_by(Book.published_date).first()
			newest_book = session.query(Book).order_by(Book.published_date.desc()).first()
			total_books = session.query(Book).count()
			python_books = session.query(Book).filter(Book.title.like('%python%')).count()
			print(f'''\n Book Analysis
				\rOldest Book: {oldest_book.title}
				\rNewest Book: {newest_book.title}
				\rTotal Books: {total_books}
				\rPython Books: {python_books}
				''')
			input('\nPress enter to return to main menu')

		elif choice == '5':
			# exit
			print("Goodbye")
			app_running = False
		else:
			print("something wrong with choice")
			app_running = False


if __name__ == '__main__':
	Base.metadata.create_all(engine)
	
	#add_csv()
	app()

	#for book in session.query(Book):
	#	print(book)







