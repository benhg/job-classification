"""This file will connect to the database, get a list of all of the fields, 
and then calculate  email coverage for all fields"""
# coding: utf-8

# In[1]:

import MySQLdb as mysql
db=mysql.connect(host="DB HOST",user="DB USER"
                ,passwd="DB PASS",db="wos2")


# In[ ]:
#Get all fields
cursor = mysql.cursors.SSCursor(db)
cursor.execute("""SELECT DISTINCT subject FROM contributors JOIN subjects ON subjects.wos_id=contributors.wos_id""")


# In[3]:

topic=cursor.fetchone()
print(topic)


# In[4]:

print((topic[0]))


# In[5]:

db2=mysql.connect(host="DB HOST",user="DB USER"
                ,passwd="DB PASS",db="wos2")
cursor2=db2.cursor(mysql.cursors.SSCursor)
coverage={}


# In[6]:
"""calculates vounts and coverage."""
while True:
    sql="""SELECT email_addr FROM subjects JOIN contributors ON subjects.wos_id=contributors.wos_id WHERE subject='{}'""".format(mysql.escape_string(topic[0]).decode("utf-8"))
    #print(sql)
    cursor2.execute(sql)
    topic_contributors=cursor2.fetchall()
    topic_contributors=[ "%s" % x for x in topic_contributors ]
    total=len(topic_contributors)
    emails=sum(x != 'None' for x in topic_contributors)
    topicCoverage=(emails/total)
    coverage[topic[0]] = topicCoverage
    coverage[topic[1]] = total
    topic = cursor.fetchone()
    if not topic:
       break


# In[7]:

#print(topic_contributors)


# In[8]:

print(coverage)
print((len(coverage)))


# In[9]:

import json
output=open("output_field.json",'w')
output.write(json.dumps(coverage, indent=4))


# In[10]:

output.close()


# In[ ]:



