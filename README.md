# LOCKSS Installer

## Introduction

The `lockss-installer` project provides a collection of scripts to setup the alpha environment
for the LOCKSS (LOCKSS Architected As Web Services) components of the LOCKSS
software. The alpha environment consists of three main groups of components:

*   Support components. This includes a Hadoop HDFS cluster, a Solr database and
    a Postgres database. These support components run from Docker containers.

*   LAAWS components. This includes the Repository, Configuration, Metadata
    Docker instances, or from Maven JAR files which come from either Maven
    Central, Sonatype OSSRH, or a local Maven Central repository.

*   Auxiliary components. This includes Pywb replayers and a Solr-based text indexer. 
    These components run from Docker containers.

## Pre-Requisites

For all running modes:

*   Docker (Docker has [installation guides](https://docs.docker.com/install/)
    for various platforms.)
*   Docker Compose

If you have not already done so, clone this Git repository
(`git clone git@github.com:lockss/lockss-installer`) and run commands from its
top-level directory.

### Using a Demo Props Server

The LOCKSS Team maintains a demo props server with a few LOCKSS plugins and
suitable title database entries, for use with the alpha environment. To use
this demo props server, use
`--props-url=http://props.lockss.org:8001/demo/lockss.xml` as the value of
`${PROPSOPTS}` below.

## Bringing up the Alpha Test Environment

### Docker Mode

If necessary, start Docker (e.g. `sudo systemctl start docker`). Check that
Docker is running with `docker info`.

*   Bring up the Repository service and its dependencies:
    
    ```
    scripts/run-with-docker ${PROPSOPTS} --detach lockss-repository-service
    ```
*   Bring up the Configuration service:
    
    ```
    scripts/run-with-docker ${PROPSOPTS} -d lockss-configuration-service
    ```
*   Bring up one or more of the other components and their dependencies, as
    desired (optionally combined into a single command):
    
    ```
    scripts/run-with-docker ${PROPSOPTS} --detach lockss-poller-service
    scripts/run-with-docker ${PROPSOPTS} --detach lockss-metadata-extraction-service
    scripts/run-with-docker ${PROPSOPTS} --detach lockss-metadata-service
    scripts/run-with-docker ${PROPSOPTS} --detach laaws-pywb
    scripts/run-with-docker ${PROPSOPTS} --detach laaws-openwayback
    scripts/run-with-docker ${PROPSOPTS} --detach laaws-edina-indexer
 
## Using the Alpha Test Environment

### Components and Ports

Whether in Docker mode or in JAR mode, you can connect to various ports on
`localhost` to interact with components:

| Component                   | Name                               | REST port | Web UI port |
|-----------------------------|------------------------------------|-----------|-------------|
| Repository service          | lockss-repository-service          | 24610     | n/a         |
| Configuration service       | lockss-configuration-service       | 24620     | 24621       |
| Poller service              | lockss-poller                      | 24630     | 24631       | 
| Metadata Extraction service | lockss-metadata-extraction-service | 24640     | 24641       |
| Metadata service            | lockss-metadata-service            | 24650     | 24651       | 
| OpenWayback Replay          | laaws-openwayback                  | n/a       | 8000        |

For those components that have a REST port, a Swagger UI is also running under
the path `/swagger-ui.html`, e.g. `http://localhost:24621/swagger-ui.html` for
the Repository service.

The LAAWS components are running a "classic" LOCKSS Web UI at the indicated
port, with the example username/password `lockss-u`/`lockss-p`.

The OpenWayback instance can be accessed at `http://localhost:8000/wayback/`. 

### Roles

By default, the Configuration service is configured to crawl remote plugin
registries on behalf of the cluster, and to act as a JMS broker for the cluster.
(JMS is a Java component used for inter-process communication.)

Although this could be done with any component, by default the Poller service is
configured to act as a crawler (except for remote plugin registries), so it is
the component to which you would add archival units (AUs) to be collected as you
might with a "classic" standalone LOCKSS daemon.

### Suggested Progression

*   Bring up the alpha environment using the demo props server.
*   Add the following archival units (AUs) to the Poler service, by accessing
    its Web UI, clicking Journal Configuration, then Add AUs, and selecting
    the appropriate publisher groupings:

    | Publisher                      | AU name                                            | AUID                                                                                                     |
    |--------------------------------|----------------------------------------------------|----------------------------------------------------------------------------------------------------------|
    | Hindawi Publishing Corporation | Advances in Human-Computer Interaction Volume 2017 | `org\|lockss\|plugin\|hindawi\|HindawiPublishingCorporationPlugin&base_url~https%3A%2F%2Fwww%2Ehindawi%2Ecom%2F&download_url~http%3A%2F%2Fdownloads%2Ehindawi%2Ecom%2F&journal_id~ahci&volume_name~2017` |
    | Hindawi Publishing Corporation | HPB Surgery Volume 2017                            | `org\|lockss\|plugin\|hindawi\|HindawiPublishingCorporationPlugin&base_url~https%3A%2F%2Fwww%2Ehindawi%2Ecom%2F&download_url~http%3A%2F%2Fdownloads%2Ehindawi%2Ecom%2F&journal_id~hpb&volume_name~2017`  |

*   Watch them crawl by clicking Daemon Status, and selecting Crawl Status from
    the drop-down box, and refreshing periodically to see the crawls progress.
*   Check what artifacts are in the repository by performing GET operations in
    its Swagger UI. For instance,
    `GET /collections/{collectionid}/aus/{auid}/artifacts` with `demo` for the
    `{collectionid}`, and the appropriate AUID for `{auid}`, will return a JSON
    list of committed artifacts in that AU.
*   Request metadata extraction on some AUs, by connecting to the Metadata
    Extraction Service's Swagger UI, selecting the `POST /mdupdates` operation,
    and using the following input (with the appropriate AUID for `{auid}`):
    
    ```
    {
      "auid": "{auid}",
      "updateType": "full_extraction"
    }
    ```

    The result will include a job ID which you can then use in the
    `GET /mdupdates/{jobid}` operation to monitor the progress of the metadata
    extraction process. The initial status of a request is `Waiting for launch`
    and a successful operation ends with status `Success`.
*   You can then query the metadata database through the Metadata Service's
    Swagger UI. Substituting the desired AUID for `{auid}`, use the
    `GET /metadata/aus/{auid}` operation. The result is a JSON list of articles,
    as well as a section (usually at the end) with paging information. If there
    are more results, a continuation token is included, which you can input to
    reiterate the request and get more results, and so on.
*   Connect to Pywb (`http://localhost:8080` then select `demo`) or OpenWayback
    (`http://localhost:8000/wayback/`) and enter some URLs (e.g. article URLs
    returned by the metadata service). _Please note that Pywb is preferred over
    OpenWayback for its richer rendering capabilities._
    
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

## Configuration

The alpha environment is configured via the `config/` tree of files. In most
directories, a given file `foo.ext` might be accompanied by `foo.docker.ext`
and `foo.jars.ext` if there is variant configuration for Docker mode or JAR
mode. Furthermore, in many cases if there is a file `foo.txt`, you can create
a customization file `foo.opt`, that is ignored by Git. In other words, you
should not edit the `.txt` files, and instead consider them as a baseline to be
customized in `.opt` files.

The `config/conf/` directory contains top-level parameterization for the
entire alpha environment.

The `config/cluster/` directory contains configuration for the alpha LOCKSS
cluster.

The `config/host/` directory is currently empty. In an environment where the
components of the cluster are run on more than one host, there would be a
(family of) configuration files that might apply to a whole host without
applying to the whole cluster, and this `config/host/` directory is used to
illustrate this (in this case on the single host where the alpha environment
is running).

The `config/plugins/` and `config/tdbxml/` directories are used when a local
props server is in use (as opposed to the demo props server). (TODO: document
this.)

Each component also has a `config/` subdirectory where configuration information
is found.

## Support

Please contact LOCKSS Support by writing to `lockss-support (at) lockss (dot) org`
for questions and help.
