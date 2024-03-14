from setuptools import setup,find_packages

setup(
    name='priyademo',
    version='0.1',
    packages = find_packages(),
    install_requires=[

    ],
    entry_points={
        "console_scripts":[
            "priyademo1=priyademo:hello"
        ]
    }
) 