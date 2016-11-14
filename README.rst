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

Flu Dahsboard is an initiative to monitor and provide alert levels for Severe Acute Respiratory Infections (SARI)
notifications registered at SINAN, the Brazilian Notifiable Diseases Information System (www.saude.gov.br/sinan).
Data is provided for each Brazilian State as well as by influenza-like illnessess (ILI) regions.

This is a product of the joint work between researchers at the Scientific Computation Program at Oswaldo Cruz
Foundation (Fiocruz, PROCC), School of Applied Mathematics at Fundação Getúlio Vargas (EMAp-FGV), both from Rio de
Janeiro, Brazil, and the Inluenza Work Force at the Health Surveillance Secretariat of the Brazilian Ministry of
Health (GT-Influenza, SVS, MS).

* Free software: GNU General Public License v3
* Documentation: https://fludashboard.readthedocs.io.


Features
--------

* Nowcast of weekly incidence;
* Activity thresholds;
* Age distribution of notified cases;
* Seasonal activity level;
* Historical incidence curves.


==========
Deployment
==========

To deploy FluDashboard Prototype use conda package (that will create a conda environment called *fludashboard*):

.. highlight:: shell

.. code:: shell

    conda config --set always_yes yes --set changeps1 no

    conda config --add channels conda-forge 

    conda update --all

    conda env create -f requirements -n fludashboard


Change to the new environment created:

.. code:: shell

    source activate fludashboard


Optionally, the deployment can be done into a docker container. To create a new container with conda environment:

.. code:: shell

    docker pull continuumio/anaconda3

===============
Running the app
===============

To run the app just type in the terminal (into fludashboard/fludashboard directory):

.. code:: shell

    python app.py


The application will be available on the port 5000. To set a custom port, use -p argument with the port number:

.. code:: shell

    python app.py -p 9000


