# vfs/search.py


def search_by_name(folder, name):
    results = []
    if name in folder.files:
        results.append(f"File: {name}")
    for fname, fobj in folder.files.items():
        if name in fname:
            results.append(f"File: {fname}")
    for dname, dobj in folder.folders.items():
        if name in dname:
            results.append(f"Folder: {dname}")
        results += search_by_name(dobj, name)
    return results


def search_by_content(folder, text):
    results = []
    for fname, fobj in folder.files.items():
        if text in fobj.content:
            results.append(f"File: {fname}")
    for dname, dobj in folder.folders.items():
        results += search_by_content(dobj, text)
    return results
