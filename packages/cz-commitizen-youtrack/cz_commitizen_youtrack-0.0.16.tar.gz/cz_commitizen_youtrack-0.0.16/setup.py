import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cz_commitizen_youtrack",
    version="0.0.16",
    author='Nigel George',
    author_email='nigel.george@shiroikuma.co.uk',
    url='https://github.com/CanisHelix/cz-youtrack',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    license="MIT",
    long_description="A variation of conventional commits with YouTrack Tasks.",
    entry_points={
        "commitizen.plugin": [
            "cz_commitizen_youtrack = cz_commitizen_youtrack:ConventionalYouTrackCz"
        ]
    },
    install_requires=["commitizen"],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
)