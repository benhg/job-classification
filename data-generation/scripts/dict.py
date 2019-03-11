 """De-duplicates coverage dictionaries. This needed to exist because of an 
unfortunate error where multiple copies of the coverage dictionary were copied 
to the same file"""
import json
coverage2={}
d=json.loads(open("output_field.json").read())
for key, value in d.items():
    if key not in coverage2.keys():
        coverage2[key] = value

file=open("out1.json","w")
file.write(json.dumps(coverage2, indent=4))
file.close()
