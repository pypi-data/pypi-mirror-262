import os
import sys
from dotenv import dotenv_values

env_vars = dotenv_values('../.env')

parent_directory = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
src_directory = os.path.join(parent_directory, 'src')
sys.path.append(src_directory)

import infodb

url = env_vars.get('DATABASE_URL')
db="sample"
schema_name = "schema1"
schema="""
{
"title":"sample",
"description":"This is just a sample schema",
"properties":{
  "name":{
    "type":"string"
  },
  "note":{
    "type":"string"
  }
},
"required":["name"],
"primary_key":["name"],
"update_allowed":["note"]
}
"""

d1 = infodb.db(url,db,schema_name,schema)
# print(d1.schemaName)

# c= d1.insert({"name":"haha4","note":"LaLa"})
# print(c)

# d = d1.get_using_key({"name":"haha"})
# print(d)


#e = d1.get("5c7f0a37eb2047699c21d682372cea10")
#print(e)


# d1.update("5c7f0a37eb2047699c21d682372cea10",{"note":"this is the updated note. this is even more"})


q = d1.search({})
print(q)