# LOCKSS Installer

## Introduction

The `lockss-installer` project provides a collection of scripts to setup the alpha environment
for the LOCKSS (LOCKSS Architected As Web Services) components of the LOCKSS
software. The alpha environment consists of three main groups of components:

*   Support components. This includes a Hadoop HDFS cluster, a Solr database and
    a Postgres database. These support components run from Docker containers.

*   LOCKSS components. This includes the Repository, Configuration, Metadata, Poller
    Docker instances.

*   Auxiliary components. This includes Pywb replayers and a Solr-based text indexer. 
    These components run from Docker containers.

## Pre-Requisites

For all running modes:

*   Docker (Docker has [installation guides](https://docs.docker.com/install/)
    for various platforms.)
*   Docker Compose
*		File System for [persistent storage](https://github.com/CWSpear/local-persist)
*		opt. Portainer <portainer.io> or similiar docker ui for managing and viewing containers.

If you have not already done so, clone this Git repository
(`git clone git@github.com:lockss/lockss-installer`) and run commands from its
top-level directory.

### Using a Props Server

## Bringing up the LOCKSS Environment

### Docker Mode

If necessary, start Docker (e.g. `sudo systemctl start docker`). Check that
Docker is running with `docker info`.

*		Determine the file system and location for the lockss cache and mount it into docker.

*   Bring up the LOCKSS Docker Componenets:
    
    ```
    scripts/run-lockss-docker
    ```

## Default Components and Ports

You can connect to various ports on the host system to interact with components:

| Component                   | Name                               | REST port | Web UI port |
|-----------------------------|------------------------------------|-----------|-------------|
| Repository service          | lockss-repository-service          | 24610     | n/a         |
| Configuration service       | lockss-configuration-service       | 24620     | 24621       |
| Poller service              | lockss-poller                      | 24630     | 24631       | 
| Metadata Extraction service | lockss-metadata-extraction-service | 24640     | 24641       |
| Metadata service            | lockss-metadata-service            | 24650     | 24651       | 
| OpenWayback Replay          | lockss-openwayback                  | n/a       | 8000        |

For those components that have a REST port, a Swagger UI is also running under
the path `/swagger-ui.html`, e.g. `http://<host>:24621/swagger-ui.html` for
the Repository service.

The LAAWS components are running a "classic" LOCKSS Web UI at the indicated
port, with the example username/password `lockss-u`/`lockss-p`.

The OpenWayback instance can be accessed at `http://<host>:8000/wayback/`. 

### Roles

By default, the Configuration service is configured to crawl remote plugin
registries on behalf of the cluster, and to act as a JMS broker for the cluster.
(JMS is a Java component used for inter-process communication.)

Although this could be done with any component, by default the Poller service is
configured to act as a crawler (except for remote plugin registries), so it is
the component to which you would add archival units (AUs) to be collected as you
might with a "classic" standalone LOCKSS daemon.

### Installation 

*   Configure the environment with config-lockss script.

### Logs

In Docker mode, the logs for the LAAWS components are found at
`logs/${component}/app.log`.

To see the Docker logging for a Docker-bound component, use this command:

```
scripts/param-docker-compose logs ${component}
```

Use `... logs --follow ...` to keep tailing the log. Use
`... logs --no-color ...` if piping the output to a command or redirecting to a
file.

## Manual Configuration

The configuration files are in the `config/` directory. In most
directories, a given file `<service>.ext` might be accompanied by `<service>.docker.ext`
configuration for Docker mode. Furthermore, in many cases if there is a file `lockss.txt`, you can modify the properties in the file `lockss.opt`, that is ignored by Git. In other words, you should not edit the `.txt` files, and instead consider them as a baseline to  customized in `.opt` files.

The `config/conf/` directory contains top-level parameterization for the
entire environment.

The `config/cluster/` directory contains configuration for the LOCKSS
cluster.

The `config/plugins/` and `config/tdbxml/` directories are used when a local
props server is in use (as opposed to the demo props server). 

Each component also has a `config/` subdirectory where configuration information
is found.

## Support

Please contact LOCKSS Support by writing to `lockss-support (at) lockss (dot) org`
for questions and help.
