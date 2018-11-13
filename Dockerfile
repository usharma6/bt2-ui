FROM rocker/shiny

RUN apt-get update && apt-get install -y python python-pip virtualenv curl less git zlib1g-dev libtbb-dev libssl-dev

RUN git clone https://github.com/BenLangmead/bowtie2 /tmp/bowtie2 \
        && cd /tmp/bowtie2 && make bowtie2-align-s BOWTIE_SHARED_MEM=1 \
        && mkdir -p /software/bowtie2 \
        && cp /tmp/bowtie2/bowtie2-align-s /tmp/bowtie2/bowtie2 /software/bowtie2

RUN Rscript -e "install.packages(c('devtools', 'dplyr', 'readr', 'shinyjs', 'rclipboard', 'processx', 'reticulate', 'shinyBS', 'digest', 'rintrojs'), repos='https://cran.rstudio.com/')" \
    && rm -rf /tmp/downloaded_packages/ /tmp/*.rds

RUN Rscript -e "install.packages('devtools'); devtools::install_github('rstudio/shinydashboard')"

RUN mkdir -p /srv/shiny-server/bt2-ui
COPY www /srv/shiny-server/bt2-ui/www
COPY MANUAL.markdown /srv/shiny-server/bt2-ui/
COPY *.R /srv/shiny-server/bt2-ui/
COPY *.py /srv/shiny-server/bt2-ui/

COPY shiny-server.conf /etc/shiny-server/shiny-server.conf

RUN R -e "rmarkdown::render('/srv/shiny-server/bt2-ui/MANUAL.markdown',output_file='/srv/shiny-server/bt2-ui/www/MANUAL.html')"
