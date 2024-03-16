from setuptools import setup,find_packages
c=["Programming Language :: Python :: 3",
   "License :: OSI Approved :: MIT License",
   "Operating System :: OS Independent",]
d="This is fun Games Package for FLAMES Game"
setup(
    name='ARflames',
    version='1.0.0',
    author='Abdurrahim',
    author_email='ar.rahimdeve7418@gmail.com',
    description=d,
    long_description="FLAMES game of the programs"+open("README.md").read(),
    long_description_content_type='text/markdown',
    keywords=['FLAMES Game','Games','String','GUI'],
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    package_data={'': ['static/*']},
    classifiers=c,
    install_requires=['Rahimcalc','pillow'],
    url="https://pypi.org/user/ARRM03/",
    entry_points={'console_scripts':['ARflames=ARflames.Comments:comments']},
    project_urls=
    {
        'Source Code':'https://github.com/ARRahim7418/Python-Packages.git',
        'Documentation':'https://github.com/ARRahim7418/Python-Packages.git'
        }
    )
