import setuptools

with open("README.md", "r", encoding="utf-8") as fhand:
    long_description = fhand.read()

setuptools.setup(
    name="aqua-man",
    version="0.0.1",
    author="Crater Kamath",
    author_email="vinayakkamath2010@gmail.com",
    description=("Simple tool to remind you to drink water "
                "during long hours in front of the screen."),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/craterkamath/aquaman",
    project_urls={
        "Bug Tracker": "https://github.com/craterkamath/aquaman/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["windows-toasts", "infi.systray", "pysimplegui", "typing", "winregistry"],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    entry_points={
        "gui_scripts" : [
            "aqman = aquaman.gui:main"
        ]
    }
)