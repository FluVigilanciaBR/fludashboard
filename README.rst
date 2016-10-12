===============================
fludashboard
===============================


.. image:: https://img.shields.io/pypi/v/fludashboard.svg
        :target: https://pypi.python.org/pypi/fludashboard

.. image:: https://img.shields.io/travis/FluVigilanciaBR/fludashboard.svg
        :target: https://travis-ci.org/FluVigilanciaBR/fludashboard

.. image:: https://readthedocs.org/projects/fludashboard/badge/?version=latest
        :target: https://fludashboard.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/FluVigilanciaBR/fludashboard/shield.svg
     :target: https://pyup.io/repos/github/FluVigilanciaBR/fludashboard/
     :alt: Updates


Flu Dashboard


* Free software: GNU General Public License v3
* Documentation: https://fludashboard.readthedocs.io.


Features
--------

* TODO

==========
Deployment
==========

To deploy FluDashboard Prototype use conda package (that will create a conda environment called *fludashboard*):

.. code-block:: shell
    conda config --set always_yes yes --set changeps1 no

    conda config --add channels conda-forge 

    conda update --all

    conda env create -f requirements -n fludashboard


Change to the new environment created:

.. code-block:: shell
    source activate fludashboard


Optionally, the deployment can be done into a docker container. To create a new container with conda environment:

.. code-block:: shell
    docker pull continuumio/anaconda3


## Running the app

To run the app just type in the terminal (in prototype directory):

.. code-block:: shell
    python app.py


The application will be available on the port 5000. To set a custom port, use -p argument with the port number:

.. code-block:: shell
    python app.py -p 9000

