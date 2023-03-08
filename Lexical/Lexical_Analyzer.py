#Programming Languages and Compilers
#Project 1, Phase I, Lexical Analyzer 
#By Eulises Franco - 02/16/2023
####- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -####

#Import required libraries
import sys
import re
from utils import DecafTokenizer
import numpy as np
####- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -####

#Define Main Class
class Lex_Analyzer:
    #Lex_Analyzer class holds the required script for propperly tokenizing an input file.
    #When class is called, path to file needs to be specified
    def __init__(self, file_path):
        file_path = file_path
        out_tokens = [] #Token, Type, Location
        #Create an instance of the tokenizer extracted from utils.py
        tokenizer = DecafTokenizer() 
        
        #Open and read inputed file
        file = open(file_path)
        read_file = file.read() 

        #Extract Regex rules from utils.py
        Keywords,Operators,Int,Float,Special_Characters,Identifiers, String = tokenizer.get_RegEx()

        #Extract Dictionary rules from utils.py
        operators_key, data_type_key, punctuation_key, keyword_key, empty_key = tokenizer.get_dictionaries()

        #Initialize line counting
        line_count = 0

        #Initialize token count
        ocur_count = 0

        #Remove comments based on "Decaf" rules
        no_comments_read_file = tokenizer.remove_Comments(read_file)

        #Dividing string into lines
        program = no_comments_read_file.split("\n")
        
        #Loop through lines
        for line in program:
            line_count += 1 #Add count to line
            tokens = tokenizer.tokenize(line) #Call tokenizer class from utils.py
            if tokens is not None: #Make sure there where tokens detected

                #Loop through each token detected
                for token in tokens:
                    #Boolean objects to avoid double detection
                    float_token = False
                    kewrd_token = False
                    #Ignore empty token
                    if token == '':
                        pass
                    
                    #Check error in string not closed
                    if token =="\"":
                        print('\n*** Error line {}.\n*** Unterminated string constant: \"\n'.format(line_count))

                    #Check error in string not opened but closed
                    if token.startswith("\"") and not token.endswith("\""):
                        print('\n*** Error line {}.\n*** Unterminated string constant: {}\n'.format(line_count,token))
                        break
                    
                    #Check if token is a decaf string and  ignore any other possible token while token it's a string
                    if re.search(String,token):
                        #Check if token repeates multiple times in line
                        m = [match.start() for match in re.finditer(token, line)]
                        if len(m)>1 and ocur_count == 0:
                            m = m[0]
                            ocur_count+=1
                        elif len(m)>1 and ocur_count > 0:
                            m = m[ocur_count]
                        else:
                            m = m[0]
                        col_start = m
                        col_end = m+len(token)
                        #print(token, (11-len(token))*" ", "line", line_count, 'cols', str(col_start+1)+'-'+ str(col_end), 'is T_StringConstant (value = {})'.format(token))
                        out_tokens.append([token,'T_StringConstant',line_count])#Token, Type, Location

                    else:
                        #Search for decaf Keywords
                        if re.search(Keywords,token) :
                            col_start = line.find(token)
                            col_end = col_start+len(token)
                            #print(token, (11-len(token))*" ", "line", line_count, 'cols', str(col_start+1)+'-'+ str(col_end),'is', keyword_key[token])
                            kewrd_token = True
                            out_tokens.append([token,keyword_key[token],line_count])#Token, Type, Location


                        #Search for decaf Identifiers
                        elif re.search(Identifiers,token) and not kewrd_token or re.search(Identifiers,token):
                            col_start = line.find(token) #Get token starting column
                            col_end = col_start+len(token) #Get token ending column
                            iden_col_start = col_start
                            iden_col_end = col_end
                            #Check if token was misplaced as identifier when it is a float
                            if re.search(Float,token):
                                pass
                            else:
                                #Make sure token is the permitted decaf length
                                if len(token) > 31:
                                    # print('\n*** Error line {}.'.format(line_count), '\n*** Identifier too long: \"{}\"\n'.format((token)))
                                    trunc_token = token[0:31]
    
                                    #print(token, (11-len(token))*" ", "line", line_count, 'cols', str(col_start+1)+'-'+ str(col_end), 'is T_Identifier (truncated to {})'.format(trunc_token))
                                    out_tokens.append([token,"T_Identifier",line_count])#Token, Type, Location

                                else:
                                    #print(token, (11-len(token))*" ", "line", line_count, 'cols', str(col_start+1)+'-'+ str(col_end), 'is T_Identifier')
                                    out_tokens.append([token,"T_Identifier",line_count])#Token, Type, Location

                        
                        #Check if token is a float
                        if re.search(Float,token):
                            #Check token has a "." if not assume it is an decaf integer
                            if "." in token:
                                col_start = line.find(token)
                                col_end = col_start+len(token)

                                if 'E' in token or 'e' in token:
                                    #print(token, (11-len(token))*" ", "line", line_count, 'cols', str(col_start+1)+'-'+ str(col_end), 'is T_DoubleConstant (value = ','%.0f'%float(token)+")")
                                    out_tokens.append([str('%.0f'%float(token)),"T_DoubleConstant",line_count])#Token, Type, Location

                                else:
                                    #print(token, (11-len(token))*" ", "line", line_count, 'cols', str(col_start+1)+'-'+ str(col_end), 'is T_DoubleConstant (value = {})'.format(float(token)))
                                    out_tokens.append([token,"T_DoubleConstant",line_count])#Token, Type, Location

                                float_token = True
                            else:
                                pass
                        #If it is not a float then it is an integer
                        elif re.search(Int,token):
                            #print(token, line)
                            col_start = line.find(token)
                            col_end = col_start+len(token)
                            if token != line: #Check token is not equal to the whole line
                                try:
                                    if iden_col_start <= col_start <= iden_col_end: #Make sure token is not part of another token
                                        pass
                                    else:
                                        #Remove "+" or "-" signs before integer
                                        if "+" in token or "-" in token:
                                            token = token[1:]
                                            #print(token, (11-len(token))*" ", "line", line_count, 'cols', str(col_start+1)+'-'+ str(col_end), 'is T_IntConstant (value = {})'.format(int(token)))
                                            out_tokens.append([token,"T_IntConstant",line_count])#Token, Type, Location
                                        else:
                                            #print(token, (11-len(token))*" ", "line", line_count, 'cols', str(col_start+1)+'-'+ str(col_end), 'is T_IntConstant (value = {})'.format(int(token)))
                                            out_tokens.append([token,"T_IntConstant",line_count])#Token, Type, Location

                                except:
                                    if "+" in token or "-" in token:
                                            token = token[1:]
                                            #print(token, (11-len(token))*" ", "line", line_count, 'cols', str(col_start+1)+'-'+ str(col_end), 'is T_IntConstant (value = {})'.format(int(token)))
                                            out_tokens.append([token,"T_IntConstant",line_count])#Token, Type, Location

                                    else:
                                        #print(token, (11-len(token))*" ", "line", line_count, 'cols', str(col_start+1)+'-'+ str(col_end), 'is T_IntConstant (value = {})'.format(int(token)))
                                        out_tokens.append([token,"T_IntConstant",line_count])#Token, Type, Location


                            else:
                                try:
                                    #print(token, (11-len(token))*" ", "line", line_count, 'cols', str(col_start+1)+'-'+ str(col_end), 'is T_IntConstant (value = {})'.format(int(token)))
                                    out_tokens.append([token,"T_IntConstant",line_count])#Token, Type, Location

                                except:
                                    pass

                        #Check if token is a decaf Operator
                        elif re.search(Operators,token)  and not float_token:
                            col_start = line.find(token)
                            col_end = col_start+len(token)
                            #print(token, (11-len(token))*" ", "line", line_count, 'cols', str(col_start+1)+'-'+ str(col_end),'is',operators_key[token])
                            out_tokens.append([token,operators_key[token],line_count])#Token, Type, Location


                        #Check if token is a decaf Special Character
                        elif re.search(Special_Characters, token):
                            col_start = line.find(token)
                            col_end = col_start+len(token)
                            try:
                                #print(token, (11-len(token))*" ", "line", line_count, 'cols', str(col_start+1)+'-'+ str(col_end),'is', punctuation_key[token])
                                out_tokens.append([token,punctuation_key[token],line_count])#Token, Type, Location

                            except:
                                print('\n*** Error line {}.'.format(line_count), '\n*** Unrecognized char: \'{}\'\n'.format((token)))

                        else:
                            pass
        
        out_tokens = np.array(out_tokens)
        save_file = open("arr","wb")
        np.save(save_file, out_tokens)
        save_file.close

Lex_Analyzer(sys.argv[1])