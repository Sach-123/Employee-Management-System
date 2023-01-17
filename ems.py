from tkinter import *
from tkinter import ttk
from tkinter.messagebox import *
from tkinter.scrolledtext import *
from pymongo import *
import requests
import matplotlib.pyplot as plt

def fn1():
	root.withdraw()
	aw.deiconify()
	aw_ent_id.focus()

def fn2():
	aw.withdraw()
	root.deiconify()

def fn3():#------------------Viewing--------------
	root.withdraw()
	vw.deiconify()
	vw_st.delete(1.0,END)
	
	con = None
	try:
		con = MongoClient("mongodb://localhost:27017")
		db = con["EMS1"]
		coll = db["emp"]
		data = coll.find()
		info = ""
		for d in data:
			info = info + "Id = " + str(d["_id"]) + " , Name = " + d["name"] + " , Salary = " + str(d["salary"]) + "\n"
		if info == "":
			vw_st.insert(INSERT,"--------NO RECORDS AVAILABLE--------")
		else:
			vw_st.insert(INSERT,info)	
	except Exception as e:
		showerror("Issue",e)
	finally:
		if con is not None:
			con.close()

def fn4():
	vw.withdraw()
	root.deiconify()

def fn5():
	root.withdraw()
	uw.deiconify()

def fn6():
	uw.withdraw()
	root.deiconify()

def fn7():
	root.withdraw()
	dw.deiconify()

def fn8():
	dw.withdraw()
	root.deiconify()

def fn9():#-----------------Charts-----------------
	con = None

	try:
		con = MongoClient("mongodb://localhost:27017")
		db = con["EMS1"]
		coll = db["emp"]
		data = coll.find().sort("salary",DESCENDING).limit(5)
		name=[]
		salary=[]
		for d in data:
			name.append(d["name"])
			salary.append(d["salary"])
		if len(name)==0:
			showerror("No Data","No data to display charts")
		else:
			plt.bar(name,salary,width=0.3,color="darkviolet")
			plt.xlabel("Name",)
			plt.ylabel("Salary")
			plt.title("Top "+str(len(name))+" salaried employee")
			plt.show()
		
	except Exception as e:
		showerror("Issue",e)

	finally:
		if con is not None:
			con.close()
		
	

def fn10():#-------------Adding----------------
	con = None
	try:
		con = MongoClient("mongodb://localhost:27017")
		db = con["EMS1"]
		coll = db["emp"]
		
		#-------------validation-------------------
		id = aw_ent_id.get()
		if(id==""):
			raise Exception("Id cannot be Empty")
		elif(not id.lstrip("-").isdigit() and id!=""):
			raise Exception("Id should contain positive numbers only")
		else:
			id = int(id)
			if(id<1):
				raise Exception("Id should contain positive numbers only")
		
		name = aw_ent_name.get()
		if (name==""):
			raise Exception("Name cannot be empty")
		elif(not name.isalpha()):
			raise Exception("Name should contains valid alphabets (a to z) only")
		elif(len(name)<2):
			raise Exception("Name should have minimum length of 2 character")
		
		salary = aw_ent_salary.get()
		if(salary==""):
			raise Exception("Salary cannot be Empty")
		elif(not salary.lstrip("-").isdigit() and salary!=""):
			raise Exception("Salary should contain numbers only")
		else:
			salary = int(salary)
			if(salary<0):
				raise Exception("Salary cannot be negative")
			elif(salary<8000):
				raise Exception("Salary should be minimum 8000")
		
		count = coll.count_documents({"_id":id})
		if (count==1):
			showerror("Invalid Id","Id already exists")
		else:
			info={"_id":id,"name":name,"salary":salary}
			coll.insert_one(info)
			showinfo("Success","Id "+str(id)+" added successfully")

	except Exception as e:
		showerror("issue", e)
		
	finally:
		if con is not None:
			con.close()
		aw_ent_id.delete(0,END)
		aw_ent_name.delete(0,END)
		aw_ent_salary.delete(0,END)
		aw_ent_id.focus()

