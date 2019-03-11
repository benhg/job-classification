import networkx as nx
import matplotlib.pyplot as plt
from networkx.readwrite import json_graph
import json

"""This file will generate graphs of the WoS database. Input file is a json file in the structure
{
    {"Field":[
        count, percentage, correlation
    ]},
    {"Field2":[
        count, percentage, correlation
    ]}
}
"""

data=json.loads(open("output_fields.json").read())

G=nx.Graph()
"""Generate a graph as a list of links between nodes. Networkx only supports integer indexed
nodes, so we need to keep a separate dictionary of labels"""
tuple_list=[]
tuple_list.extend([(1,2),(1,3),(1,4),(1,5),(1,6)])
labels={}

 """Define all of the categorical label names. Categories were found on 
 https://images.webofknowledge.com/WOKRS56B4/help/WOS/hp_subject_area_terms_easca.html
 Items in these lists will have subfields and will not be labelled."""

#Headings
labels[1]=r''
labels[2]=r'Life Sciences & Biomedicine'
labels[3]=r'Physical Sciences'
labels[4]=r'Technology'
labels[5]=r'Arts & Humanities'
labels[6]=r'Social Sciences'

#Subheadings
lifesci=['Ornithology',"Medicine",'Horticulture',"Biology","Marine & Freshwater Biology","Genetics & Heredity","Agriculture","Allergy","Anatomy & Morphology","Anesthesiology","Anthropology","Behavioral Sciences","Biodiversity & Conservation","Biophysics","Biotechnology & Applied Microbiology","Cell Biology","Developmental Biology","Environmental Sciences & Ecology","Evolutionary Biology","Fisheries","Food Science & Technology","Forestry","Gastroenterology & Hepatology","Genetics & Heredity","Geriatrics & Gerontology","Health Care Sciences & Services","Marine & Freshwater Biology","Mathematical & Computational Biology","Microbiology","Mycology","Paleontology","Plant Sciences","Public, Environmental & Occupational Health","Radiology, Nuclear Medicine & Medical Imaging","Rehabilitation","Reproductive Biology","Sport Sciences","Substance Abuse","Veterinary Sciences","Zoology"]
physsci=['Geosciences, Multidisciplinary','Multidisciplinary Sciences',"Astronomy & Astrophysics","Chemistry","Crystallography","Geochemistry & Geophysics","Geology","Mathematics","Meteorology & Atmospheric Sciences","Mineralogy","Mining & Mineral Processing","Oceanography","Optics","Physical Geography","Physics","Polymer Science"]
tech=["Acoustics","Automation & Control Systems","Computer Science","Construction & Building Technology","Energy & Fuels","Engineering","Imaging Science & Photographic Technology","Information Science & Library Science","Instruments & Instrumentation","Materials Science","Mechanics","Metallurgy & Metallurgical Engineering","Microscopy","Nuclear Science & Technology","Operations Research & Management Science","Remote Sensing","Robotics","Science & Technology Other Topics","Spectroscopy","Telecommunications","Transportation"]
arthum=["Medieval & Renaissance Studies","Folklore","Architecture","Art","Humanities, Multidisciplinary","Asian Studies","Dance","Film, Radio, Television","History","History & Philosophy of Science","Literature","Music","Philosophy","Religion","Theater"]
socsci=['Education, Special','Political Science','Planning & Development','Language & Linguistics','Education, Scientific Disciplines',"Geography","Archaeology","Area Studies","Social Sciences, Biomedical","Business & Economics","Communication","Criminology & Penology","Cultural Studies","Demography","Education & Educational Research","Ethnic Studies","Family Studies","Law","International Relations","Linguistics","Social Sciences, Mathematical Methods",'Psychology, Social',"Psychology","Public Administration","Social Issues","Social Sciences Other Topics","Social Work","Sociology","Urban Studies","Women\'s Studies"]
agro=['Agronomy',"Agricultural Engineering","Agricultural Economics & Policy","Agriculture, Dairy & Animal Science","Agriculture, Multidisciplinary"]
envs=["Water Resources",'Soil Science',"Environmental Sciences","Public, Environmental & Occupational Health", "Environmental Studies","Ecology"]
genmed=['Audiology & Speech-Language Pathology','Health Policy & Services','Gerontology','Limnology',"Peripheral Vascular Disease","Oncology",'Primary Health Care',"Andrology","Medicine, Legal","Medicine, General & Internal","Integrative & Complementary Medicine","Critical Care Medicine","Emergency Medicine","Critical Care Medicine","Dentistry, Oral Surgery & Medicine","Dermatology","Emergency Medicine","Endocrinology & Metabolism","Entomology","Hematology","Immunology","Infectious Diseases","Integrative & Complementary Medicine","Medical Ethics","Medical Informatics","Medical Laboratory Technology","Neurosciences & Neurology","Nursing","Nutrition & Dietetics","Obstetrics & Gynecology","Ophthalmology","Orthopedics","Otorhinolaryngology","Parasitology","Pathology","Pediatrics","Physiology","Virology","Surgery","Toxicology","Transplantation","Tropical Medicine","Urology & Nephrology","Medicine, Research & Experimental","Respiratory System","Rheumatology"]
neuro=["Neurosciences","Clinical Neurology","Neuroimaging"]
chem=['Biochemical Research Methods',"Chemistry, Medicinal","Chemistry, Inorganic & Nuclear","Chemistry, Physical","Chemistry, Organic","Electrochemistry","Chemistry, Applied","Chemistry, Organic","Chemistry, Analytical"]
phys=["Thermodynamics","Physics, Atomic, Molecular & Chemical","Physics, Nuclear","Physics, Condensed Matter","Physics, Particles & Fields","Physics, Multidisciplinary","Physics, Mathematical","Physics, Applied","Physics, Fluids & Plasmas",]
comp=["Computer Science, Hardware & Architecture","Computer Science, Information Systems","Computer Science, Software Engineering","Computer Science, Artificial Intelligence","Computer Science, Cybernetics","Computer Science, Interdisciplinary Applications","Computer Science, Theory & Methods"]
eng=["Engineering, Mechanical","Engineering, Aerospace","Engineering, Mechanical","Engineering, Ocean","Engineering, Biomedical","Engineering, Geological","Engineering, Multidisciplinary","Cell & Tissue Engineering","Engineering, Civil","Engineering, Petroleum","Engineering, Industrial","Engineering, Manufacturing","Engineering, Environmental","Engineering, Chemical","Engineering, Marine",]
matsci=['Nanoscience & Nanotechnology',"Materials Science, Coatings & Films","Materials Science, Multidisciplinary","Materials Science, Textiles","Materials Science, Characterization & Testing","Materials Science, Composites","Materials Science, Paper & Wood","Materials Science, Biomaterials","Materials Science, Ceramics"]
otop=["Nuclear Science & Technology","Food Science & Technology","Transportation Science & Technology"]
econ=['Hospitality, Leisure, Sport & Tourism','Ergonomics','Industrial Relations & Labor','Management',"Economics","Business, Finance","Business"]
socot=["Social Sciences, Interdisciplinary","History of Social Sciences","Social Sciences, Biomedical"]
lit=['Literary Theory & Criticism','Literary Reviews',"Poetry","Literature, General","Literature, American","Literature, Romance","Literature, German, Dutch, Scandinavian","Literature, Slavic","Literature, African, Australian, Canadian","Literature, British Isles",]
psych=["Psychiatry",'Psychology, Mathematical','Psychology, Multidisciplinary','Psychology, Educational','Psychology, Clinical', 'Psychology, Applied','Psychology, Experimental','Psychology, Psychoanalysis','Psychology, Biological', 'Psychology, General','Psychology, Developmental']
math=['Statistics & Probability','Mathematics, Applied',"Mathematics, General",'Mathematics, Interdisciplinary Applications']
phil=['Logic','Ethics',"Philosophy, General",]

