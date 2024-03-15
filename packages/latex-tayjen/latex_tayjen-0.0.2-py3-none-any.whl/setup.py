from setuptools import setup

setup(
    name = "an_example_pypi_project",
    version = "0.0.1",
    author = "Eugene Taychinov",
    author_email = "helloevgenyy@gmail.com",
    description = ("Latex creation of table and image for advanced python course"),
    license = "BSD",
    keywords = "latex image table python",
    url = "http://packages.python.org/latex_tayjen",
    packages=['latex_tayjen'],
    long_description='',
    classifiers=[
        "Development Status :: 1 - Planning",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)
