import re
import sys
import time
import os
import psutil


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

# MAX_LENGTH = 400

AVOID_AT_START = r"[\\s\\]})>,']"
PUNCTUATION = r"[.!?…]|\\.{3}|[\\u2026\\u2047-\\u2049]|[\\p{Emoji_Presentation}\\p{Extended_Pictographic}]"
QUOTE_END = r"(?:'(?=`)|''(?=``))"
SENTENCE_END = fr"(?:{PUNCTUATION}(?<!{AVOID_AT_START}(?={PUNCTUATION}))|{QUOTE_END})(?=\\S|$)"
SENTENCE_BOUNDARY = fr"(?:{SENTENCE_END}|(?=[\\r\\n]|$))"
LOOKAHEAD_PATTERN = fr"(?:(?!{SENTENCE_END}).){{1,{LOOKAHEAD_RANGE}}}{SENTENCE_END}"
NOT_PUNCTUATION_SPACE = fr"(?!{PUNCTUATION}\\s)"
SENTENCE_PATTERN = fr"{NOT_PUNCTUATION_SPACE}(?:[^\\r\\n]{{1,{{MAX_LENGTH}}}}{SENTENCE_BOUNDARY}|[^\\r\\n]{{1,{{MAX_LENGTH}}}}(?={PUNCTUATION}|{QUOTE_END})(?:{LOOKAHEAD_PATTERN})?){AVOID_AT_START}*"


# AVOID_AT_START = r'[\s\]})>,\']'
# PUNCTUATION = r'[.!?…]|\.\.{3}|[\u2026\u2047-\u2049]|[\p{Emoji_Presentation}\p{Extended_Pictographic}]'
# QUOTE_END = r'(?:\'(?=\`)|\'\'(?=\`\`))'
# SENTENCE_END = rf'(?:{PUNCTUATION}(?<!{AVOID_AT_START}(?={PUNCTUATION}))|{QUOTE_END})(?=\S|$)'
# SENTENCE_BOUNDARY = rf'(?:{SENTENCE_END}|(?=[\r\n]|$))'
# LOOKAHEAD_PATTERN = rf'(?:(?!{SENTENCE_END}).){{1,{LOOKAHEAD_RANGE}}}{SENTENCE_END}'
# NOT_PUNCTUATION_SPACE = rf'(?!{PUNCTUATION}\s)'
# SENTENCE_PATTERN = rf'{NOT_PUNCTUATION_SPACE}(?:[^\r\n]{{1,{MAX_SENTENCE_LENGTH}}}{SENTENCE_BOUNDARY}|[^\r\n]{{1,{MAX_SENTENCE_LENGTH}}}(?={PUNCTUATION}|{QUOTE_END})(?:{LOOKAHEAD_PATTERN})?){AVOID_AT_START}*'

"""

"""

