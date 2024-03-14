import os
import re

def short_paths_map(paths):
    short_paths_map_dict = {}
    for path in paths:
        if os.path.isfile(path) or os.path.isdir(path):
            path_parts = path.split(os.sep)
            if len(path_parts) >= 2:
                key = os.path.join(path_parts[-2], path_parts[-1])
            else:
                key = path
            short_paths_map_dict[key] = path
    return short_paths_map_dict
    
def model_path(filename, search_paths):
    filename = filename.lower().strip()
    for path in search_paths:
        for root, dirs, files in os.walk(path):
            for file in files:
                name, ext = os.path.splitext(file)
                full_filename = name + ext
                if name.lower().strip() == filename or full_filename.lower().strip() == filename:
                    return os.path.join(root, file)
    return None

def parse_air(air: str) -> tuple[int, int]:
    match = re.match(r'https?://(?:www\.)?civitai\.com/models/([0-9]+)(?:/.*)?[\?&]modelVersionId=([0-9]+)', air)
    if match is not None:
        return int(match.group(1)), int(match.group(2))

    model_id = None
    version_id = None
    
    if '@' in air:
        model_id, version_id = air.split('@')
    else:
        model_id = air
    
    model_id = int(model_id) if model_id else None
    version_id = int(version_id) if version_id else None

    return model_id, version_id