from setuptools import setup, find_packages
  
with open('requirements.txt') as f:
    requirements = f.readlines()
  
longDescription = 'Everscale/Venom rapid application development and testing tools.'
  
setup(
    name ='eversa',
    version ='0.2.0',
    author ='Anton Platonov',
    author_email ='anton@platonov.us',
    url ='https://github.com/SolderingArmor/eversa',
    description ='Everscale/Venom rapid application development and testing tools.',
    long_description = longDescription,
    long_description_content_type ="text/markdown",
    license ='MIT',
    packages = find_packages(),
    package_data={"eversa": ["README.md", ".config.json", ".config.json.example", "bin/*", "sample/*", "sample/.gitignore"]},
    entry_points ={
        'console_scripts': [
            'eversa = eversa.esa_cli:main'
        ]
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords ='ever everscale venom python package blockchain',
    install_requires = requirements,
    zip_safe = False
)