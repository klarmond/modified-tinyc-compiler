from __future__ import division
import re
import nltk
from nltk import Tree #functions used for drawing the tree

printDebugScanner = False
printDebugParser = False

choice1 = ""
choice2 = ""

#Determines whether or not to print certain info about the scanning and parsing operations.
#Eg: if 'y' is chosen for scanner, the tokens will be printed to the screen if the scan was successful
# if y is chosen for the parser, the current value of x, the token and the current stack are printed to the screen, followed by parse tree tokens
# given that the parse was successful
while choice1 != "y" and choice1 != "n" and choice1 != "Y" and choice1 != "N":
    choice1 = str(input("Do you want to print scanner token output to the screen (y/n)? >> "))

if choice1 == "y" or choice1 == "Y":
    printDebugScanner = True

while choice2 != "y" and choice2 != "n" and choice2 != "Y" and choice2 != "N":
    choice2 = str(input("Do you want to print parser debugging info to the screen (y/n)? >> "))

if choice2 == "y" or choice2 == "Y":
    printDebugParser = True

#######START OF SCANNER

#Used for printing "LEXICAL ERROR" to the file and the type of lexical error to the console so I could debug better while coding
def print_lexical_error(error_type):
    f_out = open("tokens.txt", "w")
    f_out.write("LEXICAL_ERROR")
    f_out.close()
    print("\nSCANNER MESSAGE:")
    print("--LEXICAL ERROR: " + error_type)

tokens = {"LP": "(",
          "RP": ")",
          "ASGN": "=",
          "SC": ";",
          "ADD": "+",
          "SUB": "-",
          "COMPARE": "<",
          "IF": "if",
          "WHILE": "while",
          "DO": "do"
          }

#regular expressions for identifying the different parts of the input and what they correspond to
reg_exp = {"LP": "^[(]",
           "RP": "^[)]",
           "ASGN": "^[=]",
           "SC": "^[;]",
           "ADD": "^[+]",
           "SUB": "^[-]",
           "COMPARE": "^[<]",
           "IF": "^(if)",
           "WHILE": "^(while)",
           "DO": "^(do)",
           "IDBEFORE": "^([a-z]+?(<|=|\+|-))",
           "IDBEFORE2": "^([a-zA-Z]+(?=<|=|\+|-){0,1})",
           "IDAFTER": "^[a-z]+",
           "NUMBEFORE": "^([0-9]+(?=<|=|\+|-){0,1})",
           "NUMAFTER": "^[0-9]+",
           "NUM2": ""}

#the list that will be stored to the tokens file
output = []
lex_error = False

try:
    f_in = open("source.tinyc", "r")
    text = ""
    for line in f_in:
        text = text + line

    f_in.close()
except FileNotFoundError:
    print("There's no 'source.tinyc' file in the directory")
    exit()

#get rid of all the whitespaces in the text
text = re.sub("[\s]+", "", text)
og_text = text

#store the last key whose regex value was used from reg_exp
last_key = ""
tracker = 0

