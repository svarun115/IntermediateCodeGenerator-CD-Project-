import re
def print_blocks():
    for block in range(len(blocks)):
        print("BLOCK ",block+1)
        temp = blocks[block]
        for no in range(temp[0],temp[1]):
            print(inp[no],end='')
        print()

def remove_cse():
    for num in range(len(blocks)):
        check_cse(blocks[num])

def print_inter():
    for line in inp:
        if line:
            print(line,end='')


def check_cse(block):
    cse_d = []
    rhs = []
    goto = 0
    for no in range(block[0],block[1]):
        temp = inp[no].split("=")
        if 'goto' in inp[no]:
            cse_d.append(inp[no])
        else:
            cse_d.append([temp[0].strip().rstrip(),temp[1].rstrip().strip()])
            rhs.append(temp[1].rstrip().strip())
    temp = set(rhs)
    for ele in temp:
        rhs.remove(ele)
    for ele in rhs:
        ids = re.findall("[a-zA-Z_]+[a-zA-Z0-9]*",ele)
        for i in range(len(cse_d)):
            if cse_d[i][1]==ele:
                for j in range(i+1,len(cse_d)):
                    if cse_d[i][0] in ids:
                        break
                    if cse_d[j][1]==ele:
                        cse_d[j][1]=cse_d[i][0]
    j = 0
    for no in range(block[0],block[1]):
        if 'goto' in cse_d[j]:
            inp[no] = cse_d[j]
            j+=1
        else:
            inp[no]=cse_d[j][0] + ' = ' + cse_d[j][1] + '\n'
            j+=1

    #print("\n\nCse_d:\n",cse_d)
    return cse_d

def create_blocks():
    for i in range(1,len(inp)):
        if "goto" in inp[i]:
            p=re.search(r'goto.*?([0-9]+)',inp[i])
            gofrom.add(int(i))
            goto.add(int(p.groups()[0]))
    uni = goto.union(gofrom)
    temp = min(goto.union(gofrom))
    blocks.append([1,temp])
    if temp in goto:
        goto.remove(temp)
    if temp in gofrom:
        gofrom.remove(temp)
    gofrom_cpy = list(gofrom)
    prev = temp
    while gofrom_cpy:
        temp = min(gofrom_cpy)
        blocks.append([prev,temp+1])
        prev = temp+1
        gofrom_cpy.remove(temp)
    temp = temp + 1
    blocks.append([temp,len(inp)])

def write_inter():
    out = open("out.txt","w")
    for line in inp:
        if line:
            out.write(line)

def write_block():
    blk = open("blocks.txt","w")
    for block in range(len(blocks)):
        blk.write("BLOCK "+str(block+1))
        blk.write('\n')
        temp = blocks[block]
        for no in range(temp[0],temp[1]):
            blk.write(inp[no])
        blk.write('\n')



def remove_cpy():
	for num in range(len(blocks)):
		cpy_prop(blocks[num])
		#cpy_prop(blocks[4])

def cpy_prop(block):
	cpy_d = []
	rhs=[]
	lhs=[]
	goto = 0
	global c
	global inp
	for no in range(block[0],block[1]):
		
		temp = inp[no].split("=")
		if 'goto' in inp[no]:
			cpy_d.append(inp[no])
			
		else:
		    cpy_d.append([temp[0].strip().rstrip(),temp[1].rstrip().strip()])
		    rhs.append(temp[1].rstrip().strip())
		    lhs.append(temp[0].rstrip().strip())
	#print(rhs)
	r=[]
	for i in rhs:
		s=re.search(r'(t\d+?)|(.*?\[t\d+?\])',i)
		if str(type(s))=="<class '_sre.SRE_Match'>":
			for j in s.groups():
				if j is not None:
					r.append(j)
	l=[]
	temp1=r
	for i in temp1:
		s=re.search(r'(.*?\[t\d+?\])',i)

		if str(type(s))=="<class '_sre.SRE_Match'>":
			print("GROUP MATCH",s.group())
			index=rhs.index(i)
			if lhs[index] not in rhs[index::]:
				print("POPPING ",cpy_d[index])
				r.remove(i)


	print("r is ",r)
	print("RHS: ",rhs)
	copy=cpy_d
	temp=rhs
	for i in temp:
		if i in r:
			for term in copy:
				if i in term:
					index=cpy_d.index(term)
					break
			l.append([index,cpy_d[index][0],cpy_d[index][1]])
			cpy_d.remove(l[-1][1::])
			
	rhs=temp		
	cpy_d=copy
			

	print("this is the list l: ",l)
	#print("cse_d is ",cse_d)
	#print("\n\n")
	for i in l:
		for j in range(i[0],len(cpy_d)):
			if i[1] in cpy_d[j][0]:
				#print("inside if")
				#print("to be replaced ",cse_d[j][0])
				cpy_d[j][0]=cpy_d[j][0].replace(i[1],i[2])
				#l.pop()
				#print("success: ",cse_d[j][0])
				
				#print("=================================")
			elif i[1] in cpy_d[j][1]:
				#print("inside elif")
				#print("to be replaced ",cse_d[j][1])
				cpy_d[j][1]=cpy_d[j][1].replace(i[1],i[2])
				#print("success: ",cse_d[j][1])

				#print("=================================")
	c_list=[]
	for u in cpy_d:
		if u[1]!=u[0]:
			c_list.append(u)
	cpy_d=c_list

	#print("Cpy_d:\n\n",cpy_d)

	
	

	temp=[0 for i in range(len(cpy_d))]
	
	for no in range(len(temp)):
       		if 'goto' in cpy_d[no]:
            		temp[no] = cpy_d[no]
            		
        	else:
            		temp[no]=cpy_d[no][0] + ' = ' + cpy_d[no][1] + '\n'
            		


	#print("\n\nTemp:\n",temp)

	count=0
	for var in range(block[0],block[1]):
			if count < len(temp):
				inp[var] = temp[count]
					
			else:
				inp[var] = None
			count+=1
	
	#for var in range(len(inp[1:])):
	#	if inp[var] == None:
	#		inp.pop(var)

	
	

	#print("\n\n")
	#print("cse_d after popping ",cse_d)

	#return cpy_d

inp = open("for.txt","r").readlines()
inp.insert(0,None)
gofrom = set()
goto = set()
blocks=[]
count1=len(inp)
create_blocks()
print_blocks()
remove_cse()
with open("cse_output.txt",'w') as f:	
	f.writelines(inp[1:])
blocks=[]
create_blocks()
print_blocks()
print("\n\nBefore copy propagation:\n\n")
for k in inp:
	print(k)
		

remove_cpy()
blocks=[]
while None in inp:
	inp.remove(None)
inp.insert(0,None)
create_blocks()
print("\n\nAfter eliminating copy propagation:\n\n")
for k in inp:
	print(k)
	
count2=len(inp)
print("Before:",count1)
print("After:",count2)

with open("output.txt",'w') as f:	
	f.writelines(inp[1:])
