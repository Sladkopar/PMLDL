from search import find_track_features, format_track

f = find_track_features('FUKUROU')

form = format_track(f)
for elem in form:
    print(f'{elem}:\t{form[elem]}')