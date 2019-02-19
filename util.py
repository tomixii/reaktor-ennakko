from flask import jsonify
#-------UTIL FUNCTIONS---------
def parse_country(country_data):
    name = ''
    year = ''
    value = 0
    for field in country_data.findall('field'):
        if field.attrib['name'] == 'Country or Area':
            name = field.text.lower()
        elif field.attrib['name'] == 'Year':
            year = field.text
        elif field.attrib['name'] == 'Value' and field.text is not None:
            value = field.text
    return name, year, value

def create_response(country_data, country, year):
    if country_data is not None:
        data_value = country_data.get(year)
        if data_value is not None and data_value > 0:
            response = {
                'country': country,
                'year': year,
                'value': str(data_value)
            }
            return jsonify(response)
    return jsonify({'value': '-1'})
