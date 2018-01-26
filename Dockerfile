FROM debian:testing

RUN apt-get update && apt-get install -q -y locales wget bzip2

# Set locale
RUN echo "pt_BR.UTF-8 UTF-8" > /etc/locale.gen
RUN locale-gen pt_BR.UTF-8
RUN update-locale pt_BR.UTF-8
ENV LC_ALL pt_BR.UTF-8

# Create deploy user
RUN useradd --shell=/bin/bash --home=/srv/deploy/ --create-home deploy

# install miniconda
RUN wget -O Miniconda.sh http://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh

RUN bash Miniconda.sh -b -p /opt/miniconda && \
    rm Miniconda.sh

ENV PATH="/opt/miniconda/bin:${PATH}"

# config conda
RUN conda config --set show_channel_urls True && \
    conda update --yes --all && \
    conda clean --tarballs --packages && \
    conda config --add channels conda-forge

RUN conda install fludashboard

EXPOSE 8000

# copy ~/.flu.yaml to current dir before build
ADD .flu.yaml /root/.flu.yaml

RUN python -m fludashboard.libs.migration
RUN conda install gunicorn -y
RUN python -m fludashboard.runwsgi
