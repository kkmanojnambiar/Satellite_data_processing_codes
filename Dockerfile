# syntax=docker/dockerfile:1
FROM continuumio/miniconda3:latest

COPY . /wrf_postprocessing_codes
WORKDIR /wrf_postprocessing_codes

RUN conda env create -f environment.yml

RUN echo "conda activate wrf" >> ~/.bashrc
SHELL ["/bin/bash", "--login", "-c"] 
# SHELL ["conda", "run", "-n", "wrf", "/bin/bash", "-c"]

RUN conda install -c conda-forge --file requirements.txt -y
RUN conda install -c conda-forge --file requirements_dev.txt -y

# CMD ["python", "main.py"]
ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "wrf", "python", "main.py"]