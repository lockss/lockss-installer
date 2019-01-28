FROM httpd:latest

MAINTAINER "Daniel Vargas" <dlvargas@stanford.edu>

# Install Python 3.x and modules
RUN apt-get update && apt-get -y install python3 python3-requests python3-pip wget
RUN pip3 install warcio connexion

# Clean up
RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Add static httpd documents
ADD htdocs htdocs
RUN mkdir htdocs/warcs
RUN chown daemon:daemon htdocs/warcs

# Add CGI scripts
RUN rm -rf cgi-bin
ADD cgi-bin cgi-bin

# Add directory for CGI script errors
RUN mkdir logs/cgitb
RUN chown daemon:daemon logs/cgitb

# Add WASAPI server
ADD wasapi wasapi

# Add Apache configuration files
ADD conf/httpd.local.conf conf
RUN echo "include conf/httpd.local.conf" >> conf/httpd.conf
