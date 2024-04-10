import json
from pathlib import Path


def get_files_data(file1: Path, file2: Path):
    with open(file1, 'r') as file1, open(file2, 'r') as file2:
        data1, data2 = json.load(file1), json.load(file2)
    return data1, data2


def generate_diff(file1: Path, file2: Path):
    result = []
    data1, data2 = get_files_data(file1, file2)
    inter_keys = set(data1) & set(data2)
    union_keys = sorted(list(set(data1) | set(data2)))
    diff1, diff2 = list(set(data1) - set(data2)),  list(set(data2) - set(data1))
    i = 0
    while i < len(union_keys):
        key = union_keys[i]
        if key in data1 and (key not in inter_keys and key not in diff2):
            result.append(f' - {key}: {data1[key]}\n')
        elif key in data2 and (key not in inter_keys and key not in diff1):
            result.append(f' + {key}: {data2[key]}\n')
        elif key in inter_keys:
            if data1[key] != data2[key]:
                result.append(f' - {key}: {data1[key]}\n')
                result.append(f' + {key}: {data2[key]}\n')
            else:
                result.append(f'   {key}: {data1[key]}\n')
        i += 1
    normalized_to_str_result = '{\n' + (''.join(result)).lower() + '}'
    return normalized_to_str_result
