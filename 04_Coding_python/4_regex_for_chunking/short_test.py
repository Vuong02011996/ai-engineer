import re
import sys
MAX_HEADING_LENGTH = 7
MAX_HEADING_CONTENT_LENGTH = 200
MAX_HEADING_UNDERLINE_LENGTH = 200
MAX_HTML_HEADING_ATTRIBUTES_LENGTH = 100
MAX_LIST_ITEM_LENGTH = 200
MAX_NESTED_LIST_ITEMS = 6
MAX_LIST_INDENT_SPACES = 7
MAX_BLOCKQUOTE_LINE_LENGTH = 200
MAX_BLOCKQUOTE_LINES = 15
MAX_CODE_BLOCK_LENGTH = 1500
MAX_CODE_LANGUAGE_LENGTH = 20
MAX_INDENTED_CODE_LINES = 20
MAX_TABLE_CELL_LENGTH = 200
MAX_TABLE_ROWS = 20
MAX_HTML_TABLE_LENGTH = 2000
MIN_HORIZONTAL_RULE_LENGTH = 3
MAX_SENTENCE_LENGTH = 400
MAX_QUOTED_TEXT_LENGTH = 300
MAX_PARENTHETICAL_CONTENT_LENGTH = 200
MAX_NESTED_PARENTHESES = 5
MAX_MATH_INLINE_LENGTH = 100
MAX_MATH_BLOCK_LENGTH = 500
MAX_PARAGRAPH_LENGTH = 1000
MAX_STANDALONE_LINE_LENGTH = 800
MAX_HTML_TAG_ATTRIBUTES_LENGTH = 100
MAX_HTML_TAG_CONTENT_LENGTH = 1000
LOOKAHEAD_RANGE = 100 #// Number of characters to look ahead for a sentence boundary

MAX_LENGTH = 400

AVOID_AT_START = r"[\\s\\]})>,']"
PUNCTUATION = r"[.!?…]|\\.{3}|[\\u2026\\u2047-\\u2049]|[\\p{Emoji_Presentation}\\p{Extended_Pictographic}]"
QUOTE_END = r"(?:'(?=`)|''(?=``))"
SENTENCE_END = fr"(?:{PUNCTUATION}(?<!{AVOID_AT_START}(?={PUNCTUATION}))|{QUOTE_END})(?=\\S|$)"
SENTENCE_BOUNDARY = fr"(?:{SENTENCE_END}|(?=[\\r\\n]|$))"
LOOKAHEAD_PATTERN = fr"(?:(?!{SENTENCE_END}).){{1,{LOOKAHEAD_RANGE}}}{SENTENCE_END}"
NOT_PUNCTUATION_SPACE = fr"(?!{PUNCTUATION}\\s)"
# SENTENCE_PATTERN = fr"{NOT_PUNCTUATION_SPACE}(?:[^\\r\\n]{{1,{{MAX_LENGTH}}}}{SENTENCE_BOUNDARY}|[^\\r\\n]{{1,{{MAX_LENGTH}}}}(?={PUNCTUATION}|{QUOTE_END})(?:{LOOKAHEAD_PATTERN})?){AVOID_AT_START}*"
SENTENCE_PATTERN = fr"{NOT_PUNCTUATION_SPACE}(?:[^\\r\\n]{{1,{MAX_LENGTH}}}{SENTENCE_BOUNDARY}|[^\\r\\n]{{1,{MAX_LENGTH}}}(?={PUNCTUATION}|{QUOTE_END})(?:{LOOKAHEAD_PATTERN})?){AVOID_AT_START}*"
regex_pattern = (
    "(" +
    # 1. Headings (Setext-style, Markdown, and HTML-style, with length constraints)
    rf"(?:^(?:[#*=-]{{1,{MAX_HEADING_LENGTH}}}|\w[^\r\n]{{0,{MAX_HEADING_CONTENT_LENGTH}}}\r?\n[-=]{{2,{MAX_HEADING_UNDERLINE_LENGTH}}}|<h[1-6][^>]{{0,{MAX_HTML_HEADING_ATTRIBUTES_LENGTH}}}>)[^\r\n]{{1,{MAX_HEADING_CONTENT_LENGTH}}}(?:</h[1-6]>)?(?:\r?\n|$))" +
    
    # rf"(?:(?:^>(?:>|\\s{{2,}}){{0,2}}{SENTENCE_PATTERN.replace(str(MAX_LENGTH), str(MAX_BLOCKQUOTE_LINE_LENGTH))}\r?\n?){{1,{MAX_BLOCKQUOTE_LINES}}})" +
    # rf"(?:(?:^>(?:>|\\s{{2,}}){{0,2}}{SENTENCE_PATTERN.replace(str(MAX_LENGTH), str(MAX_BLOCKQUOTE_LINE_LENGTH))}\r?\n?){{1,{MAX_BLOCKQUOTE_LINES}}})" +
    
    # rf"(?!{AVOID_AT_START}){SENTENCE_PATTERN.replace(r'{{MAX_LENGTH}}', str(MAX_SENTENCE_LENGTH))}" +
    ")" 
)


# Compile the regex pattern
regex = re.compile(regex_pattern, re.MULTILINE | re.UNICODE)


def read_file(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
        return file.read()

file_path = "/home/oryza/Downloads/test_reg_1.txt"

test_text = read_file(file_path)
matches = regex.findall(test_text) # ['Spa']
print(matches)