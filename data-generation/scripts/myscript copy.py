# In[1]:
import pip
pip.main(['install', "MySQL-python"])

import MySQLdb as mysql
db=mysql.connect(host="wos2.cvirc91pe37a.us-east-1.rds.amazonaws.com",user="benjaminglick" ,passwd="7a6dfd8e3c5e44e7be56",db="wos2")


# In[ ]:

cursor = mysql.cursors.SSCursor(db)
cursor.execute("""SELECT DISTINCT subject FROM contributors JOIN subjects ON subjects.wos_id=contributors.wos_id""")


# In[3]:

topic=cursor.fetchone()
print(topic)


# In[4]:

print((topic[0]))


# In[5]:

db2=mysql.connect(host="wos2.cvirc91pe37a.us-east-1.rds.amazonaws.com",user="benjaminglick" ,passwd="7a6dfd8e3c5e44e7be56",db="wos2")
cursor2=db2.cursor(mysql.cursors.SSCursor)
coverage={}


# In[6]:

while True:
    sql="""SELECT email_addr FROM subjects JOIN contributors ON subjects.wos_id=contributors.wos_id WHERE subject='{}'""".format(mysql.escape_string(topic[0]).decode("utf-8"))
    #print(sql)
    cursor2.execute(sql)
    topic_contributors=cursor2.fetchall()
    topic_contributors=[ "%s" % x for x in topic_contributors ]
    total=len(topic_contributors)
    emails=sum(x != 'None' for x in topic_contributors)
    topicCoverage=float(float(emails)/float(total))
    coverage[topic[0]] = total, topicCoverage
    topic = cursor.fetchone()
    if not topic:
       break


# In[7]:

#print(topic_contributors)


# In[8]:

#print(coverage)
#print (len(coverage))


# In[9]:

import json
output=open("output_field.json",'w')
output.write(json.dumps(coverage, indent=4))


# In[10]:

output.close()


# In[ ]: