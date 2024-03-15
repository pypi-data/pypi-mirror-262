import pathlib
import setuptools

setuptools.setup(
        name="baso_kontol",
        version="1.1.1",
        description="resep baso kontol",
        long_description=pathlib.Path("README.md").read_text(),
        long_description_content_type="text/markdown",
        url="https://github.com/IrfanDect/baso-kontol",
        author="IrfanDect",
        author_email="bsbdrack@gmail.com",
        license="MIT",
        install_requires=["rich","requests","prompt-toolkit"],
        extras_require={
            "excel": ["openpyxl"],
            },
        packages=setuptools.find_packages(),
        include_package_data=True,
        entry_points={"console_script": ["baso_kontol = baso_kontol.cli:main"]}
        )
