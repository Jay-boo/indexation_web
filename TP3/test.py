dict_1={"id":1,"score":50}
dict_2={"id":2,"score":30}
dict_3={"id":3,"score":40}

dicts=[dict_2,dict_1,dict_3]
dicts.sort(key=lambda doc: doc["score"])
print(dicts)
