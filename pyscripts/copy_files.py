import glob
import os
import shutil

data = "data"
editions = os.path.join(data, "editions")
indices = os.path.join(data, "indices")
meta = os.path.join(data, "meta")
listbibl = "../wiener-rundschau-data/data/indices/listbibl.xml"
about = "../wiener-rundschau-data/data/meta/about.xml"


shutil.rmtree(data)
os.makedirs(editions)
os.makedirs(indices)
os.makedirs(meta)


files = glob.glob("../wiener-rundschau-data/data/editions/*/*.xml")
for x in files:
    target_path = os.path.join(editions, os.path.basename(x))
    shutil.copy2(x, target_path)

shutil.copy2(listbibl, os.path.join(indices, "listbibl.xml"))
shutil.copy2(about, os.path.join(meta, "about.xml"))
