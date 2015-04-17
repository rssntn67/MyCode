#! /bin/bash
# configuration to let the script work
BASEDIR=/var/lib/rancid/var; export BASEDIR
PATH=/var/lib/rancid/bin:/usr/bin:/usr/sbin:/bin:/usr/local/bin:/usr/bin; export PATH
CVSROOT=$BASEDIR/CVS; export CVSROOT
HOME=/var/lib/rancid; export HOME
RANCID_GROUP="ARSINFO"
RANCID_REPOSITORY=$BASEDIR'/'$RANCID_GROUP
LOG_DIR=$BASEDIR'/logs'
ROUTER_DB=$RANCID_REPOSITORY'/router.db'
CONFIGS_DIR=$RANCID_REPOSITORY'/configs'
# commands
CVS_CMD='/usr/bin/cvs'
GREP='/bin/grep'
FIND_CMD='/usr/bin/find'
# opennms REST interface access URL and command
CURL='/usr/bin/curl -X GET -H "Content-Type: application/xml" -u admin:admin '
NODE_REST_URL='opennms.arsinfo.it:8980/opennms/rest/nodes?label='
#
echo "Content-Type: text/plain"
echo
echo "Router con un download programmato della configurazione piu' vecchio di 24 giorni "
echo
$FIND_CMD $CONFIGS_DIR -mtime +23 -print | grep -v CVS | sed -e "s/\/var\/lib\/rancid\/var\/ARSINFO\/configs\///g" | while read host
do grep $host $ROUTER_DB
done