#each time tokens are matched, they will be removed from the string so the loop will stop when the length is 0, but incase of an unrecognized lexical error that sends the the loop into
#an infinite loop, the tracker will indicated that the loop has iterated too many times and should end with an error
while text.__len__() > 0:

    #IDBEFORE
    try:
        #tries to use a key to match a regular expression stored as a value in a dictionary
        if re.search(reg_exp["IDBEFORE2"], text):
            #checks to see if the letter is immediately followed by a number, indicating an invalid id
            if(re.search("^([a-zA-Z]+(?=[0-9])+)", text)):
                lex_error = True
                print_lexical_error("ID LENGTH BEFORE w/ number")
                break

            x = re.match(reg_exp["IDBEFORE2"], text)

            if not re.search("(while|if|do)", x.group()): #and not re.search("\d", x.group()):
                id2 = x.group()
                #test if the matched id's length is not 1
                if id2.__len__() != 1:
                    lex_error = True
                    print_lexical_error("ID LENGTH BEFORE")
                    break
                else:
                    match2 = bool(re.search("[^a-z]", id2))

                    if match2:
                        lex_error = True
                        print_lexical_error("NON [a-z] ID")
                        break
                    else:
                        x = re.match("[a-z]+", x.group())

                text = text.replace(x.group(), "", 1) #remove the matched text in the string
                output.append("id: " + '"' + x.group() + '"') #add the stuff to the list for output
                last_key = "IDBEFORE"
    #Sometimes attribute errors occur when scanning for input
    except AttributeError:
        print("")

    #NUMBEFORE
    try:
        #checks if the number is followed immediately by a letter, which would indicate that it's part of an invalid ID
        if not re.search("^(\d+(?=[a-zA-Z])+)", text):
            if re.search(reg_exp["NUMBEFORE"], text):
                x = re.match(reg_exp["NUMBEFORE"], text)
                x = re.match("[0-9]+", x.group())
                text = text.replace(x.group(), "", 1) #remove the matched text in the string
                output.append("num: " + '"' + x.group() + '"') #add the stuff to the list for output
                last_key = "NUMBEFORE"
        else:
            x1 = re.match("^(\d+([a-zA-Z])+)", text)
            if re.search("(while|if|do)", x1.group()):
                x = re.match("[0-9]+", x1.group())
                text = text.replace(x.group(), "", 1)  # remove the matched text in the string
                output.append("num: " + '"' + x.group() + '"')  # add the stuff to the list for output
                last_key = "NUMBEFORE"
            else:
                lex_error = True
                print_lexical_error("ID length")
                break
    except AttributeError:
        print("")
######################################################
    #  if(1): last_key == "IDBEFORE" or last_key == "IDAFTER" or last_key == "NUMBEFORE" or last_key == "NUMAFTER" or last_key == "LP" or last_key == "RP":
    #  ADD
    try:
        if re.search(reg_exp["ADD"], text):
            x = re.match(reg_exp["ADD"], text)
            text = text.replace(x.group(), "", 1)
            output.append("ADD: " + '"' + x.group() + '"')
            last_key = "ADD"
    except AttributeError:
        print("")

    #  SUB
    try:
        if re.search(reg_exp["SUB"], text):
            x = re.match(reg_exp["SUB"], text)
            text = text.replace(x.group(), "", 1)
            output.append("SUB: " + '"' + x.group() + '"')
            last_key = "SUB"
    except AttributeError:
        print("")

    #  ASGN
    try:
        if re.search(reg_exp["ASGN"], text):
            x = re.match(reg_exp["ASGN"], text)
            text = text.replace(x.group(), "", 1)
            output.append("ASGN: " + '"' + x.group() + '"')
            last_key = "ASGN"
    except AttributeError:
        print("")

    #  COMPARE
    try:
        if re.search(reg_exp["COMPARE"], text):
            x = re.match(reg_exp["COMPARE"], text)
            text = text.replace(x.group(), "", 1)
            output.append("COMPARE: " + '"' + x.group() + '"')
            last_key = "COMPARE"
    except AttributeError:
        print("")
#################################################
    test = True
    if last_key == "ADD" or last_key == "SUB" or last_key == "ASGN" or last_key == "COMPARE" or last_key == "LP":

        #  IDAFTER
        try:
            if re.search(reg_exp["IDAFTER"], text):
                if (re.search("^([a-zA-Z]+(?=[0-9])+)", text)):
                    lex_error = True
                    print_lexical_error("ID LENGTH AFTER w/ number")
                    break

                x = re.match(reg_exp["IDAFTER"], text)

                if not re.search("(while|if|do)", x.group()):
                    x2 = x.group()

                    if re.search("(while|if|do)", x.group()):
                        if re.search(".(while|if|do)", x.group()) or re.search("(while|if|do).", x.group()):
                            lex_error = True
                            print_lexical_error("ID LENGTH W/ Keyword")
                            break
                        else:
                            x2 = re.sub("(while|if|do)", "", x2)

                    text = text.replace(x2, "", 1)

                    if x2.__len__() != 1:
                        lex_error = True
                        print_lexical_error("ID LENGTH AFTER")
                        break

                    output.append("id: " + '"' + x2 + '"')
                    last_key = "IDAFTER"
        except AttributeError:
            print("")

        #  NUMAFTER
        try:
            if re.search(reg_exp["NUMAFTER"], text):
                x = re.match(reg_exp["NUMAFTER"], text)
                text = text.replace(x.group(), "", 1)
                output.append("num: " + '"' + x.group() + '"')
                last_key = "NUMAFTER"

        except AttributeError:
            print("")
##########################################

    #  SC
    try:
        if re.search(reg_exp["SC"], text):
            x = re.match(reg_exp["SC"], text)
            text = text.replace(x.group(), "", 1)
            output.append("SC: " + '"' + x.group() + '"')
            last_key = "SC"
    except AttributeError:
        print("")

    #  LP
    try:
        if re.search(reg_exp["LP"], text):
            x = re.match(reg_exp["LP"], text)
            text = text.replace(x.group(), "", 1)
            output.append("LP: " + '"' + x.group() + '"')
            last_key = "LP"
    except AttributeError:
        print("")

    #  RP
    try:
        if re.search(reg_exp["RP"], text):
            x = re.match(reg_exp["RP"], text)
            text = text.replace(x.group(), "", 1)
            output.append("RP: " + '"' + x.group() + '"')
            last_key = "RP"
    except AttributeError:
        print("")

    #  IF
    try:
        if re.search(reg_exp["IF"], text):
            x = re.match(reg_exp["IF"], text)
            text = text.replace(x.group(), "", 1)
            output.append("IF: " + '"' + x.group() + '"')
            last_key = "IF"
    except AttributeError:
        print("")

    #  DO
    try:
        if re.search(reg_exp["DO"], text):
            x = re.match(reg_exp["DO"], text)
            text = text.replace(x.group(), "", 1)
            output.append("DO: " + '"' + x.group() + '"')
            last_key = "DO"
    except AttributeError:
        print("")

    #  WHILE
    try:
        if re.search(reg_exp["WHILE"], text):
            x = re.match(reg_exp["WHILE"], text)
            text = text.replace(x.group(), "", 1)
            output.append("WHILE: " + '"' + x.group() + '"')
            last_key = "WHILE"
    except AttributeError:
        print("")

    tracker += 1

    #  put a lexical error if the loop iterates too many times, indicating an unknown lexical error and print certain values for debugging
    if tracker > og_text.__len__():
        lex_error = True
        print_lexical_error("CODE ERROR")
        print("Last key: " + last_key)
        print("Error string: " + text)
        break

#  prints the token types and tokens in the console for debugging, given that there wasn't a lexical erros
if not lex_error:
    if printDebugScanner:
        print("TOKENS:")
        print(output)


#  if there wasn't a lexical error, the token types and tokens will be printed to the file
if not lex_error:
    f_out = open("tokens.txt", "w")
    for outputs in output:
        f_out.write(outputs + "\n")
    f_out.close()
    print("\nSCANNER MESSAGE:")
    print("--Token types and tokens have been printed to the file 'tokens.txt'.\n")
else:
    print("\nSCANNER MESSAGE:")
    print("--Can't proceed to parsing because of lexical error(s)")
    exit()

###########     END OF SCANNER      ######################################






##########  START OF PARSER##############


# function to return the next token in a list based on an index provided
def get_next_token(t_index):
    return tokens[t_index]


