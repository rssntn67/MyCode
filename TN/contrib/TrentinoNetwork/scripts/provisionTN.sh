#!/bin/bash
OPENNMS_HOME="/usr/share/opennms"

URL=""
foreignsource="ARSINFO"
RESTURL=" -u admin:admin http://127.0.0.1:8980/opennms/rest/foreignSources/"
CREATE_REQUISITIONS=0
IMPORT_REQUISITIONS=0
CREATE_NODES=0
NODES_FILE=""

show_help () {
        cat <<END

Usage: $0 -f <file.csv> -t <target ip address(optional)> -r (create requisition) -i (import requisition) -n (create nodes) -d (opennms home directory default /usr/share/opennms)

This script will generate a list of $PROVISION
command to be executed to provision nodes to opennms
 
END
        exit 1
}

doCreateRequisition() {
   echo $PROVISION requisition add $foreignsource
}

doImportRequisition() {
   echo $PROVISION requisition import $foreignsource
}

doCreateNodes() {
   cat $NODES_FILE | while read line
   do 
      hostname=`echo $line | cut -d';' -f1`
      dnsdomain=`echo $line | cut -d';' -f2`
      ip=`echo $line | cut -d';' -f3 | sed -e "s/\"//g" -e "s/ //g"`
      elm_category=`echo $line | cut -d';' -f4`
      snmpcommunity=`echo $line | cut -d';' -f5 | sed -e "s/\"//g"`
      snmptimeout=`echo $line | cut -d';' -f6 | sed -e "s/\"//g"`
      snmpversion=`echo $line | cut -d';' -f7 | sed -e "s/\"//g"`
      username=`echo $line | cut -d';' -f8`
      password=`echo $line | cut -d';' -f9`
      connection=`echo $line | cut -d';' -f10`
      city=`echo $line | cut -d';' -f11`
      address=`echo $line | cut -d';' -f12`
      svc_notierror=`echo $line | cut -d';' -f13`
      svc_notithres=`echo $line | cut -d';' -f14`
      criticalIp=`echo $line | cut -d';' -f15`
      enablepass=`echo $line | cut -d';' -f16`

      nodelabel=` echo "$hostname.$dnsdomain" | sed "s/\"//g"`
      category1=`echo $elm_category | awk -F\- {'print $1'} | sed "s/\"//g"`
      category2=`echo $elm_category | awk -F\- {'print $2'} | sed "s/\"//g"`
      category3=`echo $svc_notierror | sed "s/\"//g"`
      category4=`echo $svc_notithres | sed "s/\"//g"`

      description=`echo $city - $address | sed "s/\"//g"`
      foreignid=$hostname
echo 'echo provisiong node' $nodelabel 'into requisition group' $foreignsource 'with foreign id' $foreignid
echo $PROVISION node add $foreignsource $foreignid $nodelabel
echo $PROVISION node set $foreignsource $foreignid city \"$city\"
      if [ x"$criticalIp" != x"" ]; then 
echo $PROVISION node set $foreignsource $foreignid parent-foreign-id $criticalIp
      fi 

echo $PROVISION category add $foreignsource $foreignid $category1
echo $PROVISION category add $foreignsource $foreignid $category2
      if [ x"$category3" != x"" ]
      then
echo $PROVISION category add $foreignsource $foreignid $category3
      fi 
      if [ x"$category4" != x"" ]
      then
echo $PROVISION category add $foreignsource $foreignid Threshold$category4
      fi 

# Location and description 
echo $PROVISION asset add $foreignsource $foreignid address1 \"$address\"
echo $PROVISION asset add $foreignsource $foreignid description \"$description\"

# Connection information for rancid
echo $PROVISION asset add $foreignsource $foreignid username $username
echo $PROVISION asset add $foreignsource $foreignid password $password
echo $PROVISION asset add $foreignsource $foreignid connection $connection
      if [ x"$enablepass" == x"" ]
      then
echo $PROVISION asset add $foreignsource $foreignid autoenable \"A\"
echo $PROVISION asset add $foreignsource $foreignid enable notused
      else
echo $PROVISION asset add $foreignsource $foreignid enable $enablepass
      fi 

# 
echo $PROVISION interface add $foreignsource $foreignid $ip
echo $PROVISION interface set $foreignsource $foreignid $ip snmp-primary "P"
echo $PROVISION interface set $foreignsource $foreignid $ip descr \"provided by TN contrib script\"

echo $PROVISION service add $foreignsource $foreignid $ip ICMP
echo $PROVISION service add $foreignsource $foreignid $ip SNMP

echo $PROVISION  snmp set $ip $snmpcommunity version=$snmpversion timeout=$snmptimeout
CURL="curl -s -X POST -H \"Content-Type: application/xml\" -d \"<?xml version=\\\"1.0\\\" encoding=\\\"UTF-8\\\"?> <policy xmlns=\\\"http://xmlns.opennms.org/xsd/config/foreign-source\\\" class=\\\"org.opennms.netmgt.provision.persist.policies.MatchingIpInterfacePolicy\\\" name=\\\"Manage$ip\\\"> <parameter value=\\\"MANAGE\\\" key=\\\"action\\\"/> <parameter value=\\\"ALL_PARAMETERS\\\" key=\\\"matchBehavior\\\"/> <parameter value=\\\"~^$ip$\\\" key=\\\"ipAddress\\\"/> </policy>\""
echo $CURL $RESTURL$foreignsource/policies       
   done
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
                 RESTURL=" -u admin:admin http://$2:8980/opennms/rest/foreignSources/"
                 shift 2
                 ;;
 
           "-r") CREATE_REQUISITIONS=1
                 shift 1
                 ;;

           "-i") IMPORT_REQUISITIONS=1
                 shift 1
                 ;;

 
           "-n") CREATE_NODES=1
                 shift 1
                 ;;

              *) show_help
                 ;;

    esac

done

PROVISION="$OPENNMS_HOME/bin/provision.pl --password admin $URL"

if [ "$NODES_FILE" == "" ]; then
	echo "node file not set. Exiting...."
	exit 2
fi
if [ ! -f $NODES_FILE ]; then
        echo "file '$NODES_FILE' not found. Exiting...."
        exit 2
fi
if [ $CREATE_REQUISITIONS -eq 1 ]; then
       doCreateRequisition
fi
if [ $CREATE_NODES -eq 1 ]; then
       doCreateNodes 
fi
if [ $IMPORT_REQUISITIONS -eq 1 ]; then
       doImportRequisition
fi