#The first node that isn't a heading
node_num=7

#Define what subcategories should be attached to which holding categories
listOfLists=[(lifesci,2),(physsci,3),(tech,4),(arthum,5),(socsci,6),(agro,13),(envs,24),(genmed,8),(neuro,167),(chem,50),(phys,61),(comp,65),(eng,68),(matsci,72),(otop,80),(econ,108),(lit,94),(socot,124),(psych,121),(math,54),(phil,96)]


def plot_field(field_list,basenode):
    """Defines a function that takes a list of fields to be nodes, labels them, 
    and plots them as subcategories of int basenode"""
    global node_num
    for field in field_list:
    tuple_list.append((basenode,node_num))
    try:
      if field in data.keys():
        percent="%.3f"%data[field][1]
        labels[node_num]="""%s\n%s contributors\nfraction of emails covered: %s\ncorr: %s"""%(field, data[field][0],percent, data[field][2])
      else:
        labels[node_num]=field
        if field not in covered:
          print field, node_num
    except Exception as e:
      print field, node_num
    node_num+=1


def plotAll(listOfLists):
    """Plots all lists of fields in listOfLists"""
    for flist in listOfLists:
    plot_field(flist[0],flist[1])

def checkCoverage(listOfLists):
    """Runs through all fields in input file and checks to make sure they ended
    up somewhere in the graph"""
    coveredFields=[]
    for flist in listOfLists:
    coveredFields.append(flist[0])
    coveredFields=[item for sublist in coveredFields for item in sublist]
    missed=[]
    for item in data.keys():
    if item not in coveredFields:
      missed.append(item)
    print missed