# uses the x and token values supplied to return the correct data from the parse tree rules
def PT(x1, token1):
    # the terminals and non-terminals obtained from each supplied combination will be a list, so if
    # the combination states that we must invoke rule 2 from the parse table, "<statement>",
    # "SC" and "<statement_list>" will be elements of a list which will be returned
    pt_output = []
    if x1 == "<program>":
        if token1 == "id" or token1 == "SC" or token1 == "WHILE" or token1 == "DO" or token1 == "IF" or token1 == "$":
            #  search_pt() will return all the terminals and non-terminals from the parse_list that are
            # associated with the parse rule number which is given as an argument to the function
            pt_output = search_PT("1")
            return pt_output

    if x1 == "<statement_list>":
        if token1 == "id" or token1 == "SC" or token1 == "WHILE" or token1 == "DO" or token1 == "IF":
            pt_output = search_PT("2")
            return pt_output
        if token1 == "$":
            pt_output = search_PT("3")
            return pt_output

    if x1 == "<statement>":
        if token1 == "id":
            pt_output = search_PT("7")
            return pt_output
        if token1 == "SC":
            pt_output = search_PT("8")
            return pt_output
        if token1 == "WHILE":
            pt_output = search_PT("5")
            return pt_output
        if token1 == "DO":
            pt_output = search_PT("6")
            return pt_output
        if token1 == "IF":
            pt_output = search_PT("4")
            return pt_output

    if x1 == "<paren_expr>":
        if token1 == "LP":
            pt_output = search_PT("9")
            return pt_output

    if x1 == "<expr>":
        if token1 == "num" or token1 == "id" or token1 == "LP":
            pt_output = search_PT("10")
            return pt_output

    if x1 == "<test>":
        if token1 == "num" or token1 == "id" or token1 == "LP":
            pt_output = search_PT("11")
            return pt_output

    if x1 == "<test_opt>":
        if token1 == "COMPARE":
            pt_output = search_PT("12")
            return pt_output
        if token1 == "RP" or token1 == "SC" or token1 == "WHILE":
            pt_output = search_PT("13")
            return pt_output

    if x1 == "<sum>":
        if token1 == "num" or token1 == "id" or token1 == "LP":
            pt_output = search_PT("14")
            return pt_output

    if x1 == "<sum_opt>":
        if token1 == "SUB":
            pt_output = search_PT("16")
            return pt_output
        if token1 == "ADD":
            pt_output = search_PT("15")
            return pt_output
        if token1 == "COMPARE" or token1 == "RP" or token1 == "SC" or token1 == "WHILE":
            pt_output = search_PT("17")
            return pt_output

    if x1 == "<term>":
        if token1 == "num":
            pt_output = search_PT("19")
            return pt_output
        if token1 == "id":
            pt_output = search_PT("18")
            return pt_output
        if token1 == "LP":
            pt_output = search_PT("20")
            return pt_output


# takes the number for a parse rule and searches the keys of the parse table dictionary to
# find the terminals and non-terminals we need, then returns those values as a list
def search_PT(pt_num):
    reg_ex = "(" + pt_num + ")[a|b|c|d]"
    key_list = []
    output_list = []
    for p in parse_table.keys():  # gets the parse table keys matched and adds them to the list of correct keys
        if re.match(reg_ex, p):
            key_list.append(p)

    # uses the keys obtained to fetch the terminals and non-terminals that said keys are associated with
    for p in key_list:
        output_list.append(parse_table.get(p))

    return output_list

#used to print the parse tree in a seperate window using the nltk library
def print_parse_tree(tokens1):
    #defining the production rules using nltk from the parse table given
    grammar_nltk = nltk.CFG.fromstring("""
        program -> statement_list
        statement_list -> statement 'SC' statement_list | E 
        statement -> 'IF' paren_expr statement | 'WHILE' paren_expr statement | 'DO' statement 'WHILE' paren_expr | 'id' 'ASGN' expr | 'SC'
        paren_expr -> 'LP' expr 'RP'
        expr -> test
        test -> sum test_opt
        test_opt -> 'COMPARE' sum | E
        sum -> term sum_opt
        sum_opt -> 'ADD' term sum_opt | 'SUB' term sum_opt | E
        term -> 'id' | 'num' | paren_expr
        E -> 
    """)

    parser_nltk = nltk.RecursiveDescentParser(grammar_nltk)
    trees = parser_nltk.parse(tokens1)
    for tree in trees:
        print("")
    t = Tree.fromstring(str(tree))
    t.draw()

try:
    p_file_in = open("tokens.txt", "r")
    p_text = ""
    for line in p_file_in:
        p_text = p_text + line

    p_file_in.close()
except FileNotFoundError:
    print("There's no 'tokens.txt' file to parse")
    exit()

token_types = re.findall("[a-zA-Z]+(?=:)", p_text)
tokens0 = re.findall('(".")', p_text)
tokens = []
i = 0
# for token in tokens0:
#     tokens.append(re.sub('"', "", token))

tokens = token_types

token_types.append("$")

