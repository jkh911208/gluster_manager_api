def config_to_dict(data):
    temp = {}
    for line in data:
        if "=" in line:
            key_val = line.split("=")
            if len(key_val) == 2:
                temp[key_val[0].strip().replace("\"", "")] = key_val[1].strip().replace("\"", "")
    return temp
