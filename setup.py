from setuptools import setup

setup(
    name="myanswers",
    version="1.0.0",
    description="CLI tool to view and update private lab experiment answers from GitHub",
    py_modules=["myanswers"],
    entry_points={
        "console_scripts": [
            "myanswers=myanswers:main",
        ],
    },
    python_requires=">=3.7",
)