def hierarchy_pos(G, root, width=2., vert_gap = 0.01, vert_loc = 0, xcenter = 0.5, 
                  pos = None, parent = None):
    '''Defines display rules for heirarcichal positioning of graph
        If there is a cycle that is reachable from root, then this will see infinite recursion.
       G: the graph
       root: the root node of current branch
       width: horizontal space allocated for this branch - avoids overlap with other branches
       vert_gap: gap between levels of hierarchy
       vert_loc: vertical location of root
       xcenter: horizontal location of root
       pos: a dict saying where all nodes go if they have been assigned
       parent: parent of this branch.'''
    if pos == None:
        pos = {root:(xcenter,vert_loc)}
    else:
        pos[root] = (xcenter, vert_loc)
    neighbors = G.neighbors(root)
    if parent != None:
        neighbors.remove(parent)
    if len(neighbors)!=0:
        dx = width/len(neighbors) 
        nextx = xcenter - width/2 - dx/2
        for neighbor in neighbors:
            nextx += dx
            pos = hierarchy_pos(G,neighbor, width = dx, vert_gap = vert_gap, 
                                vert_loc = vert_loc-vert_gap, xcenter=nextx, pos=pos, 
                                parent = root)
    return pos
def mpl_display(G,file):
    """Plots all lists and saves to a figure. Uses MatPlotLib to display
    G is a networkx graph object, and file is an outfile path."""
    plotAll(listOfLists)
    checkCoverage(listOfLists)
    G.add_edges_from(tuple_list)
    pos = hierarchy_pos(G,1)
    plt.figure(figsize=(150,150))
    nx.draw(G, pos=pos, with_labels=False)   
    nx.draw_networkx_labels(G,pos,labels,font_size=16)
    plt.savefig(file)

def json_dump(links,labels):
    """dumps network data to json
    Useful for creating javascript visualizations of graphs"""
    with open(links, 'w') as outfile1:
        outfile1.write(json.dumps(json_graph.node_link_data(G)))
    dictlist=[{"id": 1}, {"id": 2}, {"id": 3}, {"id": 4}, {"id": 5}, {"id": 6}, {"id": 7}, {"id": 8}, {"id": 9}, {"id": 10}, {"id": 11}, {"id": 12}, {"id": 13}, {"id": 14}, {"id": 15}, {"id": 16}, {"id": 17}, {"id": 18}, {"id": 19}, {"id": 20}, {"id": 21}, {"id": 22}, {"id": 23}, {"id": 24}, {"id": 25}, {"id": 26}, {"id": 27}, {"id": 28}, {"id": 29}, {"id": 30}, {"id": 31}, {"id": 32}, {"id": 33}, {"id": 34}, {"id": 35}, {"id": 36}, {"id": 37}, {"id": 38}, {"id": 39}, {"id": 40}, {"id": 41}, {"id": 42}, {"id": 43}, {"id": 44}, {"id": 45}, {"id": 46}, {"id": 47}, {"id": 48}, {"id": 49}, {"id": 50}, {"id": 51}, {"id": 52}, {"id": 53}, {"id": 54}, {"id": 55}, {"id": 56}, {"id": 57}, {"id": 58}, {"id": 59}, {"id": 60}, {"id": 61}, {"id": 62}, {"id": 63}, {"id": 64}, {"id": 65}, {"id": 66}, {"id": 67}, {"id": 68}, {"id": 69}, {"id": 70}, {"id": 71}, {"id": 72}, {"id": 73}, {"id": 74}, {"id": 75}, {"id": 76}, {"id": 77}, {"id": 78}, {"id": 79}, {"id": 80}, {"id": 81}, {"id": 82}, {"id": 83}, {"id": 84}, {"id": 85}, {"id": 86}, {"id": 87}, {"id": 88}, {"id": 89}, {"id": 90}, {"id": 91}, {"id": 92}, {"id": 93}, {"id": 94}, {"id": 95}, {"id": 96}, {"id": 97}, {"id": 98}, {"id": 99}, {"id": 100}, {"id": 101}, {"id": 102}, {"id": 103}, {"id": 104}, {"id": 105}, {"id": 106}, {"id": 107}, {"id": 108}, {"id": 109}, {"id": 110}, {"id": 111}, {"id": 112}, {"id": 113}, {"id": 114}, {"id": 115}, {"id": 116}, {"id": 117}, {"id": 118}, {"id": 119}, {"id": 120}, {"id": 121}, {"id": 122}, {"id": 123}, {"id": 124}, {"id": 125}, {"id": 126}, {"id": 127}, {"id": 128}, {"id": 129}, {"id": 130}, {"id": 131}, {"id": 132}, {"id": 133}, {"id": 134}, {"id": 135}, {"id": 136}, {"id": 137}, {"id": 138}, {"id": 139}, {"id": 140}, {"id": 141}, {"id": 142}, {"id": 143}, {"id": 144}, {"id": 145}, {"id": 146}, {"id": 147}, {"id": 148}, {"id": 149}, {"id": 150}, {"id": 151}, {"id": 152}, {"id": 153}, {"id": 154}, {"id": 155}, {"id": 156}, {"id": 157}, {"id": 158}, {"id": 159}, {"id": 160}, {"id": 161}, {"id": 162}, {"id": 163}, {"id": 164}, {"id": 165}, {"id": 166}, {"id": 167}, {"id": 168}, {"id": 169}, {"id": 170}, {"id": 171}, {"id": 172}, {"id": 173}, {"id": 174}, {"id": 175}, {"id": 176}, {"id": 177}, {"id": 178}, {"id": 179}, {"id": 180}, {"id": 181}, {"id": 182}, {"id": 183}, {"id": 184}, {"id": 185}, {"id": 186}, {"id": 187}, {"id": 188}, {"id": 189}, {"id": 190}, {"id": 191}, {"id": 192}, {"id": 193}, {"id": 194}, {"id": 195}, {"id": 196}, {"id": 197}, {"id": 198}, {"id": 199}, {"id": 200}, {"id": 201}, {"id": 202}, {"id": 203}, {"id": 204}, {"id": 205}, {"id": 206}, {"id": 207}, {"id": 208}, {"id": 209}, {"id": 210}, {"id": 211}, {"id": 212}, {"id": 213}, {"id": 214}, {"id": 215}, {"id": 216}, {"id": 217}, {"id": 218}, {"id": 219}, {"id": 220}, {"id": 221}, {"id": 222}, {"id": 223}, {"id": 224}, {"id": 225}, {"id": 226}, {"id": 227}, {"id": 228}, {"id": 229}, {"id": 230}, {"id": 231}, {"id": 232}, {"id": 233}, {"id": 234}, {"id": 235}, {"id": 236}, {"id": 237}, {"id": 238}, {"id": 239}, {"id": 240}, {"id": 241}, {"id": 242}, {"id": 243}, {"id": 244}, {"id": 245}, {"id": 246}, {"id": 247}, {"id": 248}, {"id": 249}, {"id": 250}, {"id": 251}, {"id": 252}, {"id": 253}, {"id": 254}, {"id": 255}, {"id": 256}, {"id": 257}, {"id": 258}, {"id": 259}, {"id": 260}, {"id": 261}, {"id": 262}, {"id": 263}, {"id": 264}, {"id": 265}, {"id": 266}, {"id": 267}, {"id": 268}, {"id": 269}, {"id": 270}, {"id": 271}, {"id": 272}, {"id": 273}, {"id": 274}, {"id": 275}, {"id": 276}, {"id": 277}, {"id": 278}]
    for dict in dictlist:
      dict["label"]=labels[dict["id"]]
    #vis.js is 0-indexed and networkx is 1-indexed. 
    #Took me forever to figure out why "Dance" was a subset of "Biomedical Engieering"
    for dict in dictlist:
        dict["id"]-=1
    with open(labels, 'w') as outfile1:
      outfile1.write(json.dumps(str(dictlist)))

mpl_display(G,"out.png")
json_dump("links.json","labels.json")