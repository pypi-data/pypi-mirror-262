HydroTrack - Python Framework for Tracking and Forecasting Clusters
=====================================================================
<!-- badges: start -->
[![stable](https://img.shields.io/badge/docs-stable-blue.svg)](https://hydrotrack.readthedocs.io)
[![pypi](https://badge.fury.io/py/hydrotrack.svg)](https://pypi.python.org/pypi/hydrotrack)
[![conda](https://anaconda.org/hydrotrack/hydrotrack/badges/version.svg)](https://anaconda.org/hydrotrack/hydrotrack)
[![Documentation](https://readthedocs.org/projects/hydrotrack/badge/?version=latest)](https://hydrotrack.readthedocs.io/)
[![Colab Example](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/hydrotrack-project/hydrotrack/blob/main/examples/01_Introducing_Example/01_Introducing-Hydrotrack.ipynb)
[![Downloads](https://img.shields.io/pypi/dm/hydrotrack.svg)](https://pypi.python.org/pypi/hydrotrack)
[![Contributors](https://img.shields.io/github/contributors/hydrotrack-project/hydrotrack.svg)](https://github.com/hydrotrack-project/hydrotrack/graphs/contributors)
[![License](https://img.shields.io/pypi/l/hydrotrack.svg)](https://github.com/hydrotrack-project/hydrotrack/blob/main/LICENSE)
<!-- badges: end -->

Overview
=====================================================================

`HydroTrack` is a Python package designed to identify, track and analyze hydrological phenomena with various data formats. Using time-varying 2D input frames along with user-specified threshold value parameters, HydroTrack is able to detect objects (clusters) and associate their displacement in time.

##### Algorithm Workflow

The algorithm is divided into three main modules and form the tracking workflow. 
<ol>
  <li><b>Feature detection</b>: Focuses on identifying individual clusters detection from individual frame of data and extraction of features and statistics.
  </li>
  <li><b>Spatial Operations</b>: Involves spatial operations (intersection, union, difference, etc) between objects (clusters) from consecutive time steps (t and t-1).
  <li><b>Trajectory Linking</b>: Link objects of consecutive time steps based on the spatial association.
  </li>

Documentation
=====================================================================
For a more detailed information of `hydrotrack` package please read the user guide available [click here]([https://link-url-here.org](https://github.com/hydrotrack-project/hydrotrack/blob/main/UserGuide.md)).


Installation
=====================================================================
To install the Hydrotrack package, it is highly recommended to use virtual environments such as: Anaconda3, Miniconda, Mamba, or etc.
And to download the package from githu you can do it using the command::

    git clone https://github.com/hydrotrack-project/hydrotrack/


Create environments and install the dependencies from environment.yml file::

    cd hydrotrack
    conda env create -n hydrotrack --file environment.yml
    conda activate hydrotrack

or install package from local file::

	cd hydrotrack
	pip3 install -r requirements.txt

And it is also possible to install directly from the python package repositories (pip or conda-forge)::

	pip3 install hydrotrack

 	conda install -c conda-forge hydrotrack


Example Gallery
=====================================================================
`Open In Colab <https://colab.research.google.com/github/hydrotrack-project/hydrotrack/blob/main/examples/1_Introducing-Hydrotrack.ipynb>`_.

Support and Contact
=====================================================================
For support, email helvecio.neto@inpe.br, alan.calheiros@inpe.br