parse_table = {
    "1a": "<statement_list>",
    "2a": "<statement>",
    "2b": "SC",
    "2c": "<statement_list>",
    "3a": "",
    "4a": "IF",
    "4b": "<paren_expr>",
    "4c": "<statement>",
    "5a": "WHILE",
    "5b": "<paren_expr>",
    "5c": "<statement>",
    "6a": "DO",
    "6b": "<statement>",
    "6c": "WHILE",
    "6d": "<paren_expr>",
    "7a": "id",
    "7b": "ASGN",
    "7c": "<expr>",
    "8a": "SC",
    "9a": "LP",
    "9b": "<expr>",
    "9c": "RP",
    "10a": "<test>",
    "11a": "<sum>",
    "11b": "<test_opt>",
    "12a": "COMPARE",
    "12b": "<sum>",
    "13a": "",
    "14a": "<term>",
    "14b": "<sum_opt>",
    "15a": "ADD",
    "15b": "<term>",
    "15c": "<sum_opt>",
    "16a": "SUB",
    "16b": "<term>",
    "16c": "<sum_opt>",
    "17a": "",
    "18a": "id",
    "19a": "num",
    "20a": "<paren_expr>",
}

# list of terminals that'll be looped through to test if x is a terminal or not when parsing
terminals = ["num", "id", "SUB", "ADD", "COMPARE", "RP", "LP", "SC", "ASGN", "WHILE", "DO", "IF", "$"]

stack = []
i = 0  # used to track the current token that needs to be fetchedusing get_next_token from the list of tokens
passes = 0  # track the number of times the parse loop has ran for debugging purposes
test = ""
stack.append("$")
stack.append("<program>")
token = get_next_token(i)
x = stack[-1]  # set x to the top of the stack
final = []  # list to store the final output that will be written to the file
t_found = False  # used to indicate whether or not x was found in the list of terminals

while x != "$":
    passes = passes + 1  # track passes to output to screen
    if printDebugParser:
        print("Pass: " + str(passes))
        print("x: " + x + "\ttoken: " + token)

    t_found = False
    for terminal in terminals:  # search each value in the terminals list to see if x matches any of them
        if x == terminal:
            t_found = True  # indicate that x is a terminal by setting t_found to true
            break

    if t_found:  # if x is a terminal or $
        if x == token:
            i = i + 1
            test = test + "(" + stack[-1] + ") "
            final.append(stack.pop())
            token = get_next_token(i)
        else:
            print("\nPARSER MESSAGE:")
            print("--THERE WAS A SYNTAX ERROR(ERR 1) - - No parse tree could be made")
            exit()

    else:  # if x is a non-terminal like <statement>
        # search for and return the non-terminals corresponding to the combination given needed as a list
        y_list = PT(x, token)

        if y_list is not None:  # indicates that a combination was found in the parse table for the given x and token
            test = test + "(" + stack[-1] + ") "
            final.append(stack.pop())  # adding the popped value to the final list of output we'll generate
            count = y_list.__len__() - 1
            for stuff in range(y_list.__len__()):  # loop through the non terminals returned and push them to the stack
                # if the first value in y_list is an empty string,
                # it means that the combination of x and token that we got is supposed to be an empty
                # value (E or whatever it's called ) so we don't need to actually add it to the stack
                if y_list[count] != "":
                    stack.append(y_list[count])  # adds the terminal or non terminal obtained to the stack
                    # prints the current terminal or non-terminal obtained in the current pass
                    # from the list for debugging purposes
                    if printDebugParser:
                        print(str(count) + " " + y_list[count])
                    count = count - 1

        else:
            print("\nPARSER MESSAGE:")
            print("--THERE WAS A SYNTAX ERROR(ERR 2) - No parse tree could be made")
            if not printDebugParser:
                print("--Run the program again with 'y' selected for parser debugging to see where the parsing stopped")
            exit()

    if printDebugParser:
        print("stack: " + str(stack))  # print the stack for the current pass
        print("\n")
    t_found = False  # resets the t_found value to avoid unintended True values for if x is a terminal
    x = stack[-1]

if printDebugParser:
    print("Parse tree tokens:")
    print(final)

try:
    p_file_out = open("parse_tree.txt", "w")

    for out in final:
        p_file_out.write(out + "\n")
    p_file_out.close()
except FileNotFoundError:
    print("Couldn't print output file")
finally:
    print("\nPARSER MESSAGE:")
    print("--Parse tree tokens printed to the file 'parse.txt'.")
    token_types.pop()  # to get ird of the '$' at the end of the list
    print_parse_tree(token_types)



########END OF PARSER