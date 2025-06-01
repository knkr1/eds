from setuptools import setup

setup(
    name="eds",
    version="1.0.0",
    py_modules=[],
    packages=["eds"],
    entry_points={
        "console_scripts": [
            "eds=eds.__main__:main"
        ]
    },
    install_requires=["yt-dlp"],
)