regex_pattern = (
    "(" +
    # 1. Headings (Setext-style, Markdown, and HTML-style, with length constraints)
    rf"(?:^(?:[#*=-]{{1,{MAX_HEADING_LENGTH}}}|\w[^\r\n]{{0,{MAX_HEADING_CONTENT_LENGTH}}}\r?\n[-=]{{2,{MAX_HEADING_UNDERLINE_LENGTH}}}|<h[1-6][^>]{{0,{MAX_HTML_HEADING_ATTRIBUTES_LENGTH}}}>)[^\r\n]{{1,{MAX_HEADING_CONTENT_LENGTH}}}(?:</h[1-6]>)?(?:\r?\n|$))" +
    "|" +

    # New pattern for citations
    rf"(?:\[[0-9]+\][^\r\n]{{1,{MAX_STANDALONE_LINE_LENGTH}}})" +
    "|" +



    # 2. List items (bulleted, numbered, lettered, or task lists, including nested, up to three levels, with length constraints)
    # rf"(?:(?:^|\r?\n)[ \t]{{0,3}}(?:[-*+•]|\d{{1,3}}\.\w\.|\[[ xX]\])[ \t]+{SENTENCE_PATTERN.replace(r"{MAX_LENGTH}", str(MAX_LIST_ITEM_LENGTH))}" +
    # rf"(?:(?:\r?\n[ \t]{{2,5}}(?:[-*+•]|\d{{1,3}}\.\w\.|\[[ xX]\])[ \t]+{SENTENCE_PATTERN.replace(r"{MAX_LENGTH}", str(MAX_LIST_ITEM_LENGTH))}){{0,{MAX_NESTED_LIST_ITEMS}}}" +
    # rf"(?:\r?\n[ \t]{{4,{MAX_LIST_INDENT_SPACES}}}(?:[-*+•]|\d{{1,3}}\.\w\.|\[[ xX]\])[ \t]+{SENTENCE_PATTERN.replace(r"{MAX_LENGTH}", str(MAX_LIST_ITEM_LENGTH))}){{0,{MAX_NESTED_LIST_ITEMS}}})?)" +
    # "|" +

    # rf"(?:(?:^|\r?\n)[ \t]{{0,3}}(?:[-*+•]|\d{{1,3}}\.\\w\.|\[[ xX]\])[ \t]+{SENTENCE_PATTERN.replace('{MAX_LENGTH}', str(MAX_LIST_ITEM_LENGTH))})" +
    # rf"|(?:(?:\r?\n[ \t]{{2,5}}(?:[-*+•]|\d{{1,3}}\.\\w\.|\[[ xX]\])[ \t]+{SENTENCE_PATTERN.replace('{MAX_LENGTH}', str(MAX_LIST_ITEM_LENGTH))})" + 
    # rf"|{{0,{MAX_NESTED_LIST_ITEMS}}}" + 
    # rf"|(?:\r?\n[ \t]{{4,{MAX_LIST_INDENT_SPACES}}}(?:[-*+•]|\d{{1,3}}\.\\w\.|\[[ xX]\])[ \t]+{SENTENCE_PATTERN.replace('{MAX_LENGTH}', str(MAX_LIST_ITEM_LENGTH))})" + 
    # rf"|{{0,{MAX_NESTED_LIST_ITEMS}}})?)" + 
    # "|" + 

    # r"(?:(?:^|\r?\n)[ \t]{0,3}(?:[-*+•]|\d{1,3}\.\w\.|\[[ xX]\])[ \t]+" + 
    # SENTENCE_PATTERN.replace(r"{MAX_LENGTH}", str(MAX_LIST_ITEM_LENGTH)) +
    # r"(?:(?:\r?\n[ \t]{2,5}(?:[-*+•]|\d{1,3}\.\w\.|\[[ xX]\])[ \t]+" + 
    # SENTENCE_PATTERN.replace(r"{MAX_LENGTH}", str(MAX_LIST_ITEM_LENGTH)) + 
    # r"){0," + str(MAX_NESTED_LIST_ITEMS) + r"}" +
    # r"(?:\r?\n[ \t]{4," + str(MAX_LIST_INDENT_SPACES) + r"}(?:[-*+•]|\d{1,3}\.\w\.|\[[ xX]\])[ \t]+" + 
    # SENTENCE_PATTERN.replace(r"{MAX_LENGTH}", str(MAX_LIST_ITEM_LENGTH)) + 
    # r"){0," + str(MAX_NESTED_LIST_ITEMS) + r"})?)"
    # r"|" + 



    # # 3. Block quotes (including nested quotes and citations, up to three levels, with length constraints)
    # rf"(?:(?:^>(?:>|\\s{{2,}}){{0,2}}{SENTENCE_PATTERN.replace(r'{{MAX_LENGTH}}', str(MAX_BLOCKQUOTE_LINE_LENGTH))}\r?\n?){{1,{MAX_BLOCKQUOTE_LINES}}})" +
    # "|" +

    # 4. Code blocks (fenced, indented, or HTML pre/code tags, with length constraints)
    rf"(?:(?:^|\r?\n)(?:```|~~~)(?:\w{{0,{MAX_CODE_LANGUAGE_LENGTH}}})?\r?\n[\\s\\S]{{0,{MAX_CODE_BLOCK_LENGTH}}}?(?:```|~~~)\r?\n?" +
    rf"|(?:(?:^|\r?\n)(?: {{4}}|\t)[^\r\n]{{0,{MAX_LIST_ITEM_LENGTH}}}(?:\r?\n(?: {{4}}|\t)[^\r\n]{{0,{MAX_LIST_ITEM_LENGTH}}}){{0,{MAX_INDENTED_CODE_LINES}}}\r?\n?)" +
    rf"|(?:<pre>(?:<code>)?[\\s\\S]{{0,{MAX_CODE_BLOCK_LENGTH}}}?(?:</code>)?</pre>))" +
    "|" +

    # 5. Tables (Markdown, grid tables, and HTML tables, with length constraints)
    rf"(?:(?:^|\r?\n)(?:\|[^\r\n]{{0,{MAX_TABLE_CELL_LENGTH}}}\|(?:\r?\n\|[-:]{{1,{MAX_TABLE_CELL_LENGTH}}}\|){{0,1}}(?:\r?\n\|[^\r\n]{{0,{MAX_TABLE_CELL_LENGTH}}}\|){{0,{MAX_TABLE_ROWS}}}" +
    rf"|<table>[\\s\\S]{{0,{MAX_HTML_TABLE_LENGTH}}}?</table>))" +
    "|" +

    # 6. Horizontal rules (Markdown and HTML hr tag)
    rf"(?:^(?:[-*_]){{{MIN_HORIZONTAL_RULE_LENGTH},}}\s*$|<hr\s*/?>)" +
    "|" +

    # # 10. Standalone lines or phrases (including single-line blocks and HTML elements, with length constraints)
    # rf"(?!{AVOID_AT_START})(?:^(?:<[a-zA-Z][^>]{{0,{MAX_HTML_TAG_ATTRIBUTES_LENGTH}}}>)?{SENTENCE_PATTERN.replace(r'{{MAX_LENGTH}}', str(MAX_STANDALONE_LINE_LENGTH))}(?:</[a-zA-Z]+>)?(?:\r?\n|$))" +
    # "|" +

    # # 7. Sentences or phrases ending with punctuation (including ellipsis and Unicode punctuation)
    # rf"(?!{AVOID_AT_START}){SENTENCE_PATTERN.replace(r'{{MAX_LENGTH}}', str(MAX_SENTENCE_LENGTH))}" +
    # "|" +

    # # 8. Quoted text, parenthetical phrases, or bracketed content (with length constraints)
    # "(?:" +
    # rf"(?<!\w)\"\"\"[^\"]{{0,{MAX_QUOTED_TEXT_LENGTH}}}\"\"\"(?!\w)" +
    # rf"|(?<!\w)(?:['\"`'])[^\r\n]{{0,{MAX_QUOTED_TEXT_LENGTH}}}\1(?!\w)" +
    # rf"|(?<!\w)`[^\r\n]{{0,{MAX_QUOTED_TEXT_LENGTH}}}'(?!\w)" +
    # rf"|(?<!\w)``[^\r\n]{{0,{MAX_QUOTED_TEXT_LENGTH}}}''(?!\w)" +
    # rf"|\([^\r\n(){{0,{MAX_PARENTHETICAL_CONTENT_LENGTH}}}(?:\([^\r\n(){{0,{MAX_PARENTHETICAL_CONTENT_LENGTH}}}\)[^\r\n(){{0,{MAX_PARENTHETICAL_CONTENT_LENGTH}}}){{0,{MAX_NESTED_PARENTHESES}}}\)" +
    # rf"|\[[^\r\n\[\]]{{0,{MAX_PARENTHETICAL_CONTENT_LENGTH}}}(?:\[[^\r\n\[\]]{{0,{MAX_PARENTHETICAL_CONTENT_LENGTH}}}\][^\r\n\[\]]{{0,{MAX_PARENTHETICAL_CONTENT_LENGTH}}}){{0,{MAX_NESTED_PARENTHESES}}}\]" +
    # rf"|\$[^\r\n$]{{0,{MAX_MATH_INLINE_LENGTH}}}\$" +
    # rf"|\`[^\`\r\n]{{0,{MAX_MATH_INLINE_LENGTH}}}\`" +
    # ")" +
    # "|" +

    # # 9. Paragraphs (with length constraints)
    # rf"(?!{AVOID_AT_START})(?:(?:^|\r?\n\r?\n)(?:<p>)?{SENTENCE_PATTERN.replace(r'{{MAX_LENGTH}}', str(MAX_PARAGRAPH_LENGTH))}(?:</p>)?(?=\r?\n\r?\n|$))" +
    # "|" +

    # 11. HTML-like tags and their content (including self-closing tags and attributes, with length constraints)
    rf"(?:<[a-zA-Z][^>]{{0,{MAX_HTML_TAG_ATTRIBUTES_LENGTH}}}(?:>[\\s\\S]{{0,{MAX_HTML_TAG_CONTENT_LENGTH}}}?</[a-zA-Z]+>|\\s*/>))" +
    "|" +

    # # 12. LaTeX-style math expressions (inline and block, with length constraints)
    rf"(?:(?:\$\$[\\s\\S]{{0,{MAX_MATH_BLOCK_LENGTH}}}?\$\$)|(?:\$[^\$\r\n]{{0,{MAX_MATH_INLINE_LENGTH}}}\$))" +
    "|" +

    # # 14. Fallback for any remaining content (with length constraints)
    # rf"(?!{AVOID_AT_START}){SENTENCE_PATTERN.replace(r'{{MAX_LENGTH}}', str(MAX_STANDALONE_LINE_LENGTH))}" +
    ")"
)

