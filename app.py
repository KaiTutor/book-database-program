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
			pass
		elif choice == '3':
			# search for books
			pass
		elif choice == '4':
			# book analysis
			pass
		elif choice == '5':
			# exit
			print("Goodbye")
			app_running = False
		else:
			print("something wrong with choice")
			app_running = False


if __name__ == '__main__':
	Base.metadata.create_all(engine)
	
	add_csv()
	app()

	for book in session.query(Book):
		print(book)







