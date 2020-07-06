import io

from setuptools import find_packages
from setuptools import setup

setup(
    name="converter",
    version="1.0.0",
    url="sbs.org",
    license="BSD",
    maintainer="Lucien",
    maintainer_email="xinyu.liu@sbs.org",
    description="Test Package",
    long_description="This is my personal project. It aims to provide a web service to convert between different music sheet format, which, in this case, MusicXML to ABCNotation.",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=["flask"],
    extras_require={"test": ["pytest", "coverage"]},
)
