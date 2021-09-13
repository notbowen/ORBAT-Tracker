#Libraries needed
import requests
import time
import ctypes
from termcolor import colored

#variables
missing = []

#initialise colors on output console
def init_colors():
	kernel32 = ctypes.WinDLL('kernel32')
	hStdOut = kernel32.GetStdHandle(-11)
	mode = ctypes.c_ulong()
	kernel32.GetConsoleMode(hStdOut, ctypes.byref(mode))
	mode.value |= 4
	kernel32.SetConsoleMode(hStdOut, mode)

#check if player is in grp function
def checkGroup(name):
	inGroup = False

	#gets API request to find user ID
	id = requests.get("https://api.roblox.com/users/get-by-username", params={"username": name})
	#returns {"success": "false"} if no username, returns some other json val if user exists
	if "success" in str(id.json()): #if success is in there means invalid/username not found
		return "Missing"  #returns value to stop running the code below
		
	#parses the json response to get id
	id = id.json()['Id']
	#makes another API call, this time to the roblox group API
	groups = requests.get(f"https://groups.roblox.com/v2/users/{id}/groups/roles")
	groups = groups.json()['data'] #returns a whole json data of groups and its info
	for group in groups:
		if group['group']['id'] == 4929233: #MPC group id: 4929233
			inGroup = True

	return inGroup


#init colors
init_colors()

#log
print("[" + colored("INIT", "yellow") + "] " + "Colors initialised")
print("[" + colored("INIT", "yellow") + "] " + "Functions initialised")
	
#opens the userfile
with open("userList.txt", "r")as f: #edit the "userList.txt" if you want your own input file name
	names = f.read() #returns a string of the content in userList
	f.close()

#splits from string into a list
names = names.split('\n')

#log
print("[" + colored("INIT", "yellow") + "] " + "Names gotten, initialising checker.")
print()

#loop
for name in names:
	if name.startswith('Bravo ') or name.startswith('BATTALION') or name == "USERNAME" or name.startswith('Advisory Unit') or name.startswith('1st Platoon') or name.startswith('2nd Platoon') or name.startswith('-') or name.startswith('Officer Grade') or name.startswith('Awaiting Placement') or name == '' : continue  #Text filter
	chek = checkGroup(name) #calls the function, would store True, False or "Missing"
	#output
	if chek == False:
		print("[" + colored("-", "red") + "] " + name + " is not in the MPC group!")
		missing.append(name) #if not in MPC group, put into list to be printed later
	elif chek == "Missing":
		print("[" + colored("-", "red") + "] " + name + " was not found on Roblox")
	else:
		print("[" + colored("+", "green") + "] " + name + " is in the MPC group :D")

	time.sleep(1)

#list of ppl who are not in group
print("\n===== People who are not in MPC group =====")
if len(missing) > 0:
	for i in missing:
		print(str(missing.index(i) + 1) + '. ' + i) #prints out like: 1. skybird380 etc.
else:
	print("None :D")
while True:
	pass #to keep the console on so that it doesn't close once program ends