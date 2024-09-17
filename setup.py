from setuptools import setup, find_packages


def open_file_with_detected_encoding(file_path):
    with open(file_path, "r") as f:
        raw_data = f.read()

    return raw_data


def read_requirements():
    return open_file_with_detected_encoding("requirements.txt").splitlines()


setup(
    name="gap_analysis",
    version="1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=read_requirements(),
)
