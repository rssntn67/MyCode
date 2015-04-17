#!/bin/bash
OPENNMS_HOME="/usr/share/opennms"

URL=""
RESTURL=" -u admin:admin http://localhost:8980/opennms/rest/foreignSources/"
foreignsource="ARSINFO"
foreignid=""
ip=""

show_help () {
        cat <<END

Usage: $0 -t <target ip address(optional)> -n <foreignid> -a <ip address to add>  -d (opennms home directory default /usr/share/opennms)

This script will generate a list of $PROVISION
command to be executed to add ipaddress to foreignid
node in opennms
 
END
        exit 1
}

doAddIpSecondary() {
# 
echo $PROVISION interface add $foreignsource $foreignid $ip
echo $PROVISION interface set $foreignsource $foreignid $ip snmp-primary "S"
echo $PROVISION interface set $foreignsource $foreignid $ip descr \"provided by TN contrib script\"

echo $PROVISION service add $foreignsource $foreignid $ip ICMP
echo $PROVISION service add $foreignsource $foreignid $ip SNMP

CURL="curl -s -X POST -H \"Content-Type: application/xml\" -d \"<?xml version=\\\"1.0\\\" encoding=\\\"UTF-8\\\"?> <policy xmlns=\\\"http://xmlns.opennms.org/xsd/config/foreign-source\\\" class=\\\"org.opennms.netmgt.provision.persist.policies.MatchingIpInterfacePolicy\\\" name=\\\"Manage$ip\\\"> <parameter value=\\\"MANAGE\\\" key=\\\"action\\\"/> <parameter value=\\\"ALL_PARAMETERS\\\" key=\\\"matchBehavior\\\"/> <parameter value=\\\"~^$ip$\\\" key=\\\"ipAddress\\\"/> </policy>\""
echo $CURL $RESTURL$foreignsource/policies       
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
                 RESTURL=" -u admin:admin http://$2:8980/opennms/rest/foreignSources/"
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
doAddIpSecondary 
