import re

class DecafTokenizer:
    def __init__(self):
        #Define Rules for REGEX
        self.Keywords = "^void$|int|^double$|^bool$|^string$|^null$|^for$|^while$|^if$|^else$|^return$|^break$|Print|^ReadInteger$|^ReadLine$|^true$|^false$"
        self.Operators = "\++|\-|\*|/|%|<=|>=|[||]{2}|[==]{2}|=|[&&]{2}"
        self.Int = '[0-9]+'
        self.Int_Hex = '0[xX][0-9A-Fa-f]+'
        self.Float = '[0-9]+\.[0-9]*'
        self.Float_eE = '[+-]?[0-9]+(?:\.[0-9]+)?\.?[eE][-+]?\d+?$'
        self.Special_Char = "[\[@&~!#$\^\{}\]:;<>?,\.']|\(|\)|{}|\[\]|;|:|\.|\`"
        self.Identifiers = "[a-zA-Z_]+[a-zA-Z0-9_]*"
        self.String = "\"(.*?)\""

    def tokenize(self,line):
        """
        Function to extract tokens per line of code inputed.

        Returns list of tokens organized based on the index.
        """
        #Defining Lists for identifying tokens
        self.tokens ,StringTokens,KeywordTokens,IntTokens,FloatTokens,OperatorTokens,IdentifierTokens,SpecialCharTokens = [],[],[],[],[],[],[],[]
        #Lists for before and after tokens
        disordered_Tokens, Ordered_Tokens = [],[]
        #Compile REGEX rules
        self.paterString = re.compile(self.String)
        self.paternKeywords = re.compile(self.Keywords)
        self.paternIdentifiers = re.compile(self.Identifiers)
        self.paternOperators = re.compile(self.Operators)
        self.paterFloat = re.compile(self.Float)
        self.paterFloat_eE = re.compile(self.Float_eE)
        self.paternInt = re.compile(self.Int)
        self.paternInt_Hex = re.compile(self.Int_Hex)
        self.paternSpecialChar = re.compile(self.Special_Char)

        #create new variable that holds inputted line
        self.line = line

        #Check if strings present in line
        if self.paterString.search(self.line):
            StringTokens = [tk for tk in re.findall(self.paterString,self.line)]
            for tk in StringTokens:
                self.tokens.append("\"{}\"".format(tk))

        #Check if keywords present in line
        if self.paternKeywords.search(self.line):
            KeywordTokens = [tk for tk in re.findall(self.paternKeywords,self.line)]                
            for tk in KeywordTokens: self.tokens.append(tk)
        
        # Check if string is not properly defined
        elif line.startswith("\"") and not line.endswith("\""):
                self.tokens.append(line)

        #Check if floats present in line
        elif self.paterFloat.search(self.line) or self.paterFloat_eE.search(self.line):
                #Check if line has float with exponent
                if self.paterFloat_eE.search(self.line):
                    Float_eE_Tokens = [tk for tk in re.findall(self.paterFloat_eE,self.line)]
                    for tk in Float_eE_Tokens:             
                        self.line = self.line.replace(tk,'')
                        self.tokens.append(tk)
                else:
                    #Check if line has regular floats
                    FloatTokens = [tk for tk in re.findall(self.paterFloat,self.line)]
                    for tk in FloatTokens:
                        #Check token starts with "." if so, remove and ignore
                        if tk.startswith('.'):
                            tk = tk[1:]
                        try:
                            #Remove token so that it does not repeat in another class
                            self.line = self.line.replace(tk,'')
                            int_check = float(tk)
                        except:
                            int_check = None

                        if int_check is not None:
                            #Check if float actually has "." in between digits, if not consider as int
                            if "." in tk:
                                self.tokens.append(tk)
                            else:
                                pass
                        else:
                            pass
            
        #If not float then check if line has an Integer or Hex Integer
        elif (self.paternInt.search(self.line) or self.paternInt_Hex.search(self.line)):
            IntTokens = [tk for tk in re.findall(self.paternInt,self.line)]
            for tk in IntTokens:
                self.tokens.append(tk)

        #Check if line has an Identifier
        if self.paternIdentifiers.search(self.line) and not self.paterString.search(self.line) :
            IdentifierTokens = [tk for tk in re.findall(self.paternIdentifiers,self.line)]
            for tk in IdentifierTokens:
                #Clean line so that tokens do not repeat in other classes
                self.line = self.line.replace(tk,'')
                if tk in KeywordTokens: pass 
                else: self.tokens.append(tk)

        #Check if line has an Operator
        if self.paternOperators.search(self.line):
            OperatorTokens = [tk for tk in re.findall(self.paternOperators,self.line)]
            for tk in OperatorTokens:
                self.line = self.line.replace(tk,'')
                self.tokens.append(tk)

        #Check if line has a Special Character
        if self.paternSpecialChar.search(self.line):  
            SpecialCharTokens = [tk for tk in re.findall(self.paternSpecialChar,self.line)]
            for tk in SpecialCharTokens: self.tokens.append(tk)
        
        #Check if line ends with '"', if so append the whole line to check error
        if line.endswith("\""):
            self.tokens.append("\"")

        if self.tokens:
            ocur_count = 0
            for token in self.tokens:

                if (self.paterString.search(token) or self.paternKeywords.search(token) or 
                    self.paternSpecialChar.search(token) or self.paternInt.search(token) or self.paterFloat.search(token)): #Get more than one ocurrance
                    #Get the index location of every occurrence of a token
                    try:
                        m = [match.start() for match in re.finditer(token, line)]

                    except:
                        m = [match.start() for match in re.finditer("\{}".format(token), line)]
                        #print(m)

                    #If more than one occurrence get the first index and increment count occurrences
                    if len(m)>1 and ocur_count == 0:
                        m = m[0]
                        ocur_count+=1
                    #If more than one occurrence and already counted one occurrence get next occurrence index and increment count
                    elif len(m)>1 and ocur_count > 0:
                        try:
                            m = m[ocur_count]
                            ocur_count+= 1
                        except:
                            ocur_count = 0
                            m = m[ocur_count]
                            ocur_count +=1
                    else:
                        #If just one occurrence get that index occurrence
                        m = m[0]
                    disordered_Tokens.append((token,m))
                else:
                    m = line.find(token)
                    disordered_Tokens.append((token,m))

            #Sort tokens based on index location on line
            # print(disordered_Tokens)
            Sorted_Tokens = sorted(disordered_Tokens, key=lambda item:item[1])
            for tk in Sorted_Tokens:
                Ordered_Tokens.append(tk[0]) #Get the tokens without index into a list and return
            #print(Ordered_Tokens)
            return Ordered_Tokens

    def get_RegEx(self):
        """
        Function for geting REGEX rules

        Returns 7 strings, each contains a rule for REGEX to find
        """
        Keywords = self.Keywords
        Operators = self.Operators
        #Numerals = self.Numerals
        Int = self.Int
        Float = self.Float
        Special_Characters = self.Special_Char
        Identifiers = self.Identifiers
        String = self.String
        return Keywords,Operators,Int,Float,Special_Characters,Identifiers, String

    def get_dictionaries(self):
        """
        Function for getting dictionaries that hold token - value comparison

        Returns 5 Dictionaries
        """
        operators = {'=': "'='",'+' : "'+'",  '-':"'-'", '*':"'*'",  '/':"'/'", '%':"'%'", '<=':'T_LessEqual', '>=':'T_GreaterEqual','==':'T_Equal', '||':'T_Or', '&&':'T_And'}
        operators_key = operators.keys()

        data_type = {'void':'T_Void', 'int' : 'T_Int', 'double': 'T_Double', 'string':'T_String'}
        data_type_key = data_type.keys()

        punctuation = {';':"';'", ',':"','", '.':"'.'", '(':"'('", ')':"')'", '{':"'{'", '}':"'}'", '!':"'!'",'<':"'<'",'>':"'>'"}
        punctuation_key = punctuation.keys()

        keyword = {'while':'T_While', 'if':'T_If', 'else':'T_Else', 'return':'T_Return', 'break':'T_Break', 'true':'T_BoolConstant (value = true)', 
                   'false':'T_BoolConstant (value = false)','void':'T_Void', 'int' : 'T_Int', 'double': 'T_Double', 'string':'T_String',
                   'bool':'T_Bool','null':'T_Null','for':'T_For','Print':'T_Print','ReadInteger':'T_ReadInteger','ReadLine':'T_ReadLine'}
        keyword_key = keyword.keys()


        empty = {'':''}
        empty_key = empty.keys()

        return operators, data_type, punctuation, keyword, empty

    def remove_Comments(self,program):
        """
        Function to remove comments from the whole input code.

        returns single string with the whole code without the commented items based on decaf rules
        """
        program_Multi_Comments_Removed = re.sub("/\*[^*]*\*+(?:[^/*][^*]*\*+)*/", "", program)
        program_Single_Comments_Removed = re.sub("//.*", "", program_Multi_Comments_Removed)
        program_Comments_removed = program_Single_Comments_Removed
        return program_Comments_removed
