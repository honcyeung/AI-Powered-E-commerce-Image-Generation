# import python scripts
import generate
import edit
import load
import display

import os
import pandas as pd

DATA_PATH = "./data/FashionDataset.csv"

if __name__ == "__main__":
    df = pd.read_csv(DATA_PATH, dtype = str)
    df2 = df.copy().dropna(subset = ["Details"])
    df2["unique_id"] = df2["Details"].apply(generate.create_hash_for_image)
    df2 = df2[df2["Category"] != "Indianwear-Women"]

    for i, row in df2.iterrows():
        details = row["Details"]
        category = row["Category"]
        unique_id = row["unique_id"]

        image = generate.run_generate_pipeline(details, category, unique_id)
        if image:
            image_enhanced = edit.run_edit_pipeline(unique_id)
            display.display_images_side_by_side(unique_id)

            load.run_load_pipeline()
        else:
            print("Image generation failed.")

    df2.to_csv("./data/FashionDataset_with_id.csv", index = False)