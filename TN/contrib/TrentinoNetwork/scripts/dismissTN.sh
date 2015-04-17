#! /bin/bash
OPENNMS_HOME="/usr/share/opennms"
RESTURL=" -u admin:admin http://localhost:8980/opennms/rest/foreignSources/policies/Manage"
FOREIGN_SOURCE="ARSIFO"
NODES_FILE=""

show_help () {
        cat <<END

Usage: $0 -t <target ip address)> -d (opennms home directory default /usr/share/opennms) -f <file with the nodes to dismiss>

This script will generate a list of 
command to be executed to dismiss 
 a nodes into opennms

END
        exit 1
}

doDismiss () {
cat $NODES_FILE | while read line
    do
    hostname=`echo $line | cut -d';' -f1`
    ip=`echo $line | cut -d';' -f2 | sed -e "s/\"//g" -e "s/ //g"`
    
    foreignid=$hostname 
    echo "$PROVISION node remove $FOREIGN_SOURCE $foreignid"
    echo "curl -X DELETE -H \"Content-Type: application/xml\" $RESTURL$ip"
    done
}

if [ "${1}" == "" ] ; then
   show_help
fi

   case "${1}" in

           "-f") if [ "${2}" == "" ] ; then show_help; fi
                 NODES_FILE=$2
                 shift 2
                 ;;

           "-d") if [ "${2}" == "" ] ; then show_help; fi
                 OPENNMS_HOME=$2
                 shift 2
                 ;;

           "-t") if [ "${2}" == "" ] ; then show_help; fi
                 URL="--url http://$2:8980/opennms/rest"
                 RESTURL=" -u admin:admin http://$2:8980/opennms/rest/foreignSources/policies/Manage"
                 shift 2
                 ;;

              *) show_help
                 ;;

    esac

PROVISION="$OPENNMS_HOME/bin/provision.pl --password admin $URL"

if [ "$NODES_FILE" == "" ]; then
        echo "node file not set. Exiting...."
        exit 2
fi
if [ ! -f $NODES_FILE ]; then
        echo "file '$NODES_FILE' not found. Exiting...."
        exit 2
fi
doDismiss
