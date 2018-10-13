class ParsedFile:
    def __init__(self):
        self.symbol_table = dict(SP=0,
                   LCL=1,
                   ARG=2,
                   THIS=3,
                   THAT=4,
                   SCREEN=16384,
                   KBD=24576)
        for i in range(0,16):
            k = 'R'+str(i)
            self.symbol_table[k]=i
        self.next_address = 16
        self.instruction_list = []
    
    def __len__(self):
        return len(self.instruction_list)
    
    def symbol(self,symbol,address=self.next_address):
        if not symbol in self.symbol_table:
            self.symbol_table[symbol] = address
        else: return self.symbol_table[symbol]
    
    def append(self,line):
        if line != "":
            self.instruction_list.append(line)
        
def ParseLine(line,parsed_file):
    line=line.strip()
    CommentIndex = line.find('//')          #find and remove comments
    if CommentIndex == 0:       
        return ""
    if CommentIndex > 0:
        line=line[0:CommentIndex].strip()
    if line[0] == '(':                      #add loop symbols to hash table
        k = line[1:len(line)-1]
        parsed_file.symbol(k,len(parsed_file))
        return ""
    if line[0] == '@':                      #replace symbols with address
        k = line[1:len(line)]
        if not k.isnumeric():
            parsed_file.symbol(k)
            return '@' + str(SymbolTable[k])
    return line