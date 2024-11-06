import kaggle

# Authenticate with the Kaggle API
kaggle.api.authenticate()

# Download the dataset to the specified path and unzip it
kaggle.api.dataset_download_files(
    "asaniczka/data-science-job-postings-and-skills",
    path=r"C:\Users\OJarvis\OneDrive - Alvarez and Marsal\Documents\Repo\ds_skill_niche_proj\data\external",
    unzip=True,
)

# Download the dataset to the specified path and unzip it
kaggle.api.dataset_download_files(
    "andrewmvd/data-scientist-jobs",
    path=r"C:\Users\OJarvis\OneDrive - Alvarez and Marsal\Documents\Repo\ds_skill_niche_proj\data\external",
    unzip=True,
)

# Download the dataset to the specified path and unzip it
kaggle.api.dataset_download_files(
    "hummaamqaasim/jobs-in-data",
    path=r"C:\Users\OJarvis\OneDrive - Alvarez and Marsal\Documents\Repo\ds_skill_niche_proj\data\external",
    unzip=True,
)
