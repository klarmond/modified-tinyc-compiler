# modified-tinyc-compiler
A scanner and parser for a smaller version of the tiny-c language.  

Uses BNF grammar and a list of lexical items to generate a dictionary of symbols
and tokens extracted from the source.tinyc file provided.
 

Uses a table-driven predictive parser. The stream of tokens from the scanner
is used as input to generate a parse tree that is displayed in pre-order traversal.


The nltk (Natural language toolkit) library is implemented to generate an image of 
the parse tree.


Takes as input a source.tinyc file in the same directory and returns:

    A file with all the recognized tokens.
    A file with the parse tree.
    An image representation of the parse tree using the nltk library.

Recognized symbols and keywords and their respective tokens:

    LP = “(“
    RP = “)”
    ASGN = “=”
    SC = “;”
    ADD = “+”
    SUB = “-”
    COMPARE = “<”

    IF = “if”
    WHILE = “while”
    DO = “do”
    
Sample input (source.tinyc file content):

    x = 10;
    y = 20;

    if (x < y)
      while (x < y)
        x = x + 1;
        
 Tokens.txt file output:
 
    id: "x"
    ASGN: "="
    num: "10"
    SC: ";"
    id: "y"
    ASGN: "="
    num: "20"
    SC: ";"
    IF: "if"
    LP: "("
    id: "x"
    COMPARE: "<"
    id: "y"
    RP: ")"
    WHILE: "while"
    LP: "("
    id: "x"
    COMPARE: "<"
    id: "y"
    RP: ")"
    id: "x"
    ASGN: "="
    id: "x"
    ADD: "+"
    num: "1"
    SC: ";"

   Parse_tree.txt file output:
   
    <program>
    <statement_list>
    <statement>
    id
    ASGN
    <expr>
    <test>
    <sum>
    <term>
    num
    <sum_opt>
    <test_opt>
    SC
    <statement_list>
    <statement>
    id
    ASGN
    <expr>
    <test>
    <sum>
    <term>
    num
    <sum_opt>
    <test_opt>
    SC
    <statement_list>
    <statement>
    IF
    <paren_expr>
    LP
    <expr>
    <test>
    <sum>
    <term>
    id
    <sum_opt>
    <test_opt>
    COMPARE
    <sum>
    <term>
    id
    <sum_opt>
    RP
    <statement>
    WHILE
    <paren_expr>
    LP
    <expr>
    <test>
    <sum>
    <term>
    id
    <sum_opt>
    <test_opt>
    COMPARE
    <sum>
    <term>
    id
    <sum_opt>
    RP
    <statement>
    id
    ASGN
    <expr>
    <test>
    <sum>
    <term>
    id
    <sum_opt>
    ADD
    <term>
    num
    <sum_opt>
    <test_opt>
    SC
    <statement_list>
    
 Image of parse tree generated:
 ![Parse tree image](https://i.gyazo.com/15967da79e5ed1760010b3e74e4599e4.png)
    
Console output:    

    Do you want to print scanner token output to the screen (y/n)? >> y
    Do you want to print parser debugging info to the screen (y/n)? >> y
    TOKENS:
    ['id: "x"', 'ASGN: "="', 'num: "10"', 'SC: ";"', 'id: "y"', 'ASGN: "="', 'num: "20"', 'SC: ";"', 'IF: "if"', 'LP: "("', 'id: "x"', 'COMPARE: "<"', 'id: "y"', 'RP: ")"', 'WHILE: "while"', 'LP: "("', 'id: "x"', 'COMPARE: "<"', 'id: "y"', 'RP: ")"', 'id: "x"', 'ASGN: "="', 'id: "x"', 'ADD: "+"', 'num: "1"', 'SC: ";"']

    SCANNER MESSAGE:
    --Token types and tokens have been printed to the file 'tokens.txt'.

    Pass: 1
    x: <program>	token: id
    0 <statement_list>
    stack: ['$', '<statement_list>']


    Pass: 2
    x: <statement_list>	token: id
    2 <statement_list>
    1 SC
    0 <statement>
    stack: ['$', '<statement_list>', 'SC', '<statement>']


    Pass: 3
    x: <statement>	token: id
    2 <expr>
    1 ASGN
    0 id
    stack: ['$', '<statement_list>', 'SC', '<expr>', 'ASGN', 'id']


    Pass: 4
    x: id	token: id
    stack: ['$', '<statement_list>', 'SC', '<expr>', 'ASGN']


    Pass: 5
    x: ASGN	token: ASGN
    stack: ['$', '<statement_list>', 'SC', '<expr>']


    Pass: 6
    x: <expr>	token: num
    0 <test>
    stack: ['$', '<statement_list>', 'SC', '<test>']


    Pass: 7
    x: <test>	token: num
    1 <test_opt>
    0 <sum>
    stack: ['$', '<statement_list>', 'SC', '<test_opt>', '<sum>']


    Pass: 8
    x: <sum>	token: num
    1 <sum_opt>
    0 <term>
    stack: ['$', '<statement_list>', 'SC', '<test_opt>', '<sum_opt>', '<term>']


    Pass: 9
    x: <term>	token: num
    0 num
    stack: ['$', '<statement_list>', 'SC', '<test_opt>', '<sum_opt>', 'num']


    Pass: 10
    x: num	token: num
    stack: ['$', '<statement_list>', 'SC', '<test_opt>', '<sum_opt>']


    Pass: 11
    x: <sum_opt>	token: SC
    stack: ['$', '<statement_list>', 'SC', '<test_opt>']


    Pass: 12
    x: <test_opt>	token: SC
    stack: ['$', '<statement_list>', 'SC']


    Pass: 13
    x: SC	token: SC
    stack: ['$', '<statement_list>']


    Pass: 14
    x: <statement_list>	token: id
    2 <statement_list>
    1 SC
    0 <statement>
    stack: ['$', '<statement_list>', 'SC', '<statement>']


    Pass: 15
    x: <statement>	token: id
    2 <expr>
    1 ASGN
    0 id
    stack: ['$', '<statement_list>', 'SC', '<expr>', 'ASGN', 'id']


    Pass: 16
    x: id	token: id
    stack: ['$', '<statement_list>', 'SC', '<expr>', 'ASGN']


    Pass: 17
    x: ASGN	token: ASGN
    stack: ['$', '<statement_list>', 'SC', '<expr>']


    Pass: 18
    x: <expr>	token: num
    0 <test>
    stack: ['$', '<statement_list>', 'SC', '<test>']


    Pass: 19
    x: <test>	token: num
    1 <test_opt>
    0 <sum>
    stack: ['$', '<statement_list>', 'SC', '<test_opt>', '<sum>']


    Pass: 20
    x: <sum>	token: num
    1 <sum_opt>
    0 <term>
    stack: ['$', '<statement_list>', 'SC', '<test_opt>', '<sum_opt>', '<term>']


    Pass: 21
    x: <term>	token: num
    0 num
    stack: ['$', '<statement_list>', 'SC', '<test_opt>', '<sum_opt>', 'num']


    Pass: 22
    x: num	token: num
    stack: ['$', '<statement_list>', 'SC', '<test_opt>', '<sum_opt>']


    Pass: 23
    x: <sum_opt>	token: SC
    stack: ['$', '<statement_list>', 'SC', '<test_opt>']


    Pass: 24
    x: <test_opt>	token: SC
    stack: ['$', '<statement_list>', 'SC']


    Pass: 25
    x: SC	token: SC
    stack: ['$', '<statement_list>']


    Pass: 26
    x: <statement_list>	token: IF
    2 <statement_list>
    1 SC
    0 <statement>
    stack: ['$', '<statement_list>', 'SC', '<statement>']


    Pass: 27
    x: <statement>	token: IF
    2 <statement>
    1 <paren_expr>
    0 IF
    stack: ['$', '<statement_list>', 'SC', '<statement>', '<paren_expr>', 'IF']


    Pass: 28
    x: IF	token: IF
    stack: ['$', '<statement_list>', 'SC', '<statement>', '<paren_expr>']


    Pass: 29
    x: <paren_expr>	token: LP
    2 RP
    1 <expr>
    0 LP
    stack: ['$', '<statement_list>', 'SC', '<statement>', 'RP', '<expr>', 'LP']


    Pass: 30
    x: LP	token: LP
    stack: ['$', '<statement_list>', 'SC', '<statement>', 'RP', '<expr>']


    Pass: 31
    x: <expr>	token: id
    0 <test>
    stack: ['$', '<statement_list>', 'SC', '<statement>', 'RP', '<test>']


    Pass: 32
    x: <test>	token: id
    1 <test_opt>
    0 <sum>
    stack: ['$', '<statement_list>', 'SC', '<statement>', 'RP', '<test_opt>', '<sum>']


    Pass: 33
    x: <sum>	token: id
    1 <sum_opt>
    0 <term>
    stack: ['$', '<statement_list>', 'SC', '<statement>', 'RP', '<test_opt>', '<sum_opt>', '<term>']


    Pass: 34
    x: <term>	token: id
    0 id
    stack: ['$', '<statement_list>', 'SC', '<statement>', 'RP', '<test_opt>', '<sum_opt>', 'id']


    Pass: 35
    x: id	token: id
    stack: ['$', '<statement_list>', 'SC', '<statement>', 'RP', '<test_opt>', '<sum_opt>']


    Pass: 36
    x: <sum_opt>	token: COMPARE
    stack: ['$', '<statement_list>', 'SC', '<statement>', 'RP', '<test_opt>']


    Pass: 37
    x: <test_opt>	token: COMPARE
    1 <sum>
    0 COMPARE
    stack: ['$', '<statement_list>', 'SC', '<statement>', 'RP', '<sum>', 'COMPARE']


    Pass: 38
    x: COMPARE	token: COMPARE
    stack: ['$', '<statement_list>', 'SC', '<statement>', 'RP', '<sum>']


    Pass: 39
    x: <sum>	token: id
    1 <sum_opt>
    0 <term>
    stack: ['$', '<statement_list>', 'SC', '<statement>', 'RP', '<sum_opt>', '<term>']


    Pass: 40
    x: <term>	token: id
    0 id
    stack: ['$', '<statement_list>', 'SC', '<statement>', 'RP', '<sum_opt>', 'id']


    Pass: 41
    x: id	token: id
    stack: ['$', '<statement_list>', 'SC', '<statement>', 'RP', '<sum_opt>']


    Pass: 42
    x: <sum_opt>	token: RP
    stack: ['$', '<statement_list>', 'SC', '<statement>', 'RP']


    Pass: 43
    x: RP	token: RP
    stack: ['$', '<statement_list>', 'SC', '<statement>']


    Pass: 44
    x: <statement>	token: WHILE
    2 <statement>
    1 <paren_expr>
    0 WHILE
    stack: ['$', '<statement_list>', 'SC', '<statement>', '<paren_expr>', 'WHILE']


    Pass: 45
    x: WHILE	token: WHILE
    stack: ['$', '<statement_list>', 'SC', '<statement>', '<paren_expr>']


    Pass: 46
    x: <paren_expr>	token: LP
    2 RP
    1 <expr>
    0 LP
    stack: ['$', '<statement_list>', 'SC', '<statement>', 'RP', '<expr>', 'LP']


    Pass: 47
    x: LP	token: LP
    stack: ['$', '<statement_list>', 'SC', '<statement>', 'RP', '<expr>']


    Pass: 48
    x: <expr>	token: id
    0 <test>
    stack: ['$', '<statement_list>', 'SC', '<statement>', 'RP', '<test>']


    Pass: 49
    x: <test>	token: id
    1 <test_opt>
    0 <sum>
    stack: ['$', '<statement_list>', 'SC', '<statement>', 'RP', '<test_opt>', '<sum>']


    Pass: 50
    x: <sum>	token: id
    1 <sum_opt>
    0 <term>
    stack: ['$', '<statement_list>', 'SC', '<statement>', 'RP', '<test_opt>', '<sum_opt>', '<term>']


    Pass: 51
    x: <term>	token: id
    0 id
    stack: ['$', '<statement_list>', 'SC', '<statement>', 'RP', '<test_opt>', '<sum_opt>', 'id']


    Pass: 52
    x: id	token: id
    stack: ['$', '<statement_list>', 'SC', '<statement>', 'RP', '<test_opt>', '<sum_opt>']


    Pass: 53
    x: <sum_opt>	token: COMPARE
    stack: ['$', '<statement_list>', 'SC', '<statement>', 'RP', '<test_opt>']


    Pass: 54
    x: <test_opt>	token: COMPARE
    1 <sum>
    0 COMPARE
    stack: ['$', '<statement_list>', 'SC', '<statement>', 'RP', '<sum>', 'COMPARE']


    Pass: 55
    x: COMPARE	token: COMPARE
    stack: ['$', '<statement_list>', 'SC', '<statement>', 'RP', '<sum>']


    Pass: 56
    x: <sum>	token: id
    1 <sum_opt>
    0 <term>
    stack: ['$', '<statement_list>', 'SC', '<statement>', 'RP', '<sum_opt>', '<term>']


    Pass: 57
    x: <term>	token: id
    0 id
    stack: ['$', '<statement_list>', 'SC', '<statement>', 'RP', '<sum_opt>', 'id']


    Pass: 58
    x: id	token: id
    stack: ['$', '<statement_list>', 'SC', '<statement>', 'RP', '<sum_opt>']


    Pass: 59
    x: <sum_opt>	token: RP
    stack: ['$', '<statement_list>', 'SC', '<statement>', 'RP']


    Pass: 60
    x: RP	token: RP
    stack: ['$', '<statement_list>', 'SC', '<statement>']


    Pass: 61
    x: <statement>	token: id
    2 <expr>
    1 ASGN
    0 id
    stack: ['$', '<statement_list>', 'SC', '<expr>', 'ASGN', 'id']


    Pass: 62
    x: id	token: id
    stack: ['$', '<statement_list>', 'SC', '<expr>', 'ASGN']


    Pass: 63
    x: ASGN	token: ASGN
    stack: ['$', '<statement_list>', 'SC', '<expr>']


    Pass: 64
    x: <expr>	token: id
    0 <test>
    stack: ['$', '<statement_list>', 'SC', '<test>']


    Pass: 65
    x: <test>	token: id
    1 <test_opt>
    0 <sum>
    stack: ['$', '<statement_list>', 'SC', '<test_opt>', '<sum>']


    Pass: 66
    x: <sum>	token: id
    1 <sum_opt>
    0 <term>
    stack: ['$', '<statement_list>', 'SC', '<test_opt>', '<sum_opt>', '<term>']


    Pass: 67
    x: <term>	token: id
    0 id
    stack: ['$', '<statement_list>', 'SC', '<test_opt>', '<sum_opt>', 'id']


    Pass: 68
    x: id	token: id
    stack: ['$', '<statement_list>', 'SC', '<test_opt>', '<sum_opt>']


    Pass: 69
    x: <sum_opt>	token: ADD
    2 <sum_opt>
    1 <term>
    0 ADD
    stack: ['$', '<statement_list>', 'SC', '<test_opt>', '<sum_opt>', '<term>', 'ADD']


    Pass: 70
    x: ADD	token: ADD
    stack: ['$', '<statement_list>', 'SC', '<test_opt>', '<sum_opt>', '<term>']


    Pass: 71
    x: <term>	token: num
    0 num
    stack: ['$', '<statement_list>', 'SC', '<test_opt>', '<sum_opt>', 'num']


    Pass: 72
    x: num	token: num
    stack: ['$', '<statement_list>', 'SC', '<test_opt>', '<sum_opt>']


    Pass: 73
    x: <sum_opt>	token: SC
    stack: ['$', '<statement_list>', 'SC', '<test_opt>']


    Pass: 74
    x: <test_opt>	token: SC
    stack: ['$', '<statement_list>', 'SC']


    Pass: 75
    x: SC	token: SC
    stack: ['$', '<statement_list>']


    Pass: 76
    x: <statement_list>	token: $
    stack: ['$']


    Parse tree tokens:
    ['<program>', '<statement_list>', '<statement>', 'id', 'ASGN', '<expr>', '<test>', '<sum>', '<term>', 'num', '<sum_opt>', '<test_opt>', 'SC', '<statement_list>', '<statement>', 'id', 'ASGN', '<expr>', '<test>', '<sum>', '<term>', 'num', '<sum_opt>', '<test_opt>', 'SC', '<statement_list>', '<statement>', 'IF', '<paren_expr>', 'LP', '<expr>', '<test>', '<sum>', '<term>', 'id', '<sum_opt>', '<test_opt>', 'COMPARE', '<sum>', '<term>', 'id', '<sum_opt>', 'RP', '<statement>', 'WHILE', '<paren_expr>', 'LP', '<expr>', '<test>', '<sum>', '<term>', 'id', '<sum_opt>', '<test_opt>', 'COMPARE', '<sum>', '<term>', 'id', '<sum_opt>', 'RP', '<statement>', 'id', 'ASGN', '<expr>', '<test>', '<sum>', '<term>', 'id', '<sum_opt>', 'ADD', '<term>', 'num', '<sum_opt>', '<test_opt>', 'SC', '<statement_list>']

    PARSER MESSAGE:
    --Parse tree tokens printed to the file 'parse_tree.txt'.



 
 



