import re

# Farhan Ali
# i.farhanali.dev@gmail.com

# parse cookies and return a dictionary
# if cookies are not valid then returns a empty dictionary
def parse(cookies):
	parsed = {}
	if cookies is None: return parsed
	
	# magical regex (I don't know much about regex)
	res = re.findall("\s*(.*?)=(.*?);\s*", cookies)
	
	# cookies are invalid if it is None
	if res is not None:
		for data in res:
			if len(data) == 2:
				parsed[data[0]] = data[1]
	
	# return the parsed cookies dictionary
	return parsed
