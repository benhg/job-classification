"""Multithreaded version of field_new.py, which runs sql queries in parallel.
Because most time spent on sql queries is spent waiting, we can acheive a massive
improvement on wall-clock time by simply running queries in parallel"""
# coding: utf-8

# In[1]:
import json
import MySQLdb as mysql
import multiprocessing
# db=mysql.connect(host="DB HOST",user="DB USER"
#                ,passwd="DB PASS",db="wos2")


# In[ ]:

# cursor = mysql.cursors.SSCursor(db)
# cursor.execute("""SELECT DISTINCT subject FROM contributors JOIN subjects ON subjects.wos_id=contributors.wos_id""")


# In[3]:
#
topics=["Oncology","Clinical Neurology","Communication","Computer Science, Artificial Intelligence","Computer Science, Cybernetics","Computer Science, Hardware & Architecture","Computer Science, Information Systems","Computer Science, Interdisciplinary Applications","Computer Science, Software Engineering","Computer Science, Theory & Methods","Construction & Building Technology","Criminology & Penology","Critical Care Medicine","Crystallography","Cultural Studies","Dance","Demography","Dentistry, Oral Surgery & Medicine","Dermatology","Developmental Biology","Ecology","Economics","Education & Educational Research","Education, Scientific Disciplines","Education, Special","Electrochemistry","Emergency Medicine","Endocrinology & Metabolism","Energy & Fuels","Engineering, Aerospace","Engineering, Biomedical","Engineering, Chemical","Engineering, Civil","Engineering, Electrical & Electronic","Engineering, Environmental","Engineering, Geological","Engineering, Industrial","Engineering, Manufacturing","Engineering, Marine","Engineering, Mechanical","Engineering, Multidisciplinary","Engineering, Ocean","Engineering, Petroleum","Entomology","Environmental Sciences","Environmental Studies","Ergonomics","Ethics","Ethnic Studies","Evolutionary Biology","Family Studies","Film, Radio, Television","Fisheries","Folklore","Food Science & Technology","Forestry","Gastroenterology & Hepatology","Genetics & Heredity","Geochemistry & Geophysics","Geography, Physical","Geology","Geosciences, Multidisciplinary","Geriatrics & Gerontology","Gerontology","Green & Sustainable Science & Technology","Health Care Sciences & Services","Health Policy & Services","Hematology","History","History & Philosophy of Science","History of Social Sciences","Horticulture","Hospitality, Leisure, Sport & Tourism","Humanities, Multidisciplinary","Imaging Science & Photographic Technology","Immunology","Industrial Relations & Labor","Infectious Diseases","Information Science & Library Science","Instruments & Instrumentation","Integrative & Complementary Medicine","International Relations","Language & Linguistics","Law","Limnology","Linguistics","Literary Reviews","Literary Theory & Criticism","Literature","Literature, African, Australian, Canadian","Literature, American","Literature, British Isles","Literature, German, Dutch, Scandinavian","Literature, Romance","Literature, Slavic","Logic","Management","Marine & Freshwater Biology","Materials Science, Biomaterials","Materials Science, Ceramics","Materials Science, Characterization & Testing","Materials Science, Coatings & Films","Materials Science, Composites","Materials Science, Multidisciplinary","Materials Science, Paper & Wood","Materials Science, Textiles","Mathematical & Computational Biology","Mathematics","Mathematics, Applied","Mathematics, Interdisciplinary Applications","Mechanics","Medical Ethics","Medical Informatics","Medical Laboratory Technology","Medicine, General & Internal","Medicine, Legal","Medicine, Research & Experimental","Medieval & Renaissance Studies","Metallurgy & Metallurgical Engineering","Meteorology & Atmospheric Sciences","Microbiology","Microscopy","Mineralogy","Mining & Mineral Processing","Multidisciplinary Sciences","Music","Mycology","Nanoscience & Nanotechnology","Neuroimaging","Neurosciences","Nuclear Science & Technology","Nursing","Nutrition & Dietetics","Obstetrics & Gynecology","Oceanography","Oncology","Operations Research & Management Science","Ophthalmology","Optics","Ornithology","Orthopedics","Otorhinolaryngology","Paleontology","Parasitology","Pathology","Pediatrics","Peripheral Vascular Disease","Pharmacology & Pharmacy","Philosophy","Physics, Applied","Physics, Atomic, Molecular & Chemical","Physics, Condensed Matter","Physics, Fluids & Plasmas","Physics, Mathematical","Physics, Multidisciplinary","Physics, Nuclear","Physics, Particles & Fields","Physiology","Planning & Development","Plant Sciences","Poetry","Political Science","Polymer Science","Primary Health Care","Psychiatry","Psychology","Psychology, Applied","Psychology, Biological","Psychology, Clinical","Psychology, Developmental","Psychology, Educational","Psychology, Experimental","Psychology, Mathematical","Psychology, Multidisciplinary","Psychology, Psychoanalysis","Psychology, Social","Public Administration","Public, Environmental & Occupational Health","Radiology, Nuclear Medicine & Medical Imaging","Rehabilitation","Religion","Remote Sensing","Reproductive Biology","Respiratory System","Rheumatology","Robotics","Social Issues","Social Sciences, Biomedical","Social Sciences, Interdisciplinary","Social Sciences, Mathematical Methods","Social Work","Sociology","Soil Science","Spectroscopy","Sport Sciences","Statistics & Probability","Substance Abuse","Surgery","Telecommunications","Theater","Thermodynamics","Toxicology","Transplantation","Transportation","Transportation Science & Technology","Tropical Medicine","Urban Studies","Urology & Nephrology","Veterinary Sciences","Virology","Women's Studies","Zoology"]

# In[5]:
coverage={}

coverage2={}
for key, value in coverage.items():
    if key not in coverage2.keys():
        coverage2[key] = value
#print coverage2

# In[6]:

def calc_stuff(topic):
    try:
        db2=mysql.connect(host="DB HOST",user="DB USER"
                ,passwd="DB PASS",db="wos2")
        sql="""SELECT email_addr FROM subjects JOIN contributors ON subjects.wos_id=contributors.wos_id WHERE subject='{}'""".format(mysql.escape_string(topic).decode("utf-8"))
        cursor2=db2.cursor(mysql.cursors.SSCursor)
        print(sql)
        cursor2.execute(sql)
        topic_contributors=cursor2.fetchall()
        topic_contributors=[ "%s" % x for x in topic_contributors ]
        total=len(topic_contributors)
        emails=sum(x != 'None' for x in topic_contributors)
        topicCoverage=float(float(emails)/float(total))
        coverage[topic] = (total, topicCoverage)
        temp=open("out.json","a")
        temp.write(json.dumps(coverage, indent=4))
        temp.close()
    # if not topic:
    #     break
    except Exception as e:
        print(e)
        print("Errored on {}".format(topic))


pool = multiprocessing.Pool(4)
out1 = pool.map(calc_stuff, topics)



# In[7]:

#print(topic_contributors)


# In[8]:

print(coverage)
print (len(coverage))


# In[9]:

output=open("output_field.json",'w')
output.write(json.dumps(coverage, indent=4))


# In[10]:

output.close()


# In[ ]:



