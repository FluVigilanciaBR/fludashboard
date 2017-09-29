FROM debian:testing

# RUN apt-get update && apt-get install -q -y locales python3 python3-pip python3-setuptools python3-numpy python3-pandas libpq-dev python3-gdal libgdal-dev
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

# Add and install requirements.txt before we send the code so we don't have to
# install everything again whenever any file in this directory changes (this
# helps build the container a *lot* faster by using the cache.
ADD requirements.txt /tmp/requirements.txt

RUN conda install --file /tmp/requirements.txt

# Send files to the container
ADD fludashboard /srv/deploy/fludashboard
ADD data /srv/deploy/data

WORKDIR /srv/deploy/

# Change the permissions for the user home directory
RUN chown -R deploy:deploy /srv/deploy/

EXPOSE 5000

CMD ["/srv/deploy/fludashboard/runwsgi.sh"]
