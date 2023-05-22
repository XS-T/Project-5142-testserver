from json_tables import JSONTable

table = JSONTable("table.json")
table.load()

table.add("Alex", "Germany")

lookup_result = table.lookup("Emily")
if lookup_result:
    print("Found:", lookup_result)
else:
    print("Not found.")

table.save()
