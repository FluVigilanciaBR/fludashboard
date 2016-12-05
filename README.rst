============
fludashboard
============

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

Flu Dashboard is an initiative to monitor and provide alert levels for Severe Acute Respiratory Infections (SARI)
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

=============
Functionality
=============

FluDashboard presents activity levels and incidence information time series by epidemiological week as well as by
epidemiological season.
Those two can be accessed by the **"Detalhado (semana)" (i.e, detailed)** and the **"Resumido (ano)" (i.e, summary)** view. Each view is composed by 4 panels:

- Country map
- Incidence chart
- Incidence table
- Age and gender distribution

In each, information can be displayed by State or by Region.

Detalhado (weekly activity information) view:
---------------------------------------------

- Country map (upper left)

 Each State/Region is colored according to selected week activity level:

 - Low activity (green): incidence below epidemic threshold;
 - Epidemic activity (yellow): incidence above epidemic threshold and below high incidence threshold;
 - High activity (orange): incidence above high and below very high incidence threshold;
 - Very high activity (red): incidence above very high incidence threshold.

- Incidence chart (upper right)

 This panel presents the reported incidence time series (black solid line) for the corresponding season, with an horizontal marker indicating the selected epidemiological week. Incidence is reported per 100 thousand individuals. Incidence estimation, when possible, is shown as a red solid line along with 95% confidence interval as dotted red lines. The activity level probability is also presented as text on the upper left corner. Map color correspond to activity level with highest probability. Along with reported and estimated incidence, the system presents the following activity thresholds, estimated based on historical activity at each State/Region:
  
 - Pre-epidemic threshold (blue dashed line): activity level which indicates, when crossed, the beginning of sustained  transmission for the current season. After crossing this threshold, incidence is expected to present steady  increase (subject to fluctuations);
 - High activity threshold (green dashed line): activity level above which incidence is considered high for that location. Calculated based on the estimated 90 percentile of historical activity distribution.
 - Very high activity threshold (red dashed line): activity level above which incidence is considered high for that region. Calculated based on the estimated 97.5 percentile of historical activity distribution.

- Incidence chart background color scheme

 The background color of the incidence time series represent the typical activity level per week. That is, the historical incidence distribution per week. It allows for identification of typical seasonal pattern, making easier to identify the period of higher activity (epidemic period).

 - Weekly low activity (green shade): activity below the 10% percentile in each week;
 - Weekly low to average activity (yellow shade): activity between the 10% and 50% percentiles in each week;
 - Weekly average to high activity (oragne shade): activity between the 50% and 90% percentile in each week;
 - Weekly high activity (red shade): activity above 90% percentile in each week.

 When the incidence in a given week is within the high activity region (red background), even if below the incidence thresholds, it indicates that for that particular week the incidence is unusually high. This information is useful for detecting seasons where the epidemic period starts earlier than usual, for instance. Check activity for season 2016 for example.

- Incidence table (lower left)

 Incidence for the corresponding State/Region at selected epidemiological week, along with 90% confidence interval when based on estimation. Along with the name of the State/Region and incidence, this table also presents selected data current status:

 - Stable: reported data is considered to be sufficiently close to total number of notifications. Reported values are expected to suffer minor updates in the future, if any;
 - Estimated: reported data is based on estimation of the digitization opportunity. That is, based on the number of notifications already entered in the system (incomplete) and typical delay between notification at health unit and digitization in the system. Reported values are expected to change in the future, becoming stable after a few weeks;
 - Incomplete: reported data is not yet stable due to digitization opportunity pattern in the selected State/Region and our system is not able to provide reliable estimates. Data is subject to significant changes in the future, becoming stable after a few weeks.

- Age and gender distribution

 Reported incidence (without estimation) bar chart by gender and age bracket.

 - Females (blue);
 - Males (orange);
 - Total population (green).

 Distributions are subject to future updates as described in the incidence table. Distribution in this panel does not use estimations, being always the currently reported distribution, either stable or incomplete.

Resumido (seasonal activity) view:
----------------------------------

This view uses detailed activity levels to report the seasonal one.

- Country map (upper left)

 Each State/Region is colored according to selected week activity level:

 - Low activity (green): incidence below epidemic threshold during the whole season
 - Epidemic activity (yellow): incidence has crossed the epidemic threshold at least once, but never crossed high incidence threshold;
 - High activity (orange): weekly incidence has been reported above high or very high incidence threshold between 1 to 4 weeks;
 - Very high activity (red): weekly incidence has been reported above high or very high incidence threshold for 5 weeks or more.

- Incidence chart (upper right)

 This panel presents the reported incidence time series (black solid line) for the corresponding season. Incidence is reported per 100 thousand individuals. Incidence estimation, when possible, is shown as a red solid line along with 95% confidence interval as dotted red lines. The activity level probability is also presented as text on the upper left corner. Map color correspond to activity level with highest probability. Along with reported and estimated incidence, the system presents the following activity thresholds, estimated based on historical activity at each State/Region:

 - Pre-epidemic threshold (blue dashed line): activity level which indicates, when crossed, the beginning of sustained transmission for the current season. After crossing this threshold, incidence is expected to present steady increase (subject to fluctuations);
 - High activity threshold (green dashed line): activity level above which incidence is considered high for that location. Calculated based on the estimated 90 percentile of historical activity distribution.
 - Very high activity threshold (red dashed line): activity level above which incidence is considered high for that region. Calculated based on the estimated 97.5 percentile of historical activity distribution.

- Incidence table (lower left)

 Incidence for the corresponding State/Region for selected season up to latest report. Along with the name of the State/Region and incidence, this table also presents selected data current status:

 - Stable: reported data is considered to be sufficiently close to total number of notifications. Reported values are expected to suffer minor updates in the future, if any;
 - Incomplete: reported data is not yet stable due to digitization opportunity pattern in the selected State/Region. Data is subject to significant changes in the future, becoming stable after a few weeks.

- Age and gender distribution

 Reported incidence bar chart by gender and age bracket for the selected season.

 - Females (blue);
 - Males (orange);
 - Total population (green).

 Distributions are subject to future updates as described in the incidence table. Distribution in this panel does not use estimations, being always the currently reported distribution, either stable or incomplete.
