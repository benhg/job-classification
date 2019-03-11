import sqlite3

with open("edges") as file:
	line=file.readline()
	line=file.readline()
	conn = sqlite3.connect('/Users/ben/jevin_west/edge_data.db')
	c=conn.cursor()
	while line:
		source=int(line.split(" ")[0])
		target=int(line.split(" ")[1].strip())
		sql="INSERT INTO edges VALUES ({},{})".format(source,target)
		c.execute(sql)
		line=file.readline()
        conn.commit()
	conn.close()
