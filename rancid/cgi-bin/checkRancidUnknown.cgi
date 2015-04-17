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
echo "Riepilogo Router di tipo unknown nel Gruppo ARSINFO"
echo
echo "Le cause piu' comuni sono: "
echo "1) errata snmp community in opennms"
echo "2) sysoid non supportato in opennms/rancid"
echo ""
$GREP ':unknown:' $ROUTER_DB | awk -F: {'print$1'} | while read unknownrouter
do SYSOID=`$CURL $NODE_REST_URL$unknownrouter 2>/dev/null | /usr/bin/xmllint --format - | grep sysObjectId | sed -e "s/<sysObjectId>//g" -e "s/<\/sysObjectId>//g"`
if [ "$SYSOID" == "" ]
then echo "unknown router $unknownrouter  - Possibile causa: community snmp errata"
fi
if [ ! "$SYSOID" == "" ]
then echo "unknown router $unknownrouter - Possibile causa: sysoid $SYSOID sconosciuto"
fi
if [ ! -f $CONFIGS_DIR/$unknownrouter ]
then echo "Error: configuration does not exists"
fi
done
# End of loop on unknown