def fn11():#---------------Updating------------------
	con = None
	try:
		con = MongoClient("mongodb://localhost:27017")
		db = con["EMS1"]
		coll = db["emp"]
		
		#-------------validation-------------------
		id = uw_ent_id.get()
		if(id==""):
			raise Exception("Id cannot be Empty")
		elif(not id.lstrip("-").isdigit() and id!=""):
			raise Exception("Id should contain positive numbers only")
		else:
			id = int(id)
			if(id<1):
				raise Exception("Id should be positive numbers only")
		
		name = uw_ent_name.get()
		if (name==""):
			raise Exception("Name cannot be empty")
		elif(not name.isalpha()):
			raise Exception("Name should contains valid alphabets (a to z) only")
		elif(len(name)<2):
			raise Exception("Name should have minimum length of 2 character")
		
		salary = uw_ent_salary.get()
		if(salary==""):
			raise Exception("Salary cannot be Empty")
		elif(not salary.lstrip("-").isdigit() and salary!=""):
			raise Exception("Salary should contain numbers only")
		else:
			salary = int(salary)
			if(salary<0):
				raise Exception("Salary cannot be negative")
			elif(salary<8000):
				raise Exception("Salary should be minimum 8000")

		count = coll.count_documents({"_id":id})
		if count ==1:
			coll.update_one({"_id":id},{"$set" : {"name":name,"salary":salary}})
			showinfo("Success","Employee with Id "+str(id)+" updated Successfully")
		else:
			showerror("No DATA","Id do not exist")

	except Exception as e:
		showerror("Issue",e)
		
	finally:
		if con is not None:
			con.close()
		uw_ent_id.delete(0,END)
		uw_ent_name.delete(0,END)
		uw_ent_salary.delete(0,END)
		uw_ent_id.focus()

def fn12():#---------------Deleting-------------
	con = None
	try:
		con = MongoClient("mongodb://localhost:27017")
		db = con["EMS1"]
		coll = db["emp"]
		
		#---------------validation------------------
		id = dw_ent_id.get()
		if(id==""):
			raise Exception("Id cannot be Empty")
		elif(not id.lstrip("-").isdigit() and id!=""):
			raise Exception("Id should contains positive number only")
		else:
			id = int(id)
			if(id<1):
				raise Exception("Id should be positive numbers only")
		
		count = coll.count_documents({"_id":id})
		if count==1:
			coll.delete_one({"_id":id})
			showinfo("Success", "Employee with Id "+str(id)+" deleted successfully")
		else:
			showerror("Issue:","Id do not exist")
	except Exception as e:
			showerror("Issue",e)
			
	finally:
		if con is not None:
			con.close()
		dw_ent_id.delete(0,END)
		dw_ent_id.focus()

def fn13():#--------------Deleting All------------
	answer = askyesno(title="Confirmation",message="Do you really want to delete all data?")
	if answer:
		con = None
		try:
			con = MongoClient("mongodb://localhost:27017")
			db = con["EMS1"]
			coll = db["emp"]
			count = coll.count_documents({})
			if count ==0:
				showerror("No Data","No data exists to delete")
			else:
				coll.delete_many({})
				showinfo("Success","All data deleted successfully")
		except Exception as e:
			showerror("Issue",e)
		finally:
			if con is not None:
				con.close()
	

#------------------Home Window----------------
root = Tk()
root.title("E.M.S")
root.geometry("550x600+100+100")
root.iconbitmap("employee.ico")
bg=PhotoImage(file="bg.png")
label1 = Label(root,image=bg)
label1.place(x=0,y=0)
f1 = ("Arial",25,"bold")
f2 = ("Agency FB",35)

btn_add = Button(root,text="Add",font=f1,width=15,borderwidth=3,relief="ridge",command=fn1)
btn_view = Button(root,text="View",font=f1,width=15,borderwidth=3,relief="ridge",command=fn3)
btn_update = Button(root,text="Update",font=f1,width=15,borderwidth=3,relief="ridge",command=fn5)
btn_delete = Button(root,text="Delete",font=f1,width=15,borderwidth=3,relief="ridge",command=fn7)
btn_charts = Button(root,text="Charts",font=f1,width=15,borderwidth=3,relief="ridge",command=fn9)

btn_add.pack(pady=10)
btn_view.pack(pady=10)
btn_update.pack(pady=10)
btn_delete.pack(pady=10)
btn_charts.pack(pady=10)

sep = ttk.Separator(root,orient="horizontal")
sep.pack(fill="x")


lab_loc = Label(root,text="Location: ", font=f2)
lab_loc_res = Label(root,text="",font=f2,fg="crimson")
lab_temp = Label(root,text="Temp: ",font=f2)
lab_temp_res = Label(root,text="",font=f2,fg="crimson")

lab_loc.place(x=10,y=475)
lab_loc_res.place(x=150,y=475)
lab_temp.place(x=300,y=475)
lab_temp_res.place(x=400,y=475)

try:
	la = "https://ipinfo.io/"
	res = requests.get(la)
	data = res.json()
	city = data["city"]

	ta1 = "https://api.openweathermap.org/data/2.5/weather"
	ta2 = "?q="+city
	ta3 = "&appid="+"aaf5677ac0821cdb477c3365b2871a45"+"&units=metric"
	ta = ta1 + ta2 + ta3
	res = requests.get(ta)
	data = res.json()
	temp = data["main"]["temp"]

	lab_loc_res.configure(text=city)
	lab_temp_res.configure(text=str(temp)+"\u00B0C")
