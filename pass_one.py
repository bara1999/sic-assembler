from tkinter import *
#Opening SIC program
inp = open("SIC_input.asm","r")
#For output of PASS ONE
out = open("Intermediatefile.mdt","w")
#SYMBOLTAB
symtab = open("SymbolTab.txt","w");
sym = {}
error=[]
littab = {}



optab = {
    "ADD":"18",
    "AND":"40",
    "COMP":"28",
    "DIV":"24",
    "J":"3C",
    "JEQ":"30",
    "JGT":"34",
    "JLT":"38",
    "JSUB":"48",
    "LDA":"00",
    "LDCH":"50",
    "LDL":"08",
    "LDX":"04",
    "MUL":"20",
    "OR":"44",
    "RD":"D8",
    "RSUB":"4C",
    "STA":"0C",
    "STCH":"54",
    "STL":"14",
    "STSW":"E8",
    "STX":"10",
    "SUB":"1C",
    "TD":"E0",
    "TIX":"2C",
    "WD":"DC"}
LOCCTR=0
#READING FIRST LINE
first = inp.readline()
if first[11:20].strip() == "START":
        LOCCTR =first[21:38].strip()
        start1 = LOCCTR    
        start =int(LOCCTR,16)
        PN=first[0:10].strip()
        out.write(LOCCTR+" "*6+first[0:38])
else:
    LOCCTR=0

for i in inp.readlines():
   
    n = i
    string=n[40:70]#to remove comments
    if (n[11:20].strip()!='End'):
        if n[0]!='.':
            if len(string) == 0:

               out.write(LOCCTR+" "*6+n)
            else:
                out.write(LOCCTR+" "*6+n[0:38]+"\n")

            if n[0:10].strip()!="":
                if n[0:10].strip() in sym:

                    print("error:duplicate symbol : "+n[0:10].strip())
                    error.append("error:duplicate symbol : "+n[0:10].strip())
                    
                else:
                    space=18-len(n[0:10].strip())
                    symtab.write(n[0:10].strip()+" "*space+LOCCTR+"\n")
                    
                    sym[n[0:10].strip()] = LOCCTR
            
            if n[11:19].strip() in optab.keys() or n[11:19].strip()=="WORD":
              LOCCTR = str(hex(int(LOCCTR,16)+(3)))[2:]
            elif n[11:19].strip()=="RESW":
              temp = int(n[21:38].strip())
              LOCCTR = str(hex(int(LOCCTR,16)+(temp)*3))[2:]
            elif n[11:19].strip()=="RESB":
              LOCCTR = str(hex(int(LOCCTR,16)+int(n[21:38].strip())))[2:]
            elif n[11:19].strip()=="BYTE":
              if n[21:38].strip()[0]=="X":
                LOCCTR = str(hex(int(LOCCTR,16)+int((len(n[21:38].strip())-3)/2)))[2:]
              elif n[21:38].strip()[0]=="C":
                LOCCTR = str(hex(int(LOCCTR,16)+int((len(n[21:38].strip())-3))))[2:]
        
            elif n[11:19].strip()=="LTORG":
                for i in littab:
                    space=18-len(i)
                    out.write(LOCCTR+" "*6+"*"+" "*10+i+"\n")
                    symtab.write(i+" "*space+LOCCTR+"\n")
                    sym[i] = LOCCTR
                    
                    LOCCTR=str(hex(int(LOCCTR,16)+int(littab[i][0])))[2:]
                littab={} 
            elif n[11:19].strip()=="END":
                
                out.write('\n')
                if littab:
                     for i in littab:
                        space=18-len(i)
                        out.write(LOCCTR+" "*6+"*"+" "*10+i+"\n")
                        symtab.write(i+" "*space+LOCCTR+"\n")
                        sym[i] = LOCCTR
                    
                        LOCCTR=str(hex(int(LOCCTR,16)+int(littab[i][0])))[2:]
            else:
                print("error: invalid opcdce"+ n[11:19].strip())
                error.append("error:duplicate symbol : "+n[0:10].strip())
                break


            if n[21:22] == '=':
                literal = n[21:38].strip()
                if literal[1]== 'X':
                     hexco = literal[3:-1]
                     
                     if literal not in littab:
                        littab[literal]=[len(hexco)/2]
                elif  literal[1]=='C':
                     hexco = literal[3:-1]
                     
                     if literal not in littab:
                        littab[literal]=[len(hexco)]
                else:
                    print("ُERROR: NOT Valid Literal : "+literal) 
                    error.append("error:duplicate symbol : "+n[0:10].strip())
    
               
inp.close()
out.close()
symtab.close()

lastaddress=LOCCTR
programLength = int(lastaddress,16) - start
proglen = hex(int(programLength))[2:]

print("program name is : "+PN+"\n"+"pogram length: "+proglen+'\n')      
for i in sym:
    print(i+"  "+sym[i]+"\n")        
    
 


root =Tk()
root.title("Sic assembler") 
text1 = open("SymbolTab.txt").read()
prognam = Label(root ,text = "Program Name :" + PN,font=('arial',16))
prognam.pack(fill = BOTH)
blank= Label(root ,text = "")
blank.pack(fill = BOTH)
programLength = Label(root ,text = " Program Langth :" + str(proglen),font=('arial',16),bg='yellow' )
programLength.pack(fill = BOTH)
blank= Label(root ,text = "")
blank.pack(fill = BOTH)
programLength = Label(root ,text = " Location Counter :" + str(LOCCTR),font=('arial',16) )
programLength.pack(fill = BOTH)
blank= Label(root ,text = "")
blank.pack(fill = BOTH)
symTit = Label(root, text=" Symbol Table:",font=('arial',16),fg='red',bg='yellow')
symTit.pack(fill = BOTH)
sym1 = Label(root, text=text1,font=('arial',16))
sym1.pack(fill = BOTH)

root.mainloop()