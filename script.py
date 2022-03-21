import requests
from bs4 import BeautifulSoup
import threading

def get_solution(ex_num, primary_type):
	site = requests.get(get_solution_link(ex_num))
	soup = BeautifulSoup(site.content, 'html.parser')
	img = soup.find("img", {"class": "newDataIMG", "src": True, "alt": True})
	if "https" not in img['src']:
		if primary_type:
			done_primary.append(((ex_num), (" - " + "https://zdam.xyz" + img['src'] + "\n")))
		else:
			done_secondary.append(((ex_num), (" - " + "https://zdam.xyz" + img['src'] + "\n")))
	else:
		if primary_type:
			done_primary.append(((ex_num), (" - " + img['src'] + "\n")))
		else:
			done_secondary.append(((ex_num), (" - " + img['src'] + "\n")))

def get_solution_link(ex_num):
	return "https://zdam.xyz/" + str(124551 + ex_num)

	
exercises_primary = [4, 7, 9, 10, 12, 20, 24, 26, 27, 40, 44, 59, 67, 73, 76, 77, 80]
exercises_secondary = [(i if i != 23 and i != 25 and i != 26 else None) for i in range(15, 31)]
threads = []
done_primary = []
done_secondary = []

while None in exercises_secondary:
	exercises_secondary.remove(None)

for ex_num in exercises_primary:
	get_solution_thread = threading.Thread(target=get_solution, args=(ex_num, True))
	threads.append(get_solution_thread)
	get_solution_thread.start()
for thread in threads:
	thread.join()

threads = []
for ex_num in exercises_secondary:
	get_solution_thread = threading.Thread(target=get_solution, args=(ex_num, False))
	threads.append(get_solution_thread)
	get_solution_thread.start()
for thread in threads:
	thread.join()

with open("matma-zadania.txt", "w") as file:
	file.write("Math exercises\n\n")
	file.write("Primary:\n")
	for exercise in sorted(done_primary, key=lambda x: x[0]):
		file.write(str(exercise[0]) + exercise[1])
	file.write("Secondary:\n")
	for exercise in sorted(done_secondary, key=lambda x: x[0]):
		file.write(str(exercise[0]) + exercise[1])
    
print("DONE")
