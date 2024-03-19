import pathlib
import setuptools


setuptools.setup(
        name="CapCokor_tiga",
        version="1.1.4",
        description="cap cokor tiga adalah minuman paling goblog di dunia",
        long_description=pathlib.Path("README.md").read_text(),
        long_description_content_type="text/markdown",
        url="https://github.com/IrfanDect/Cap_Cokor_tiga",
        author="bsbdrack",
        author_email="bsbdrack@gmail.com",
        license="MIT",
        install_requires=["baso-kontol"],
        extras_require={
            "excel": ["openpyxl"],
            },
        packages=setuptools.find_packages(),
        include_package_data=True,
        entry_points={"console_script": ["CapCokor_tiga = CapCokor_tiga.cli:main"]}
        )
