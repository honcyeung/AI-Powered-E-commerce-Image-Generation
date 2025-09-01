# AI-Powered E-commerce Image Generation
[View the interactive workflow diagram here](https://honcyeung.github.io/AI-Powered-E-commerce-Image-Generation/)

This repository provides an automated, AI-powered solution for generating and managing e-commerce product images. By leveraging Google's powerful imagen-3.0-generate-002 model, the system streamlines the creation of high-quality product visuals from simple text descriptions, and integrates with Google Cloud services for a robust and scalable image pipeline.

## Features
- **AI-Powered Image Generation:** Automatically generates new product images based on a fashion dataset using a state-of-the-art generative AI model.
- **Automated Image Editing:** Standardizes and processes generated images, ensuring they are ready for use on an e-commerce platform.
- **Cloud Integration:** Seamlessly uploads generated and edited images to a Google Cloud Storage bucket for secure and scalable storage.
- **Data Management:** Stores product information and image metadata in Google BigQuery, providing a centralized and queryable database.
- **Modular Scripts:** The project is organized into modular Python scripts for easy management and execution of each step in the pipeline.

## Usage
The project is broken down into several scripts that can be run independently or in a sequence.
- `main.py`: The primary entry point for the application. It orchestrates the entire workflow, from loading the data to generating, editing, and uploading the images.
- `load.py`: Handles the initial data loading from data/FashionDataset.csv and prepares it for processing.
- `generate.py`: Contains the logic to interact with the Google genai API and create new images based on the data.
- `edit.py`: Implements image processing functions to standardize and prepare the images for final output.
- `display.py`: display the original and edit AI-generated images.

To run the full pipeline, execute the main script:
```python main.py```