# Compile the regex pattern
regex = re.compile(regex_pattern, re.MULTILINE | re.UNICODE)

def format_bytes(size):
    # Function to format bytes as human-readable text
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024


def read_file(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
        return file.read()

test_text = read_file(sys.argv[1])

start_time = time.time()
start_memory = psutil.Process(os.getpid()).memory_info().rss

# Your matching logic here
matches = regex.findall(test_text)

end_time = time.time()
end_memory = psutil.Process(os.getpid()).memory_info().rss

execution_time = end_time - start_time
memory_used = end_memory - start_memory

print(f"Number of chunks: {len(matches) if matches else 0}")
print(f"Execution time: {execution_time:.3f} seconds")
print(f"Memory used: {memory_used / 1024:.2f} KB")

print('\nFirst 10 chunks:')
if matches:
    for match in matches[:10]:
        print(repr(match)[:50] + '...')
else:
    print('No chunks found.')


"""
// Define the regex pattern
// Headings
// Citations
// List items
// Block quotes
// Code blocks
// Tables
// Horizontal rules
// Standalone lines or phrases
// Sentences or phrases
// Quoted text, parenthetical phrases, or bracketed content
// Paragraphs
// HTML-like tags and their content
// LaTeX-style math expressions
// Fallback for any remaining content
// Read the regex and test text from files

"""