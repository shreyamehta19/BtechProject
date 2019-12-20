# BtechProject
Code Summarizer

code.py tries to summarize the code using the lexical structure of the code.
The code has two main classes:

1)TokenGenerator : Which takes UAST file of the code as the input. Generates token and classifies them into methods using stack datastructure. The output is as:
    i) The summarization at the method level
    ii)Tokens stored in "Token" file
    iii)All the variables that are members of the class with "ClassDeclarations"
    iv)All the variables within method written in "MethodDeclarations"

2)Token Prioritizer(To be pushed) : This method gives weights to the tokens of the method. Weights are considered on the position of the occurence of the token and the frequency.    
    
