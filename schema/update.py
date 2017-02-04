# This script updates the schema with new enumerations from the jurisdictions list
import json
import jsonmerge 
import collections

jur_list = ["XM","XI","XR","ZZ"]
sub_list = []


def get_codes(filename,codelist,target,array=True):

    enum = []

    with open(filename) as file:
        filedata = json.loads(file.read(),object_pairs_hook=collections.OrderedDict)
        for code in filedata[codelist]:
            enum.append(code['code'])  
    if array:
        return {"properties": {target: {"items": {"enum":enum }}}}
    else:
        return {"properties": {target: {"enum":enum }}}


jurisdiction = get_codes("codelist-jurisdictions.json","national","jurisdiction")
subnational = get_codes("codelist-jurisdictions.json","subnational","subnationalJurisdiction")
structure = get_codes("codelist-structure.json","structure","structure")
sector = get_codes("codelist-sector.json","sector","sector")
listType = get_codes("codelist-listType.json","listType","listType",False)


with open("list-schema.json") as schema_file:
    schema = json.loads(schema_file.read(),object_pairs_hook=collections.OrderedDict)

schema = jsonmerge.merge(schema,jurisdiction)
schema = jsonmerge.merge(schema,subnational)
schema = jsonmerge.merge(schema,structure)
schema = jsonmerge.merge(schema,sector)
schema = jsonmerge.merge(schema,listType)

print(json.dumps(schema,indent=4))

