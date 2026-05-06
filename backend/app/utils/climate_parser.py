def parse_climate_data(
    state: str,
    raw_data: dict
):

    parameters = raw_data["properties"]["parameter"]

    temp_data = parameters["T2M"]
    rainfall_data = parameters["PRECTOTCORR"]
    humidity_data = parameters["RH2M"]

    parsed_rows = []

    for key in temp_data.keys():

        year = int(key[:4])
        month = int(key[4:])

        # Skip annual aggregate row
        if month == 13:
            continue

        parsed_rows.append({
            "state": state,
            "year": year,
            "month": month,
            "avg_temperature": temp_data.get(key),
            "rainfall": rainfall_data.get(key),
            "humidity": humidity_data.get(key)
        })

    return parsed_rows