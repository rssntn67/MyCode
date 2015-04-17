#!/bin/bash

OPENNMS_HOME="/usr/share/opennms"

URL=""
foreignsource="ARSINFO"
NODES_FILE=""

show_help () {
        cat <<END

Usage: $0 -f <file.csv> -t <target ip address(optional)> -d (opennms home directory default /usr/share/opennms)

This script will generate a list of $PROVISION
command to be executed to updates node path outage into opennms
 
END
        exit 1
}

doUpdateNodes() {
   cat $NODES_FILE | while read line
   do 
      foreignid=`echo $line | cut -d';' -f1`

      if [ x"$criticalIp" != x"" ]; then 
echo $PROVISION node set $foreignsource $foreignid parent-foreign-id ''
      fi 
  done
echo  'sed -e "s/parent-foreign-id=\"\"//g"' "$OPENNMS_HOME/etc/imports/pending/$foreignsource.xml" '>' "/tmp/$foreignsource.xml"
echo  mv /tmp/$foreignsource.xml $OPENNMS_HOME/etc/imports/pending/$foreignsource.xml 

}

if [ "${1}" == "" ] ; then
   show_help
fi
while [ "${1}" != "" ] ; do

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
                 shift 2
                 ;;
 
              *) show_help
                 ;;

    esac

done

PROVISION="$OPENNMS_HOME/bin/provision.pl --password admin $URL"

if [ "$NODES_FILE" == ""  ]; then
        echo "node file not set. Exiting...."
        exit 2
fi
if [ ! -f $NODES_FILE ]; then
        echo "file '$NODES_FILE' not found. Exiting...."
        exit 2
fi
doUpdateNodes 
