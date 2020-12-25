import json

with open('schemas/schema.json') as file:
    all_schemas = json.load(file)
register_schema = all_schemas['register']
create_post_schema = all_schemas['create_post']
