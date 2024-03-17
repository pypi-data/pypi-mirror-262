# JSONLibGem #

## What is this? ##
This module allow you to serialize and deserialize json files.

----------


# Using #


Using the library is as simple and convenient as possible:

Let's import it first:
First, import everything from the library (use the `from JSONLibGem import *` construct).

Examples:

### Serialize a JSON-formatted string into a new JSON file ###
    json_data = '{"name": "Ivan", "surname": "Ivanov", "age": 11, "can_eat_potato": false, "parts_of_body": ["Head","Potato"]}'
    output_name = "output_data.json"
    JSONLib.serialize_json(json_data, output=output_name)

### Deserialize a JSON-formatted string into a new Python object ###
    json_data = '{"name": "Ivan", "surname": "Ivanov", "age": 11, "can_eat_potato": false, "parts_of_body": ["Head","Potato"]}'
    output_name = "output_data.json"
    JSONLib.deserialize_json(json_data, output=output_name)

### Some functions of this module ###

You can print Serialized and Deserialized strings. To do this, you do not have to specify the argument "output".


    


----------