except Exception as e:
	showerror("Unable to Fetch Data",e)
	lab_loc_res.configure(text="---")
	lab_temp_res.configure(text="---")


#-------------------Add Window--------------------
aw = Toplevel(root)
aw.title("Add Employee")
aw.geometry("550x600+100+100")
aw.iconbitmap("employee.ico")
label2 = Label(aw,image=bg)
label2.place(x=0,y=0)

aw_lab_id = Label(aw,text="Enter id ",font=f1)
aw_ent_id = Entry(aw,font=f1,bd=3)
aw_lab_name = Label(aw,text="Enter name ",font=f1)
aw_ent_name = Entry(aw,font=f1,bd=3)
aw_lab_salary = Label(aw,text="Enter salary ",font=f1)
aw_ent_salary = Entry(aw,font=f1,bd=3)

aw_btn_save = Button(aw,text="Save",font = f2,width=10,borderwidth=3,relief="raised",command=fn10)
aw_btn_back = Button(aw,text="Back",font = f2,width=10,borderwidth=3,relief="raised",command=fn2)

aw_lab_id.pack(pady=10)	
aw_ent_id.pack()
aw_lab_name.pack(pady=10)
aw_ent_name.pack()
aw_lab_salary.pack(pady=10)
aw_ent_salary.pack()

aw_btn_save.pack(pady=(30,10))
aw_btn_back.pack(pady=10)


def fn14(event):
	fn10()
aw_btn_save.bind("<Return>",fn14)

aw.withdraw()
aw.protocol("WM_DELETE_WINDOW",root.destroy)


#----------------------View Window-----------------
vw = Toplevel(root)
vw.title("View Records")
vw.geometry("550x600+100+100")
vw.iconbitmap("employee.ico")
label3 = Label(vw,image=bg)
label3.place(x=0,y=0)
f3 = ("Arial",20,"bold")


vw_st = ScrolledText(vw,font=f3,width=34,height=12,bd=4)
vw_btn_back = Button(vw,text="Back",font=f2,width=10,borderwidth=3,relief="raised",command=fn4)

vw_st.pack(pady=10)
vw_btn_back.pack(pady=10)



vw.withdraw()
vw.protocol("WM_DELETE_WINDOW",root.destroy)


#---------------------Update Window-------------------

uw = Toplevel(root)
uw.title("Update Employee Record")
uw.geometry("550x600+100+100")
uw.iconbitmap("employee.ico")
label4 = Label(uw,image=bg)
label4.place(x=0,y=0)

uw_lab_id = Label(uw,text="Enter Id ",font=f1)
uw_ent_id = Entry(uw,font=f1,bd=3)
uw_lab_name = Label(uw,text="Enter name ",font=f1)
uw_ent_name = Entry(uw,font=f1,bd=3)
uw_lab_salary = Label(uw,text="Enter salary ",font=f1)
uw_ent_salary = Entry(uw,font=f1,bd=3)

uw_btn_save = Button(uw,text="Save",font = f2,width=10,borderwidth=3,relief="raised",command=fn11)
uw_btn_back = Button(uw,text="Back",font = f2,width=10,borderwidth=3,relief="raised",command=fn6)

uw_lab_id.pack(pady=10)
uw_ent_id.pack()
uw_lab_name.pack(pady=10)
uw_ent_name.pack()
uw_lab_salary.pack(pady=10)
uw_ent_salary.pack()

uw_btn_save.pack(pady=(30,10))
uw_btn_back.pack(pady=10)

def fn15(event):
	fn11()
uw_btn_save.bind("<Return>",fn15)

uw.withdraw()
uw.protocol("WM_DELETE_WINDOW",root.destroy)


#---------------------Delete Window---------------------

dw = Toplevel(root)
dw.title("Delete Record")
dw.geometry("550x600+100+100")
dw.iconbitmap("employee.ico")
label5 = Label(dw,image=bg)
label5.place(x=0,y=0)

dw_lab_id = Label(dw,text="Enter Id",font=f1)
dw_ent_id = Entry(dw,font=f1,bd=3)
dw_btn_save = Button(dw,text="Save",font = f2,width=10,borderwidth=3,relief="raised",command=fn12)
dw_btn_back = Button(dw,text="Back",font = f2,width=10,borderwidth=3,relief="raised",command=fn8)
dw_btn_delall = Button(dw,text="Delete All",font = f2,width=10,bg="red",fg="white",borderwidth=5,relief="groove",command=fn13)

dw_lab_id.pack(pady=10)
dw_ent_id.pack()
dw_btn_save.pack(pady=(30,10))
dw_btn_back.pack(pady=10)
dw_btn_delall.pack(pady=10)

def fn16(event):
	fn12()
dw_btn_save.bind("<Return>",fn16)

dw.withdraw()
dw.protocol("WM_DELETE_WINDOW",root.destroy)


root.mainloop()
