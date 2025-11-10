import glob
import os
import shutil

data = "data"
editions = os.path.join(data, "editions")
shutil.rmtree(data, ignore_errors=True)

data_path = "../wiener-rundschau-data/data"
shutil.copytree(data_path, data)
shutil.rmtree(editions, ignore_errors=True)
os.makedirs(editions, exist_ok=True)


files = glob.glob("../wiener-rundschau-data/data/editions/*/*.xml")
for x in files:
    target_path = os.path.join(editions, os.path.basename(x))
    shutil.copy2(x, target_path)
