from setuptools import setup, find_packages

def parse_requirements(file_path):
    with open(file_path, 'r') as f:
        return [line.strip() for line in f if line.strip()]
requirements_file = 'requirements.txt'
install_requires = parse_requirements(requirements_file)

setup(
    name='cv2_jewellery',
    version='0.1',
    packages=find_packages(),
    description='Package for overlaying jewellery on webcam feed',
    author='Dipenkumar ',
    install_requires=install_requires,
)