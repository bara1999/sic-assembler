from pass_one import optab,LOCCTR,start1,sym,proglen,error


objpgm = open("ObjectProgram.obj","w")
errorFile= open("errorFile.txt","w")
listing = open("listing.lst","w")	
inter = open("Intermediatefile.mdt","r")
symtab = open("SymbolTab.txt","r")
l = []

addrlist = []
for i in inter.readlines():

    ls= i
    dep=ls[:-1]
    if len(dep)<50:
        for i in range(50-len(dep)):
         dep = dep+" "
   
    opcode= ls[20:29].strip()
    
    address = ls[0:5].strip()
    
    if opcode != "START" :
            addrlist.append(address)
            
    label = ls[10:19].strip()
    
    operand = ls[30:39].strip()
    if operand[-2:] == ",X":
        operand = operand[:-2]
        sym[operand]=str(hex(int(sym[operand],16)+int('8000',16)))[2:]
       
    if opcode=="START":
        listing.write(ls)

        
        objpgm.write("H^"+label+"^00"+start1+"^00"+proglen.upper())
    elif opcode=="END":
        l.append("")
        
        listing.write(ls)

        tempstr = "\nE^00"+start1
        
    else:
        if opcode in optab.keys():
            op = optab[opcode]
            
        
            if opcode=="RSUB":
                op +="0000"
            
            elif operand in sym.keys():
                op += sym[operand]
           
                
            l.append(op)
            
            listing.write(dep+op+'\n')
        elif opcode=="WORD":
            op = hex(int(operand))
            op1 = str(op)
            op1 = op1[2:]
            if len(op1)<6:
                for i in range(6-len(op1)):
                    op1 = "0"+op1
            
            l.append(op1)
            listing.write(dep+op1+'\n')

                 
        
        elif opcode =="BYTE"  :
            temp = operand[2:len(operand)-1] 
            if operand[0]=="C":
               
                f=""
                for i in temp:
                    hexcode = hex(ord(i))
                    tmp = str(hexcode)
                    f +=tmp[2:]
                l.append(f)
                listing.write(dep+f+'\n')
                
                
            elif operand[0]=="X":
                l.append(temp)
                listing.write(dep+temp+'\n')

        elif label=="*"  :
            
            temp = opcode[3:len(opcode)-1]
            
            if opcode[1]=="C":
                
                f=""
                for i in temp:
                    hexcode = hex(ord(i))
                    tmp = str(hexcode)
                    f+=tmp[2:]
                l.append(f)
                listing.write(dep+f+'\n')
            elif opcode[1]=="X":
                
                l.append(temp)
                listing.write(dep+temp+"\n")
                
        
        

        else:
            l.append("")
            listing.write(ls)
i = 0

while i<len(l):
    
	addr = addrlist[i]
	cont = 0
	if l[i]!="":
		objpgm.write("\nT^00"+addr.upper()+"^")        
		tell = objpgm.tell()
		objpgm.write("  ")
		j=i
		while i<len(l) and l[i]!="" and cont<10 : 
			objpgm.write("^" + l[i].upper())
			cont +=1
			i+=1
		i=i-1	
		objpgm.seek(tell)
		tempaddr = str(int(addrlist[i],16)-int(addr,16) + int(3))
		tempaddr1=hex(int(tempaddr))
		taddr = tempaddr1[2:4]
		if len(l[i])<=6:
			s=int((len(l[i]))/2)
			taddr=str(s)
		if len(taddr) == 1:
			taddr= "0"+taddr
		

		objpgm.write(taddr.upper())  
		objpgm.seek(0,2)
		
		
	i+=1

objpgm.write(tempstr)

for i in error:
    print(i)
    errorFile.write(i+'\n')

errorFile.close()
objpgm.close()
inter.close()
symtab.close()

		
					
        
                    
                    
                    
    

            
    
    



        
        
            
            
            
            
