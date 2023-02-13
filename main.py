import argparse

def get_arguments():
	parser = argparse.ArgumentParser()
	parser.add_argument("-a", "--aaa", dest="aaa", help="This is A???")
	arguments = parser.parse_args()
	# if not arguments.aaa:
		# parser.error("[-] Please specify arg 'aaa' .")
	return arguments

print("TIP ICS");

options = get_arguments()
if options.aaa:
	print(options.aaa)
else:
	print("Option aaa not entered")
