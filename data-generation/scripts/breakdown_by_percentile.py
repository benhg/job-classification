
# coding: utf-8

# In[1]:

import MySQLdb as mysql
db=mysql.connect(host="wos2.cvirc91pe37a.us-east-1.rds.amazonaws.com",user="benjaminglick"
                 ,passwd="7a6dfd8e3c5e44e7be56",db="wos2")


# In[2]:

cursor = mysql.cursors.SSCursor(db)
cursor.execute("""SELECT contributors.wos_id, email_addr, contributors.display_name, COUNT(contributors.wos_id) FROM refs JOIN contributors ON refs.wos_id=contributors.wos_id GROUP BY wos_id DESC;""")


# In[3]:

percentile_size=2001283
contribs=cursor.fetchmany(percentile_size)


# In[4]:

#print(contribs)


# In[5]:

percentile_out={}


# In[6]:
percentile=99
import json
while percentile!=0:
    percentile_out={}
    total=len(contribs)
    percentile_contributors=[ "%s" % x[1] for x in contribs]
    #print(percentile_contributors)
    with_email=sum(x != 'None' for x in percentile_contributors)
    #print(with_email)
    print((percentile_contributors, percentile))
    topicCoverage=float(with_email/total)
    percentile_out[percentile] = topicCoverage
    contribs = cursor.fetchmany(percentile_size)
    percentile-=1
    output=open("output_percentile.json",'a')
    output.write(json.dumps(percentile_out, indent=4))
    output.close()
    if not contribs:
       break
