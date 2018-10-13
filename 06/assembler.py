def InitSymbolTable():
    SymbolTable = dict(SP=0,
                   LCL=1,
                   ARG=2,
                   THIS=3,
                   THAT=4,
                   SCREEN=16384,
                   KBD=24576)
    for i in range(0,16):
        k = 'R'+str(i)
        SymbolTable[k]=i
    return SymbolTable

def ClearFile(file):
    newfile=[]
    for i in range(len(file)):
        line = file[i].strip()
        CommentIndex = line.find('//')  #find and remove comments
        if CommentIndex == 0:       
            line = ""
        if CommentIndex > 0:
            line=line[0:CommentIndex].strip()
        if line != "":
            newfile.append(line)            #collects all non-empty lines
    keys = InitSymbolTable()          #collects addresses for symbols
    nextaddress=16
    i=0
    while i < len(newfile):            #pop (Xxx), save index
        if newfile[i][0]=="(":
            k=newfile.pop(i).strip("()")
            keys[k]=i
        else:
            i+=1
    for i in range(len(newfile)):           #replace symbols with addresses,
        if newfile[i][0] == '@':            #assigning addresses as needed
            k = newfile[i].strip("@")
            if not k.isnumeric():
                if not k in keys.keys():
                    keys[k]=nextaddress
                    nextaddress += 1
                newfile[i] = '@' + str(keys[k])
    return newfile

def ParseLine(line,ParsedFile,SymbolTable,NextAddress):
    line=line.strip()
    if line == "":
        return ""
    CommentIndex = line.find('//')          #find and remove comments
    if CommentIndex == 0:       
        return ""
    if CommentIndex > 0:
        line=line[0:CommentIndex].strip()
    if line[0] == '(':                      #add loop symbols to hash table
        k = line[1:len(line)-1]
        SymbolTable[k]=len(ParsedFile)
        return ""
    if line[0] == '@':                      #replace symbols with address
        k = line[1:len(line)]
        if not k.isnumeric():
            if not k in SymbolTable:
                SymbolTable[k] = NextAddress
                NextAddress += 1
            return '@' + str(SymbolTable[k])
    return line
            
def ParseFile(file):
    SymbolTable = InitSymbolTable()
    NextAddress = 16
    ParsedFile = []
    for line in file:
        newline = ParseLine(line,ParsedFile,SymbolTable,NextAddress)
        if newline != "":
            ParsedFile.append(newline)
    return ParsedFile

def ConvertDest(dest):
    A = "0"
    D = "0"
    M = "0"
    if "A" in dest:
        A = "1"
    if "D" in dest:
        D = "1"
    if "M" in dest:
        M = "1"
    return A + D + M
    
def to_binary(num):
    n = bin(int(num))
    lead = 5 - len(n)
    return (str(0) * lead) + n[2:len(n)]

def to_16(num):
    n = to_binary(num)
    lead = 16 - len(n)
    return (str(0) * lead) + n
    
def InitJmpMnems():
    jmp_mnems = dict()
    mnems = ["null","JGT","JEQ","JGE","JLT","JNE","JLE","JMP"]
    for val in list(range(0,8)):
        jmp_mnems[mnems[val]] = to_binary(val)
    return jmp_mnems

jmp_mnems = InitJmpMnems()
    
def ConvertJump(jmp):
    return jmp_mnems[jmp]

def InitInstMnems():
    inst_mnems = dict()
    A=["0","1","-1","D","A","!D","!A","-D","-A","D+1","A+1","D-1","A-1","D+A","D-A","A-D","D&A","D|A"]
    M=['0', '1', '-1', 'D', 'M', '!D', '!M', '-D', '-M', 'D+1', 'M+1', 'D-1', 'M-1', 'D+M', 'D-M', 'M-D', 'D&M', 'D|M'] 
    instbits=["101010","111111","111010","001100","110000","001101","110001","001111","110011","011111","110111","001110","110010","000010","010011","000111","000000","010101"]
    abits=[]
    mbits=[]
    for i in instbits:
        abits.append("0"+i)
        mbits.append("1"+i)
    for i in range(len(abits)):
        inst_mnems[M[i]] = mbits[i]
    for i in range(len(abits)):
        inst_mnems[A[i]] = abits[i]
    return inst_mnems

inst_mnems=InitInstMnems()
    
def ConvertInst(inst):
    return inst_mnems[inst]

def ConvertLine(line):
    if line[0] == "@":
        return to_16(line[1:len(line)])
    if "=" in line:
        dest = line[0:line.find("=")]
        dest=ConvertDest(dest)
        line = line[line.find("=")+1:]
    else:
        dest = "000"
    if ";" in line:
        jmp = line[line.find(";")+1:len(line)]
        jmp = ConvertJump(jmp)
        line = line[:line.find(";")]
    else:
        jmp = "000"
    inst = ConvertInst(line)
    return "111" + inst + dest + jmp

def ConvertFile(file):
    parsed_file = ClearFile(file)
    converted_file = []
    for line in parsed_file:
        converted_file.append(ConvertLine(line))
    return converted_file