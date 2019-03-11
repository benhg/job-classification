
# coding: utf-8

# In[1]:

import MySQLdb as mysql
import multiprocessing
db=mysql.connect(host="DB HOST",user="DB USER"
                ,passwd="DB PASS",db="wos2")


# In[ ]:




# In[ ]:




# In[2]:
topics=["Chemistry, Multidisciplinary","Chemistry, Physical","Clinical Neurology","Communication","Computer Science, Artificial Intelligence","Computer Science, Cybernetics","Computer Science, Hardware & Architecture","Computer Science, Information Systems","Computer Science, Interdisciplinary Applications","Computer Science, Software Engineering","Computer Science, Theory & Methods","Construction & Building Technology","Criminology & Penology","Critical Care Medicine","Crystallography","Cultural Studies","Dance","Demography","Dentistry, Oral Surgery & Medicine","Dermatology","Developmental Biology","Ecology","Economics","Education & Educational Research","Education, Scientific Disciplines","Education, Special","Electrochemistry","Emergency Medicine","Endocrinology & Metabolism","Energy & Fuels","Engineering, Aerospace","Engineering, Biomedical","Engineering, Chemical","Engineering, Civil","Engineering, Electrical & Electronic","Engineering, Environmental","Engineering, Geological","Engineering, Industrial","Engineering, Manufacturing","Engineering, Marine","Engineering, Mechanical","Engineering, Multidisciplinary","Engineering, Ocean","Engineering, Petroleum","Entomology","Environmental Sciences","Environmental Studies","Ergonomics","Ethics","Ethnic Studies","Evolutionary Biology","Family Studies","Film, Radio, Television","Fisheries","Folklore","Food Science & Technology","Forestry","Gastroenterology & Hepatology","Genetics & Heredity","Geochemistry & Geophysics","Geography","Geography, Physical","Geology","Geosciences, Multidisciplinary","Geriatrics & Gerontology","Gerontology","Green & Sustainable Science & Technology","Health Care Sciences & Services","Health Policy & Services","Hematology","History","History & Philosophy of Science","History of Social Sciences","Horticulture","Hospitality, Leisure, Sport & Tourism","Humanities, Multidisciplinary","Imaging Science & Photographic Technology","Immunology","Industrial Relations & Labor","Infectious Diseases","Information Science & Library Science","Instruments & Instrumentation","Integrative & Complementary Medicine","International Relations","Language & Linguistics","Law","Limnology","Linguistics","Literary Reviews","Literary Theory & Criticism","Literature","Literature, African, Australian, Canadian","Literature, American","Literature, British Isles","Literature, German, Dutch, Scandinavian","Literature, Romance","Literature, Slavic","Logic","Management","Marine & Freshwater Biology","Materials Science, Biomaterials","Materials Science, Ceramics","Materials Science, Characterization & Testing","Materials Science, Coatings & Films","Materials Science, Composites","Materials Science, Multidisciplinary","Materials Science, Paper & Wood","Materials Science, Textiles","Mathematical & Computational Biology","Mathematics","Mathematics, Applied","Mathematics, Interdisciplinary Applications","Mechanics","Medical Ethics","Medical Informatics","Medical Laboratory Technology","Medicine, General & Internal","Medicine, Legal","Medicine, Research & Experimental","Medieval & Renaissance Studies","Metallurgy & Metallurgical Engineering","Meteorology & Atmospheric Sciences","Microbiology","Microscopy","Mineralogy","Mining & Mineral Processing","Multidisciplinary Sciences","Music","Mycology","Nanoscience & Nanotechnology","Neuroimaging","Neurosciences","Nuclear Science & Technology","Nursing","Nutrition & Dietetics","Obstetrics & Gynecology","Oceanography","Oncology","Operations Research & Management Science","Ophthalmology","Optics","Ornithology","Orthopedics","Otorhinolaryngology","Paleontology","Parasitology","Pathology","Pediatrics","Peripheral Vascular Disease","Pharmacology & Pharmacy","Philosophy","Physics, Applied","Physics, Atomic, Molecular & Chemical","Physics, Condensed Matter","Physics, Fluids & Plasmas","Physics, Mathematical","Physics, Multidisciplinary","Physics, Nuclear","Physics, Particles & Fields","Physiology","Planning & Development","Plant Sciences","Poetry","Political Science","Polymer Science","Primary Health Care","Psychiatry","Psychology","Psychology, Applied","Psychology, Biological","Psychology, Clinical","Psychology, Developmental","Psychology, Educational","Psychology, Experimental","Psychology, Mathematical","Psychology, Multidisciplinary","Psychology, Psychoanalysis","Psychology, Social","Public Administration","Public, Environmental & Occupational Health","Radiology, Nuclear Medicine & Medical Imaging","Rehabilitation","Religion","Remote Sensing","Reproductive Biology","Respiratory System","Rheumatology","Robotics","Social Issues","Social Sciences, Biomedical","Social Sciences, Interdisciplinary","Social Sciences, Mathematical Methods","Social Work","Sociology","Soil Science","Spectroscopy","Sport Sciences","Statistics & Probability","Substance Abuse","Surgery","Telecommunications","Theater","Thermodynamics","Toxicology","Transplantation","Transportation","Transportation Science & Technology","Tropical Medicine","Urban Studies","Urology & Nephrology","Veterinary Sciences","Virology","Water Resources","Women's Studies","Zoology"]



# In[ ]:
class DB:
	"""This is a class which wraps around the MySQLdb database class. 
	The only real difference here is that this DB class will try a query again if it catches an 
	operational exception from mySQL. For example, if it cannot connect to the db, it will try again"""
  conn = None

  def connect(self):
    db=mysql.connect(host="DB HOST",user="DB USER"
                ,passwd="DB PASS",db="wos2")
  def query(self, sql):
    try:
      cursor = mysql.cursors.SSCursor(self.conn)
      cursor.execute(sql)
    except (AttributeError, mysql.OperationalError):
      self.connect()
      cursor = self.conn.cursor()
      cursor.execute(sql)
    return cursor

def process(topic):
	"""Generates a percentile breakdown for a field. Percentile of raw citations vs percentage of 
	covered emails"""
	try:
	    db=DB()
	    db.connect()
	    sql="""SELECT contributors.wos_id, contributors.email_addr, contributors.display_name, contributors.cluster_id,COUNT(contributors.wos_id) FROM contributors JOIN subjects ON  contributors.wos_id=subjects.wos_id JOIN refs on refs.wos_id=subjects.wos_id WHERE subject='{}' GROUP BY contributors.cluster_id order by COUNT(refs.wos_id) DESC;""".format(mysql.escape_string(topic).decode("utf-8"))
	    print(sql)
	    cursor=db.query(sql)
	    contribs=cursor.fetchall()
	    print(len(contribs), contribs)
	    percentile_size=len(contribs)/100
	    import json
	    percentile_out={}
	    for percentile in range(99,0,-1):
	    	print("Hello")
	        total=percentile_size
	        n_1=int(percentile_size*(percentile+1))
	        n_2=int(percentile_size*(percentile))
	        percentile_contributors=contribs[n_2:n_1]
	        print(percentile_contributors)
	        percentile_emails=sum(x[1] is not None for x in percentile_contributors)
	        print(percentile_emails)
	        percentile_out[percentile]=float(float(percentile_emails)/float(total))
	    output=open("output_percentile_{}.json".format(topic),'w')
	    output.write(json.dumps(percentile_out, indent=4))
	    output.close()
	except Exception as e:
		print(e)
    

pool = multiprocessing.Pool(150)
out1 = pool.map(process, topics)

# In[ ]:




# In[ ]:



