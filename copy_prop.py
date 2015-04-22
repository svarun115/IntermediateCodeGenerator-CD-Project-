def remove_cpy():
	for num in range(len(blocks)):
		cpy_prop(blocks[num])
def cpy_prop(block):
	cse_d = []
	rhs=[]
	goto = 0
	global c
	for no in range(block[0],block[1]):
		print("0: ",block[0])
		print("1: ",block[1])
		temp = inp[no].split("=")
		if 'goto' in inp[no]:
			cse_d.append(inp[no])
			
		else:
		    cse_d.append([temp[0].strip().rstrip(),temp[1].rstrip().strip()])
		    rhs.append(temp[1].rstrip().strip())
	#print(rhs)
	r=[]
	for i in rhs:
		s=re.search(r'(t\d+?)|(.*?\[t\d+?\])',i)
		if str(type(s))=="<class '_sre.SRE_Match'>":
			for j in s.groups():
				if j is not None:
					r.append(j)
	l=[]
	
	for i in rhs:
		if i in r:
			index=rhs.index(i)
			l.append([index,cse_d[index][0],cse_d[index][1]])
			

	#print("this is the list l: ",l)
	#print("cse_d is ",cse_d)
	#print("\n\n")
	for i in l:
		for j in range(i[0],len(cse_d)):
			if i[1] in cse_d[j][0]:
				#print("inside if")
				#print("to be replaced ",cse_d[j][0])
				cse_d[j][0]=cse_d[j][0].replace(i[1],i[2])
				#print("success: ",cse_d[j][0])
				
				#print("=================================")
			elif i[1] in cse_d[j][1]:
				#print("inside elif")
				#print("to be replaced ",cse_d[j][1])
				cse_d[j][1]=cse_d[j][1].replace(i[1],i[2])
				#print("success: ",cse_d[j][1])

				#print("=================================")
	c_list=[]
	for u in cse_d:
		if u[1]!=u[0]:
			c_list.append(u)
	cse_d=c_list
	#print("\n\n")
	#print("cse_d after popping ",cse_d)
