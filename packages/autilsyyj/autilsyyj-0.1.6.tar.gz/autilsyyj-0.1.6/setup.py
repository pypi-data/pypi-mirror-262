from setuptools import setup, find_packages
setup(
    name="autilsyyj",
    version="0.1.6",
    packages=find_packages(),
    install_requires=["os","imutils","jsonpatch","uuid","opencv-python",
        "numpy","shutil","tqdm","random","tabulate", "shapely",
        "pillow","scikit-learn","jsonpointer"],
    author="admon",
    author_email="admon@gmail.com",
    description="A brief utils of scripts"
)