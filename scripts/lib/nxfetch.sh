#!/bin/bash
# Argument = -h -v -i groupId:artifactId:version -c classifier -p packaging -r repository
#shopt -o -s xtrace

# Define Nexus Configuration
NEXUS_BASE=https://oss.sonatype.org
REST_PATH=/service/local
ART_REDIR=/artifact/maven/redirect
META_PATH=/artifact/maven/resolve

usage()
{
cat <<EOF

usage: $0 options

This script will fetch an artifact from a Nexus server using the Nexus REST redirect service.

OPTIONS:
   -h      Show this message
   -v      Verbose
   -q      Quiet
   -s      Verify SHA1 checksum after download
   -f      Force overwirte of file
   -i      GAV coordinate groupId:artifactId:version
   -p      Artifact Packaging
   -r      Repository (Defaults to releases, snapshots if version ends in SNAPSHOT)
   -c      Artifact Classifier (Should be used with -e)
   -e      Extension           (Should be used with -c)
   -o      Output filename

EOF
}

# Read in Complete Set of Coordinates from the Command Line
GROUP_ID=
ARTIFACT_ID=
VERSION=
CLASSIFIER=""
PACKAGING=jar
REPO=
EXT=
VERBOSE=0
QUIET=0
CHECK_SHA1=0
FORCE=0
OUTPUT_FILE=

CURL_OPTS=

while getopts "hvqsfi:p:r:c:e:o:" OPTION
do
     case $OPTION in
         h)
             usage
             exit 1
             ;;
         i)
             OIFS=$IFS
             IFS=":"
             GAV_COORD=( $OPTARG )
             GROUP_ID=${GAV_COORD[0]}
             ARTIFACT_ID=${GAV_COORD[1]}
             VERSION=${GAV_COORD[2]}
             IFS=$OIFS
             ;;
         c)
             CLASSIFIER=$OPTARG
             ;;
         p)
             PACKAGING=$OPTARG
             ;;
         e)
             EXT=$OPTARG
             ;;
         r)
             REPO=$OPTARG
             ;;
         o)
             OUTPUT_FILE=$OPTARG
             ;;
         f)
             FORCE=1
             ;;
         q)
             QUIET=1
             ;;
         v)
             VERBOSE=1
             ;;
         s)
             CHECK_SHA1=1
             ;;
         ?)
             usage
             exit
             ;;
     esac
done

if [[ -z $GROUP_ID ]] || [[ -z $ARTIFACT_ID ]] || [[ -z $VERSION ]]
then
     echo "BAD ARGUMENTS: Either groupId, artifactId, or version was not supplied" >&2
     usage
     exit 1
fi

if [ -z $OUTPUT_FILE -a $CHECK_SHA1 -eq 1 ]; then
     echo "BAD ARGUMENTS: Output filename must be in use if SHA1 is requested" >&2
     usage
     exit 1
fi

# Define default values for optional components

# If the version requested is a SNAPSHOT use snapshots, otherwise use releases
if [[ "$VERSION" =~ .*SNAPSHOT ]]
then
    : ${REPO:="snapshots"}
else
    : ${REPO:="releases"}
fi

if [ -n "$OUTPUT_FILE" ]; then
        if [ -f "$OUTPUT_FILE" -a $FORCE -ne 1 ]; then
                echo "ERROR: Output file exists and force not specified" >&2
                exit 1
        fi

        CURL_OPTS="-o $OUTPUT_FILE.$$ $CURL_OPTS"
fi

if [ $VERBOSE -eq 1 ]; then
        CURL_OPTS="-v $CURL_OPTS"
else
        CURL_OPTS="-sS $CURL_OPTS"
fi

# Construct the base URL
REDIRECT_URL=${NEXUS_BASE}${REST_PATH}${ART_REDIR}
META_URL=${NEXUS_BASE}${REST_PATH}${META_PATH}

# Generate the list of parameters
PARAM_KEYS=( g a v r p c e )
PARAM_VALUES=( $GROUP_ID $ARTIFACT_ID $VERSION $REPO $PACKAGING $CLASSIFIER $EXT )
PARAMS=""
for index in ${!PARAM_KEYS[*]}
do
  if [[ ${PARAM_VALUES[$index]} != "" ]]
  then
    PARAMS="${PARAMS}${PARAM_KEYS[$index]}=${PARAM_VALUES[$index]}&"
  fi
done

REDIRECT_URL="${REDIRECT_URL}?${PARAMS}"
META_URL="${META_URL}?${PARAMS}"

[ $QUIET -ne 1 ] && echo "Fetching Artifact from $REDIRECT_URL..." >&2
curl $CURL_OPTS -L ${REDIRECT_URL}

if [ $? -ne 0 ]; then
  echo "Error downloading artifact from nexus, try again with verbose to see details" >&2
  [ -n "$OUTPUT_FILE" ] && rm -f "$OUTPUT_FILE.$$"
  exit 1
fi

if [ $CHECK_SHA1 -eq 1 ]; then
        SHA1_NEXUS=$(curl -Ss ${META_URL} | sed -n 's!.*<sha1>\(.*\)</sha1>!\1!p')
        SHA1_FILE=$(sha1sum $OUTPUT_FILE.$$ | cut -f 1 -d\ )

        if [ "$SHA1_FILE" != "$SHA1_NEXUS" ]; then
                echo "ERROR: the SHA1 hashes do not match" >&2
                echo "File  SHA1: $SHA1_FILE" >&2
                echo "Nexus SHA1: $SHA1_NEXUS" >&2
                rm -f "$OUTPUT_FILE.$$"
                exit 1
        fi

        [ $QUIET -ne 1 ] && echo "INFO: SHA1 hashes match, download successfull" >&2
fi

[ -n "$OUTPUT_FILE" ] && mv "$OUTPUT_FILE.$$" "$OUTPUT_FILE"

exit 0