import re

# Farhan Ali
# i.farhanali.dev@gmail.com

# Magical Regex
MAGIC = r"\s*(.*?)=(.*?);\s*"

# parse cookies and return a dictionary
# If cookies are not valid then return an empty dictionary
def parse(cookies):
	if not isinstance(cookies, str):
		raise Exception(f"parse() requires a str, but got {type(cookies).__name__}")

	# Doing magic here
	res = re.findall(MAGIC, cookies)
	
	# Cookies are invalid if it is None
	parsed = {}
	if res is None or len(res) == 0:
		return parse
	
	for data in res:
		if len(data) == 2:
			parsed[data[0].strip()] = data[1].strip()
	
	# return the parsed cookies dictionary
	return parsed


def encode_cookies(cookies):
	if not isinstance(cookies, dict):
		raise Exception(f"encode_cookies requires a dict, but got {type(cookies).__name__}")

	encoded = []

	# append cookies in a list as key=value
	for k,v in cookies.items():
		encoded.append("%s=%s" % (k, v))
	
	# adding ; at the end of each cookie and returns the final string
	return "; ".join(encoded)
