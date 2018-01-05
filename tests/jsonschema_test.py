import os
import json
import glob
from collections import OrderedDict
import unittest
import pytest
from jsonschema import Draft4Validator


current_dir = os.path.dirname(os.path.realpath(__file__))

codes_dir = os.path.join(current_dir, '../lists')
org_id_lists = []
for org_id_list_file in glob.glob(codes_dir + '/*/*.json'):
    with open(org_id_list_file) as org_id_list:
        data = json.load(org_id_list, object_pairs_hook=OrderedDict)
        org_id_lists.append((data['code'], data))


with open(os.path.join(current_dir, '../schema/list-schema.json')) as list_schema_file:
    list_schema = json.load(list_schema_file)

keep_properties = ["code", "description", "name"]

for key, value in list(list_schema['properties'].items()):
    if key not in keep_properties:
        list_schema['properties'].pop(key)

list_schema['properties']['description']['properties']['en']['minLength'] = 10
list_schema['properties']['description']['properties']['en']['type'] = ['string', 'null']


@pytest.mark.parametrize("list_name,list_data", org_id_lists)
def test_valid(list_name,list_data):
    validator = Draft4Validator(list_schema)
    errors = []

    for error in validator.iter_errors(list_data):
        errors.append("{} at {}".format(error.message, "/".join(error.path)))

    assert errors == []




if __name__ == '__main__':
    unittest.main()
