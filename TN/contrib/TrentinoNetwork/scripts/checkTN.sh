#!/bin/bash
OPENNMS_HOME="/usr/share/opennms"

foreignsource="ARSINFO"
RESTURL=" -u admin:admin http://127.0.0.1:8980/opennms/rest/foreignSources/"
NODES_FILE=""
VRFURL="-u admin:admin http://vrf.arsinfo.it:8080/fast_isi/getVRF" 

show_help () {
        cat <<END

Usage: $0 -f <file.csv> 

This script will check that the cvs file is properly formatted
 
END
        exit 1
}

doCheckNodes() {
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
      doCheckDns $nodelabel
      doCheckIp $ip
      doCheckTnnetCategory $category1 $category2
      doCheckNotifCategory $category3
      doCheckThresCategory $category4
      doCheckSnmp $snmpcommunity $snmptimeout $snmpversion
      doCheckConn $username $password $enablepass $connection
   done
}

#if [ "${1}" == "" ] ; then
   #show_help
#fi
#while [ "${1}" != "" ] ; do
#
   #case "${1}" in
#
           #"-f") if [ "${2}" == "" ] ; then show_help; fi
                 #NODES_FILE=$2
                 #shift 2
                 #;;
#
              #*) show_help
                 #;;
#
    #esac
#
#done
#
#if [ "$NODES_FILE" == "" ]; then
	#echo "node file not set. Exiting...."
	#exit 2
#fi
#if [ ! -f $NODES_FILE ]; then
        #echo "file '$NODES_FILE' not found. Exiting...."
        #exit 2
#fi
#doCheckNodes
 curl -s -X GET $VRFURL  
#| sed -e 's/[{}]/''/g' | awk -v k="text" '{n=split($0,a,","); for (i=1; i<=n; i++) print a[i]}' | sed -e "s/\[//g" -e "s/\]//g" -e "s/\"//g" -e "s/ //g" | sort -u
