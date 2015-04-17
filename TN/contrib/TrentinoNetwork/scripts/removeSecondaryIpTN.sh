#!/bin/bash
OPENNMS_HOME="/usr/share/opennms"

URL=""
RESTURL=" -u admin:admin http://localhost:8980/opennms/rest/foreignSources/policies/Manage"
foreignsource="ARSINFO"
foreignid=""
ip=""

show_help () {
        cat <<END

Usage: $0 -t <target ip address(optional)> -n <foreignid> -a <ip address to add>  -d (opennms home directory default /usr/share/opennms)

This script will generate a list of $PROVISION
command to be executed to remove ipaddress to foreignid
node in opennms
 
END
        exit 1
}

doRemoveIpSecondary() {
# 
echo $PROVISION interface remove $foreignsource $foreignid $ip
echo "curl -X DELETE -H \"Content-Type: application/xml\" $RESTURL$ip"
}

if [ "${1}" == "" ] ; then
   show_help
fi
while [ "${1}" != "" ] ; do

   case "${1}" in

           "-n") if [ "${2}" == "" ] ; then show_help; fi
                 foreignid=$2
                 shift 2
                 ;;

           "-a") if [ "${2}" == "" ] ; then show_help; fi
                 ip=$2
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

done

PROVISION="$OPENNMS_HOME/bin/provision.pl $URL"

if [ "$foreignid" == "" ]; then
	echo "foreign id not set. Exiting...."
	exit 2
fi
if [ "$ip" == "" ]; then
	echo "ip address not set. Exiting...."
	exit 2
fi
doRemoveIpSecondary 
