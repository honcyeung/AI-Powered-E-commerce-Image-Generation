# import python scripts
import generate
import edit
import load

import os
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt
import io

DATA_PATH = "./data/FashionDataset.csv"
DATA_WITH_ID_PATH = "./data/FashionDataset_with_id.csv"

if __name__ == "__main__":
    df = pd.read_csv(DATA_PATH, dtype = str)
    df2 = df.copy().dropna(subset = ["Details"])
    df2["unique_id"] = df2["Details"].apply(generate.create_hash_for_image)
    test = df2.sample(1)

    for i, row in df2.iterrows():
        details = row["Details"]
        category = row["Category"]
        unique_id = row["unique_id"]
        
        print(details)
        print(category)
        print()

        image = generate.run_generate_pipeline(details, category, unique_id)
        if image:
            image_bytes_io = io.BytesIO()
            image_bytes_io.write(image.image.image_bytes)
            image_bytes_io.seek(0)
            reloaded_image = Image.open(image_bytes_io)
            plt.imshow(reloaded_image)
            plt.axis('off')
            plt.show()

            image_enhanced = edit.run_edit_pipeline(unique_id)
            image_enhanced.show()

            load.run_load_pipeline()
        else:
            print("Image generation failed.")