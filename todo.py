import sys
import datetime
import json

class Todo:
	def __init__(self, content):
		self.date = str(datetime.date.today())
		self.content = content

def main(argv):

	#Initalize todo list
	todos = []
	data = {}
	try:
		with open("todos.json", 'r') as read_file:
			data = json.load(read_file)
	except Exception as e:
		print("file not found")
		print(e)

	#Initial list display
	displayTodos(todos,data)

	#Command prompting
	while(True):
		print("-" * 40)
		command = input('''Enter a command:
	a : add a new todo
	r : delete todo
	f : mark todo as finished
	d : display todos
	sq: save and quit
	q : quit without saving
''').lower()

		if command == 'd':
			displayTodos(todos,data)
		elif command == 'sq':
			saveTodos(data,todos)
			print("Save and quit.\nGoodbye.")
			sys.exit(0)
		elif command == 'q':
			save = input('Save before exiting?: ')
			if save.lower().startswith("y"):
				saveTodos(data,todos)
				print("Save and quit.\nGoodbye.")
			else:
				print("Exit without saving...")
			sys.exit(0)
		elif command == 'a':
			print("Add a todo!")
			content = input("Content: ")
			todo = Todo(content)
			todos.append(todo)
		elif command == 'r':	
			toRemove = input("Remove which item?: ")
			# try to remove from data array (loaded todos)
			# if exception, tries to remove from unsaved todo list
			# further exception means invalid input
			try:
				index = int(toRemove) - 1
				removed = data[index]
				removeTodo(data,index)
				print("Removed {0} - {1}".format(toRemove,removed['content']))
			except Exception as err:
				try:
					# toRemove adjusted users can delete by entered displayed number 
					# rather than actual index
					index = int(toRemove) - len(data) - 1
					removed = todos[index]
					removeTodo(todos,index)
					print("Removed {0} - {1}".format(toRemove,removed.content))
				except Exception as err:	
					print("Invalid input\n")
		elif command == 'f':
			finished = input("Enter line number: ")
			try:
				index = int(finished)-1
				copy = data[index]
				strikeout = ''
				for c in copy['content']:
					strikeout = strikeout + c + '\u0336'
				data[index]['content'] = strikeout
			except Exception as err:
				try:
					index = int(finished)-len(data)-1
					copy = todos[index]
					strikeout = ''
					for c in copy.content:
						strikeout = strikeout + c + '\u0336'
					todos[index].content = strikeout
				except Exception as err:
					print("Invalid input\n")
		else:
			print("Invalid Command")

#code I found to handle datetime objects converted to json
def converter(obj):
	if isinstance(object, datetime.datetime):
		return object.__str__()

def displayTodos(todos, data):
	index = 1

	#display todos loaded from json (data[])
	for todo in data:
		print("{0:>6}. {1} | {2}".format(index,str(todo['date']),todo['content']))
		index += 1

	#display unsaved todos (todos[])
	for todo in todos:
		print("{0:>6}. {1} | {2}".format(index,str(todo.date),todo.content))
		index += 1

def removeTodo(todos,index):
	todos.pop(index)

def saveTodos(data, todos):
	js_out = []
	for todo in data:
		js_out.append(todo)
	with open("todos.json", 'w') as fout:
		for todo in todos:
			js_out.append(vars(todo))
		json.dump(js_out, fout, default=converter)

if __name__ == "__main__":
    main(sys.argv[1:])

