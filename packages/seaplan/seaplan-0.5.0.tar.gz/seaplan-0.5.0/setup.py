import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

version = {}
with open("seaplan/version.py") as fp:
    exec(fp.read(), version)

setuptools.setup(
    name="seaplan",
    version=version['__version__'],
    author="Wayne Crawford",
    author_email="crawford@ipgp.fr",
    description="Sea-going mission planning",
    long_description=long_description,
    long_description_content_type="text/markdown; charset=UTF-8",
    url="https://github.com/WayneCrawford/seaplan",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
          'scipy>=1.6.3',
          'pyproj>=3.1.0',
          'shapely>=1.7',
          'pyshp>=2.1',
          'matplotlib>=3.4',
          'fiona>=1.9.6',
          'cartopy>=0.22',
          'pyyaml>=3.0',
          'xarray>=v2022.03.0',
          'jsonschema>=3.2',
          'docutils>=0.20',
          'jsonref>=1.0'
      ],
    entry_points={
         'console_scripts': [
             'seaplan=seaplan.sea_plan:main',
             'seaplan-validate=seaplan.validate_json:_console_script'
         ]
    },
    python_requires='>=3.9',
    classifiers=(
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Physics"
    ),
    keywords='oceanography, marine, OBS'
)
