from setuptools import setup, find_packages
setup(
    name="autilsyyj",
    version="0.1.4",
    packages=find_packages(),
    install_requires=["os","imutils","json","uuid","cv2",
        "numpy","shutil","tqdm","random","tabulate", "shapely",
        "pillow","scikit-learn"],
    author="admon",
    author_email="admon@gmail.com",
    description="A brief utils of scripts"
)