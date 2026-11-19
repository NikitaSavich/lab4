def find_unique(items):
    result = []
    for item in items:
        if items.count(item) == 1:
            result.append(item)
    return result