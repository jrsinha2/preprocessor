import re
f=open("input",'r')
r=f.read()
s=re.split('\n',r)		# s contains all the lines of the input file
namtab=[]		#used to store the name of the macros
symbols=["GE","NE","EQ","LT","GT","LE"]			#for conditions 
deftab=[]			#used to store the starting line no. of definitions and endling line no.
argtabk=[]		#used to store keyword arguments name
argtabkv=[]		#used to store the arguments value
argmap=[]			
argname=[]		#used to arguments names of all the macros
argtypec=[]		#used to store the count of the args of the macros 
define=0		#just flag variable
start=0			#start line of the macro def.
end=0			#end line of the macro def.
index=-1	#index of macro
checkarg=0	##just flag variable
expand=0	#just flag variable
line=-1		#line count
countmacro=0	#macro count
argcount=0	 
key=0	
name=0	#just flag variable
temp=0	
flag=0	#just flag variable
prototype=0	#just flag variable
startarg=0	
argsubs=0	
iftab=[]	#store the line nos. of the if part
elsetab=[]	#store the line nos. of the else part
ifindex=-1	
ifpart=-1				#just flag variable
elsepart=-1	#just flag variable
elsedone=0	#just flag variable
ifdone=0	#just flag variable
elseindex=-1
logic=""	
elseyes=0	#just flag variable	
ifyes=0	#just flag variable
lin=""
snamtab=[]		#used to store single line macro names
valuetab=[]		#single line macros values 
definesingle=0	#just flag variable
namesingle=0	#just flag variable
namindex=0	
#print(s)	
for l in s:				#l is line 
	i=0
	flag=0
	line+=1		#line incremented
	words=l.split()		#words contain allt he words of the line
	size=len(words)		
	#print(words)
	simple=1			#just flag variable
	for i in range(0,size):	
		if(words[i] in snamtab):						#check if the word is in snamtab(if it is single macro name) 	
			for j in range(len(snamtab)):
				if(words[i]==snamtab[j]):
					namindex=j				#if yes then which no/index
					break
			lin=l
			lin=lin.replace(words[i],valuetab[namindex])				#replace it with its corresponding value
			l=lin
		if(words[i] in namtab):								#check if the word is in namtab(if it is multi line macro name)
			simple=0
			checkarg=1			#next check its arguments
			for j in range(len(namtab)):
				if(words[i]==namtab[j]):		#if yes then which no/index
					index=j
					break
			#sprint(line)
			#print(words[i])
			
		elif(checkarg==1):			#arguments check mode on
			simple=0
			argcall=0
			for j in range(0,len(words[i])):
				if(words[i][j]=='%'):				#because keyword arguments start with % so checking....
					argtabk.append(words[i][j+1])
					
					argtabkv.append(words[i][j+3])
					key=1
					argcall+=1
				elif(words[i][j]!=',' and words[i][j-1]!='=' and words[i][j-1]!='%' and words[i][j]!='='):		#any left out 
					argtabkv.append(words[i][j])
					argcall+=1
			checkarg=0
			expand=1				#next is expansion
			
			#print(argtabk)
			#print(argtabkv)
			#print(argcall)
			argmap.append(argcall)
			#print(argmap)
			#print(line)
		#elif(expand==1):
			simple=0
			#print(line)
			start=deftab[index]			#gets the starting line no. of the definition from deftab
			end=deftab[len(deftab)-index-1]		#gets the ending line no. of the definition from deftab
			flag=0
			#print(start)
			#print(end)
			for j in range(start+1,end):
				if(s[j].find("STARTMACRO")==-1 and s[j].find("ENDMACRO")==-1 and s[j].find("//")==-1):			#dont write startmacro ,endmacro or comments line
					flag=0
					#print('en')
					lin=s[j]
					for k in range(0,len(argtabk)):
						char='%'+argtabk[k]
						if(lin.find(char)!=-1):
							lin=lin.replace(char,argtabkv[k])			#substitution of keyword arguments
							flag=1
							
					
					while(1):						#if arguments doesnt match the arguments called so...default value 0
						if(lin.find("%")!=-1):
							loc=lin.find("%")
							char="%"+lin[loc+1]
							if(char not in argname): 
								lin=lin.replace(char,'0')
								ws=lin.split()
								flag=1
							else:
								break
						else:
						
							break
					#print(flag)
					if(flag==1):
						ws=lin.split()
						#ifspot=0
						#print(ws)
						if(lin.find("if")!=-1):				# if it contains if condition
							#ifspot=1
							#print('en')
							for x in range(len(ws)):
								#print('ENterd')
								if(ws[x] in symbols):
									logic=ws[x]					#get its logic in condition
									break
							if(j!=iftab[ifindex] and ifindex>=0):
								ifindex+=1
							elif(ifindex==-1):
								ifindex+=1
							ifpart=0
							ifdone=0
							#loc=lin.find("if")
							#print("logic is",logic)
							#print((int)(ws[x-1]),(int)(ws[x+1]))
							if(logic=='GE' and ws[x-1][0]!='%' and ws[x+1][0]!='%'):			#matching its condition with its logic ..if yes then ifpart expansion
								if((int)(ws[x-1])>=(int)(ws[x+1])):													#if no else part expansion or no expansion depends on type of if
									ifpart=1
									#print('en')
							elif(logic=='LE' and ws[x-1][0]!='%' and ws[x+1][0]!='%'):
								if((int)(ws[x-1])<=(int)(ws[x+1])):
									ifpart=1
									#print('en')							
							elif(logic=='NE' and ws[x-1][0]!='%' and ws[x+1][0]!='%'):
								if((int)(ws[x-1])!=(int)(ws[x+1])):
									ifpart=1
									#print('en')
							elif(logic=='LT' and ws[x-1][0]!='%' and ws[x+1][0]!='%'):
								if((int)(ws[x-1])<(int)(ws[x+1])):
									ifpart=1
									#print('en')
							elif(logic=='GT' and ws[x-1][0]!='%' and ws[x+1][0]!='%'):
								if((int)(ws[x-1])>(int)(ws[x+1])):
									ifpart=1
									#print('en')
							elif(logic=='EQ' and ws[x-1][0]!='%' and ws[x+1][0]!='%'):
								if((int)(ws[x-1])==(int)(ws[x+1])):
									ifpart=1
									#print('en')
						elif(ifpart==1 and ifdone==0):					#if ifpart expansion yes then start from its starting line no. till ending line no.
							#print('Entered')
							if(j>iftab[ifindex] and j<iftab[len(iftab)-ifindex-1]):
								#print('entered2')
								print(lin)
							elif(j>iftab[len(iftab)-ifindex-1]):
								#print('en')
								ifdone=1
								ifpart=-1
						if(elsepart==1 and elsedone!=1):
						#print('en')
							if(j>elsetab[elseindex] and j<elsetab[len(elsetab)-elseindex-1]):
								print(lin)
							elif(j>elsetab[len(elsetab)-elseindex-1]):
								elsedone=1
								elsepart=-1
						elif(ifpart==-1 and elsepart==-1):
							print(lin)
						#print(lin)
						argsubs+=1	
					if(lin.find("else")!=-1):			#since else part doesnt contain any condition so ouside.. 
						#print('en')
						if(j!=elsetab[elseindex] and elseindex>=0):
							elseindex+=1
						elif(elseindex==-1):
							elseindex+=1
						
						elsedone=0
						ifpart=0
						if(ifdone!=1):
							elsepart=1
					
					#for k in range(index,len(argtypec)):
					if(flag==0):																	#for positional arguments
						#print('Hi')
						lin=s[j]
						for m in range(startarg,startarg+argtypec[index]):
							char=argname[m]
							#print(char)
							if(lin.find(char)!=-1):
								lin=lin.replace(char,argtabkv[m])
								#print(lin)
								flag=1
						while(1):
							if(lin.find("%")!=-1):
								loc=lin.find("%")
								char="%"+lin[loc+1]
								if(char not in argname):
									lin=lin.replace(char,'0')
									ws=lin.split()
									flag=1
								else:
									break
							else:
								break
						if(flag==1):
							#lin=s[j]
							ws=lin.split()
							if(lin.find("if")!=-1):
							#ifspot=1
								for x in range(len(ws)):
								#print('ENterd')
									if(ws[x] in symbols):
										logic=ws[x]
										break
								if(j!=iftab[ifindex] and ifindex>=0):
									ifindex+=1
								elif(ifindex==-1):
									ifindex+=1
								ifpart=0
								ifdone=0
								#print('Hi')
							#loc=lin.find("if")
								#print("logic is",logic)
								if(logic=='GE' and ws[x-1][0]!='%' and ws[x+1][0]!='%'):
									if((int)(ws[x-1])>=(int)(ws[x+1])):
										ifpart=1
								elif(logic=='LE' and ws[x-1][0]!='%' and ws[x+1][0]!='%'):
									if((int)(ws[x-1])<=(int)(ws[x+1])):
										ifpart=1
										#print('Entered')							
								elif(logic=='NE' and ws[x-1][0]!='%' and ws[x+1][0]!='%'):
									if((int)(ws[x-1])!=(int)(ws[x+1])):
										ifpart=1
								elif(logic=='LT' and ws[x-1][0]!='%' and ws[x+1][0]!='%'):
									if((int)(ws[x-1])<(int)(ws[x+1])):
										ifpart=1
								elif(logic=='GT' and ws[x-1][0]!='%' and ws[x+1][0]!='%'):
									if((int)(ws[x-1])>(int)(ws[x+1])):
										ifpart=1
								elif(logic=='EQ' and ws[x-1][0]!='%' and ws[x+1][0]!='%'):
									if((int)(ws[x-1])==(int)(ws[x+1])):
										ifpart=1
										#print('en')
							elif(ifpart==1 and ifdone==0):
								#print('Entered')
								if(j>iftab[ifindex] and j<iftab[len(iftab)-ifindex-1]):
									#print('entered2')
									print(lin)
								elif(j>iftab[len(iftab)-ifindex-1]):
									#print('en')
									ifdone=1
									ifpart=-1
							elif(lin.find("else")!=-1):
								#print('en')
								if(j!=elsetab[elseindex] and elseindex>=0):
									elseindex+=1
								elif(elseindex==-1):
									elseindex+=1
								elsedone=0
								if(ifdone!=1):
									elsepart=1
							elif(elsepart==1 and elsedone==0):
								#print('en')
								if(j>elsetab[elseindex] and j<elsetab[len(elsetab)-elseindex-1]):
									print(lin)
								elif(j>elsetab[len(elsetab)-elseindex-1]):
									elsedone=1
									elsepart=-1
							elif(ifpart==-1 and elsepart==-1 ):
								#print('en')
								print(lin)
								#print(lin)
							argsubs+=1
					#print('Entered')
					#if(flag==0):
						#for n in range(argsubs,len(argtabkv)):
							#for k in range(0,len(argtypec)):
								#for m in range(temp,argtypec[k]):
									#if(argsubs==n):
							#flag=1
							#print('Entered')
							#break
					#if(flag==1):
						#print(s[j].replace(argname[argsubs],argtabp[n]))
						#flag=0
					
					if(flag==0 and s[j].find("else")==-1 and s[j].find("endif")==-1):
						print(s[j])			
			startarg+=argtypec[index]
			expand=0
		elif(words[i]=='MACRO'):					#if MACRO found then its single line macro
			definesingle=1
			simple=0
			namesingle=1										
		elif(namesingle==1):
			namesingle=0
			snamtab.append(words[i])			#store its name in snamtab
			simple=0
		elif(definesingle==1):				
			valuetab.append(words[i])
			definesingle=0
		elif(words[i]=='STARTMACRO'):		#if STARTMACRO found then its multi line macro
			#print("Entered startmacro if")
			define=1
			deftab.append(line)				#store its starting line
			simple=0
			name=1
			#print(deftab)
			prototype=1
			countmacro+=1
		elif(name==1):
			name=0
			namtab.append(words[i])		#stroe its name in namtab
			#print(namtab)
			simple=0
		elif(define==1):						#define start
			if(words[i]=='ENDMACRO'):			#if endmacro found endling line stored
				#print("Entered endmacro")
				deftab.append(line)
				#print(deftab)
				countmacro-=1
				simple=0
			else:
				simple=0
				argcount=0
				#print("Entered define==1")
				#print(words[i])
				if(prototype==1):							#to store its arguments name from its prototype  remember not checking line by line ..it is words loop
					for j in range(len(words[i])):
				
						if(words[i][j]==','):
							argname.append('%'+words[i][j-1])
							#print(argname)
							argcount+=1
					argname.append('%'+words[i][len(words[i])-1])
					prototype=0
					#print(argname)
					argtypec.append(argcount+1)
			
					#print(argtypec)
				if(words[i]=="if"):				#if if found then if starting line stored in iftab
					ifyes=1
					iftab.append(line)
				elif(words[i]=="else"):		#if else found then else starting line stored in elsetab and if ending line stored
					ifyes=0
					elseyes=1
					iftab.append(line)
					elsetab.append(line)
				elif(words[i]=="endif"):		#if endif found 
					ifyes=0
					if(elseyes==1):
						elsetab.append(line)		#if it contains else then store its endling line
					else:
						iftab.append(line)		#or store if endling line 
					elseyes=0	
				
		if(countmacro==0):			#for nested macro....stack logic...0 1 2 1 0.. 
			define=0	
			
	if(simple==1 and countmacro==0 and define==0):
		print(l)				#didnt notice simple variable  it is used to tell if its not special or it is...if simple==1 then its asm code line...

#Thank You
#Author Aditya Sinha
