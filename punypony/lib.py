import json
import os


def mapping_write(path, data):
    with open(path, 'w') as f:
        f.write(json.dumps(data))


def mapping_read(path):
    if not os.path.exists(path):
        with open(path, 'w') as f:
            f.write('{}')

    with open(path, 'r') as f:
        content = f.read()
    return json.loads(content)
