"""
	Days of the week Chapter 4
	CS 351

	Description:
		Working with different types of collection
"""

days = {
	1 : "Monday",
	2 : "Tuesday",
	3 : "Wednesday",
	4 : "Thursday",
	5 : "Friday",
	6 : "Satuday",
	7 : "Sunday"
}

print(days)
print(list(days.keys()))
# Generator function to get only the values for all keys in days
print(tuple(days.get(x) for x in days.keys()))
