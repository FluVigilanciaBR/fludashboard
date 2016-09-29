# FluDashboard Prototype

## Deployment

To deploy FluDashboard Prototype use conda package (that will create a conda environment called *fludashboard*):

```shell
conda env create -f environment.yml

```

Change to the new environment created:

```shell
source activate fludashboard

```

*<sup>Use requirements.txt from root directory of FluDashboard project.</sup>*

Optionally, the deployment can be done into a docker container. To create a new container with conda environment:

```shell
docker pull continuumio/anaconda3

```

## Running the app

To run the app just type in the terminal (in prototype directory):

```shell
python app.py

```

The application will be available on the port 5000. To set a custom port, use -p argument with the port number:

```shell
python app.py -p 9000

```
