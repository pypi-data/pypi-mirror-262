from setuptools import setup, find_packages
setup(
    name="autilsyyj",
    version="0.1.7",
    packages=find_packages(),
    install_requires=["imutils","jsonpatch","uuid","opencv-python",
        "numpy","tqdm","random","tabulate", "shapely",
        "pillow","scikit-learn","jsonpointer"],
    author="admon",
    author_email="admon@gmail.com",
    description="A brief utils of scripts"
)