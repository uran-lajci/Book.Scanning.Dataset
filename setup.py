import os
import shutil

import setuptools

import utilities


def main() -> None:
    with open('requirements.txt') as text_file:
        requirements = text_file.read().splitlines()

    version = utilities.__version__

    setuptools.setup(
        packages=setuptools.find_packages(),
        install_requires=requirements,
        python_requires='>=3.10.0',
        include_package_data=True,
        version=version,
        name='bookscanning_dataset',
    )

    egg_info_path = '../Book.Scanning.Dataset/bookscanning_dataset.egg-info'
    if os.path.exists(egg_info_path):
        shutil.rmtree(egg_info_path)


if __name__ == '__main__':
    main()
