import re

def dead_code():
	lhs=[]
	rhs=[]
	dead=[]
	for i in inp[1:]:
		if 'goto' in i:
			rhs.append(i)
			continue
		elif '=' not in i:
			rhs.append(i)
			continue
		temp=i.split('=')
		if '[' not in temp[0]:
			lhs.append(temp[0].strip())
		else:
			l=re.search(r'.*\[(.*)\].*',temp[0]).group(1)
			rhs.append(l)
		for x in temp[1:]:
			rhs.append(x)
	lhs=set(lhs)
	rhs=set(rhs)
	for i in lhs:
		for j in rhs:
			if re.search(r'\b'+i+r'\b',j):
				break
		else:
			dead.append(i)
	print("The dead variables are:\n",dead)

	#removing the dead code statements
	for i in range(1,len(inp)):
		for j in dead:
			if inp[i]!=None:
				if re.search(r'\b'+j+r'\b',inp[i]):
					inp[i]=None
	
	
	while None in inp:
		inp.remove(None)
	inp.insert(0,None)

	#writing into a file
	with open('dead.txt','w') as f:
		f.writelines(inp[1:])


def print_blocks():
    for block in range(len(blocks)):
        print("BLOCK ",block+1)
        temp = blocks[block]
        for no in range(temp[0],temp[1]):
            print(inp[no],end='')
        print()

def file_cpy():
	with open("cpy_output.txt",'w') as f:	
		f.writelines(inp[1:])

def file_cse():
	with open("cse_output.txt",'w') as f:	
		f.writelines(inp[1:])

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
    flag = 0 
    for ele in rhs:
        ids = re.findall("[a-zA-Z_]+[a-zA-Z0-9]*",ele)
        for i in range(len(cse_d)):
            modded = 0
            if cse_d[i][1]==ele:
                for j in range(i+1,len(cse_d)):
                    if cse_d[j][0] in ids:
                        flag = 1
                        continue
                    if cse_d[j][1]==ele:
                        if flag==1:
                            flag = 0
                            i = j
                        else:
                            cse_d[j][1]=cse_d[i][0]
    j = 0
    for no in range(block[0],block[1]):
        if 'goto' in cse_d[j]:
            inp[no] = cse_d[j]
            j+=1
        else:
            inp[no]=cse_d[j][0] + ' = ' + cse_d[j][1] + '\n'
            j+=1
    return cse_d

def create_blocks():
	for i in range(1,len(inp)):
	 	if "goto" in inp[i]:
	 		p=re.search(r'goto.*?([0-9]+)',inp[i])
	 		gofrom.add(int(i))
	 		goto.add(int(p.groups()[0]))

	if len(gofrom) != 0 and len(goto) != 0:
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

	else:
		gofrom.add(1)
		goto.add(len(inp))

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
	

def cpy_prop(block):
	cpy_d = []
	rhs=[]
	lhs=[]
	goto = 0
	global inp
	for no in range(block[0],block[1]):		
		temp = inp[no].split("=")
		if 'goto' in inp[no]:
			cpy_d.append(inp[no])
		else:
		    cpy_d.append([temp[0].strip().rstrip(),temp[1].rstrip().strip()])
		    rhs.append([len(cpy_d)-1,temp[1].rstrip().strip()])
		    lhs.append([len(cpy_d)-1,temp[0].rstrip().strip()])
	r=[]
	l=[]

	for i in rhs:
		s=re.search(r'(t\d+?)|(.*?\[t\d+?\])',i[1])
		if str(type(s))=="<class '_sre.SRE_Match'>":
			for j in s.groups():
				if j is not None:
					if '[' in j:
						
						if lhs[i[0]][1] in [rhs[y][1] for y in range(i[0]+1,len(rhs))]:
							r.append(rhs[i[0]])
					else:
						r.append(rhs[i[0]])
	
	for i in rhs:
		if i in r:
			ter=lhs[i[0]]+[i[1]]
			l.append(ter)
			
	for i in l:
		for j in range(i[0],len(cpy_d)):
			if i[1] in cpy_d[j][0]:
				cpy_d[j][0]=cpy_d[j][0].replace(i[1],i[2])
			elif i[1] in cpy_d[j][1]:
				cpy_d[j][1]=cpy_d[j][1].replace(i[1],i[2])

	c_list=[]
	for u in cpy_d:
		if u[1]!=u[0]:
			c_list.append(u)
	cpy_d=c_list

	temp=[0 for i in range(len(cpy_d))]
	
	for no in range(len(temp)):
       		if 'goto' in cpy_d[no]:
            		temp[no] = cpy_d[no]
            		
        	else:
            		temp[no]=cpy_d[no][0] + ' = ' + cpy_d[no][1] + '\n'

	count=0
	for var in range(block[0],block[1]):
			if count < len(temp):
				inp[var] = temp[count]
					
			else:
				inp[var] = None
			count+=1

	
inp = open("input.txt","r").readlines()
inp.insert(0,None)
gofrom = set()
goto = set()
blocks=[]
count1=len(inp)
print("-------------------------------------------------------")
print("Eliminating dead code.\nOutput written into 'dead.txt'")
dead_code()
print("-------------------------------------------------------")
print("Creating simple blocks.\nOutput written into 'blocks.txt'")
create_blocks()
write_block()
#print_blocks()
print("-------------------------------------------------------")
print("Removing common subexpressions.\nOutput written into 'cse_output.txt'")
remove_cse()
file_cse()

# start of copy propagation	
print("-------------------------------------------------------")
print("Copy Propagation:\nOutput written into 'cpy_output.txt'")
#print_blocks()
remove_cpy()
#blocks=[]

while None in inp:
		inp.remove(None)
inp.insert(0,None)

#gofrom = set()
#goto = set()

#create_blocks()
file_cpy()
#print_blocks()

count2=len(inp)
print("-------------------------------------------------------")
print("Number of lines before code optimisation:",count1)
print("Number of lines after code optimisation:",count2)
print("-------------------------------------------------------")
