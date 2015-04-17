#!/bin/bash
OPENNMS_HOME="/usr/share/opennms"

URL=""
RESTURL=" -u admin:admin http://localhost:8980/opennms/rest/foreignSources/"
RESTURLFORDELETE=" -u admin:admin http://localhost:8980/opennms/rest/foreignSources/policies/Manage"
foreignsource="ARSINFO"
foreignid=""
oldip=""
newip=""
snmpcommunity=public
snmpversion=v2c
snmptimeout=5000

show_help () {
        cat <<END

Usage: $0 -t <target ip address(optional)> -n <foreignid> -a <ip address to add> -o <ip address to remove> 
          -c <community default 'public'> -to <timeout default 5000ms> -v <version default v2c > 
          -d (opennms home directory default /usr/share/opennms)

This script will generate a list of $PROVISION
command to be executed to manage ipaddress change
for the sepcified foreignid
node in opennms
 
END
        exit 1
}

doAddIpPrimary() {
# 
echo $PROVISION interface add $foreignsource $foreignid $newip
echo $PROVISION interface set $foreignsource $foreignid $newip snmp-primary "P"
echo $PROVISION interface set $foreignsource $foreignid $newip descr \"provided by TN contrib script\"

echo $PROVISION service add $foreignsource $foreignid $newip ICMP
echo $PROVISION service add $foreignsource $foreignid $newip SNMP

echo $PROVISION  snmp set $newip $snmpcommunity version=$snmpversion timeout=$snmptimeout

CURL="curl -s -X POST -H \"Content-Type: application/xml\" -d \"<?xml version=\\\"1.0\\\" encoding=\\\"UTF-8\\\"?> <policy xmlns=\\\"http://xmlns.opennms.org/xsd/config/foreign-source\\\" class=\\\"org.opennms.netmgt.provision.persist.policies.MatchingIpInterfacePolicy\\\" name=\\\"Manage$newip\\\"> <parameter value=\\\"MANAGE\\\" key=\\\"action\\\"/> <parameter value=\\\"ALL_PARAMETERS\\\" key=\\\"matchBehavior\\\"/> <parameter value=\\\"~^$newip$\\\" key=\\\"ipAddress\\\"/> </policy>\""
echo $CURL $RESTURL$foreignsource/policies       
}

doRemoveIp() {
#
echo $PROVISION interface remove $foreignsource $foreignid $oldip
echo "curl -X DELETE -H \"Content-Type: application/xml\" $RESTURLFORDELETE$oldip"
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
                 newip=$2
                 shift 2
                 ;;

           "-o") if [ "${2}" == "" ] ; then show_help; fi
                 oldip=$2
                 shift 2
                 ;;

           "-c") if [ "${2}" == "" ] ; then show_help; fi
                 snmpcommunity=$2
                 shift 2
                 ;;

           "-to") if [ "${2}" == "" ] ; then show_help; fi
                 snmptimeout=$2
                 shift 2
                 ;;

           "-v") if [ "${2}" == "" ] ; then show_help; fi
                 snmpversion=$2
                 shift 2
                 ;;

           "-d") if [ "${2}" == "" ] ; then show_help; fi
                 OPENNMS_HOME=$2
                 shift 2
                 ;;

           "-t") if [ "${2}" == "" ] ; then show_help; fi
                 URL="--url http://$2:8980/opennms/rest"
                 RESTURL=" -u admin:admin http://$2:8980/opennms/rest/foreignSources/"
                 RESTURLFORDELETE=" -u admin:admin http://$2:8980/opennms/rest/foreignSources/policies/Manage"
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
if [ "$newip" == "" ]; then
	echo "new ip address not set. Exiting...."
	exit 2
fi
if [ "$oldip" == "" ]; then
	echo "old ip address not set. Exiting...."
	exit 2
fi

doRemoveIp
doAddIpPrimary 
