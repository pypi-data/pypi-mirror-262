"""
    JSON library
Version: 0.0.4
Python Version: 3

"""


class JSONLibGem:
    @staticmethod
    def deserialize_json(json_str, output=None):

        def parse_value(i):
            if i.startswith('"') and i.endswith('"'):
                return i[1:-1]
            elif i == 'true':
                return True
            elif i == 'false':
                return False
            elif '.' in i:
                return float(i)
            else:
                try:
                    return int(i)
                except:
                    return i

        def parse_json(h):
            if h.startswith('{') and h.endswith('}'):
                h = h[1:-1]
                json_pairs = h.split(', ')
                json_data = {}
                for i in json_pairs:
                    if ':' in i:
                        key, value = i.split(': ', 1)
                        json_data[key] = parse_value(value)
                return json_data
            elif h.startswith('[') and h.endswith(']'):
                h = h[1:-1]
                elements = h.split(', ')
                json_data = []
                for element in elements:
                    json_data.append(parse_value(element))
                return json_data
            else:
                return parse_value(h)

        python_object = parse_json(json_str)

        if output:
            with open(output, 'w') as file:
                file.write(str(python_object))
        else:
            print(python_object)

    @staticmethod
    def serialize_json(data, output=None):
        def generate_json(j):
            if isinstance(j, dict):
                json_str = '{'
                for key, value in j.items():
                    json_str += f'"{key}": {generate_json(value)}, '
                if len(j) > 0:
                    json_str = json_str[:-2]
                json_str += '}'
            elif isinstance(j, list):
                json_str = '['
                for item in j:
                    json_str += f'{generate_json(item)}, '
                if len(j) > 0:
                    json_str = json_str[:-2]
                json_str += ']'
            elif isinstance(j, str):
                json_str = f'{j}'
            else:
                json_str = str(j)
            return json_str

        json_data = generate_json(data)

        if output:
            with open(output, 'w') as file:
                file.write(json_data)
        else:
            print(json_data)
