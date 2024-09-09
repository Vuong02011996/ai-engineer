import re

regex_pattern = r"\BSpa" r"ain\B"
# Compile the regex pattern
regex = re.compile(regex_pattern, re.MULTILINE | re.UNICODE)

# Your matching logic here
test_text = "This is GSpan company"
# matches = regex.split(test_text) # ['This is G', 'n company'] 
# matches = regex.match(test_text) # None
# matches = regex.search(test_text) # <re.Match object; span=(9, 12), match='Spa'>
matches = regex.findall(test_text) # ['Spa']
print(matches)

regex_pattern = r"ain\B"