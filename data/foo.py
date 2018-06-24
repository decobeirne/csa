bar = {
"title": "Cloughjordan Community Farm",

"image": "/images/profile/profile-cloughjordan.jpg",

"desc": ["Community Supported Farms improve the quality and quantity of food available locally while reducing the environmental impact of producing this food. Our farm is co-owned by the members. Members pay a regular contribution to cover administration, running costs and wages of our growers. In return we all receive a regular supply of farm fresh vegetables in season, delivered 3 times a week to a central collection point. We also arrange regular farm walks, as well as training and educational events. If you can collect your produce in Cloughjordan, you’re eligible to be a member – it's as simple as that! Our pricing structure means being a member and sharing all this quality produce is affordable for everyone.",
       "The farmers are Pat Malone and Kevin Dudley, helped by woofers. Pat Malone graduated from Horticulture College in 1989 and began his own commercial enterprise as a conventional vegetable grower. After ten years it was clear to him that this way of farming was too hard on the land and intense on the soul. He took a career break and spent six years working with Irish Seeds Savers Association as a researcher and collector of heritage fruit trees, mainly apples. There he deepened his love and understanding of the natural rhythms and cycles of nature. He also developed a passion and fascination with the world of Bio Dynamics and later with horses. He moved to Cloughjordan in 2007 and was instrumental in setting up the community farm. Then, having completed his own house build in the ecovillage he took over as field scale vegetable farmer in 2011."],

"info": {"Website": "cloughjordancommunityfarm.ie",
       "Email": "info@cloughjordancommunityfarm.ie",
       "Address": ["Cloughjordan Community Farm,", "The Eco Village,", "Cloughjordan,", "County Tipperary"],
       "CSA pickup location": "Cloughjordan Eco Village",
       "Farmers": "Pat Malone and Kevin Dudley",
       "Contact phone": "087 7910149"
       }
}
import time

import json
json_path = "cloughjordan.json"

t0 = time.time()
data = json.load(open(json_path, 'r'))
t1 = time.time()
print(t1 - t0)

import pdb; pdb.set_trace()

t0 = time.time()
json.dump(data, open(json_path, 'w'))
t1 = time.time()
print(t1 - t0)



import pickle

pickle_path = "cloughjordan.p"


t0 = time.time()
data2 = pickle.load(open(pickle_path, 'rb'))
t1 = time.time()
print(t1 - t0)

t0 = time.time()
pickle.dump(bar, open(pickle_path, 'wb'))
t1 = time.time()
print(t1 - t0)


