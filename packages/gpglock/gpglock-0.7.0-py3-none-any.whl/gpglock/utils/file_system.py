import os

def get_all_non_hidden_files(dir_path) -> list[str]:    
    entities = []
    for root, dirs, filenames in os.walk(dir_path):
        filenames = [f for f in filenames if not f[0] == '.'] # Ignore hidden files
        dirs[:] = [d for d in dirs if not d[0] == '.'] # Ignore hidden dirs
        for filename in filenames:
            filepath = os.path.join(root, filename)
            entities.append(filepath)
    return entities