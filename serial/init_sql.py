import sqlite3

conn=sqlite3.connect('vics.db')

c=conn.cursor()
c.execute('''create table entries (block integer not null,state integer,parking integer,park_num integer,'text' text )''')
conn.commit()

for i in range(1,21):
	if i==5:
		c.execute("insert into entries (block,state,parking,park_num) values (?,?,?,?)",[i,0,65,255])
	elif i==15:
		c.execute("insert into entries (block,state,parking,park_num) values (?,?,?,?)",[i,0,64,255])
	else:
		c.execute("insert into entries (block,state,parking,park_num) values (?,?,?,?)" ,[i,0,0,0])

	conn.commit()

cur=c.execute("select * from entries")
print cur.fetchall()
