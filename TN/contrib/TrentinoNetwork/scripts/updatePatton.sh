#!/bin/bash
OPENNMS_HOME="/usr/share/opennms"
SQL_COMMAND="select n.nodeid,ipaddr from node n left join ipinterface i on i.nodeid = n.nodeid left join category_node cn on cn.nodeid=n.nodeid left join categories c on c.categoryid=cn.categoryid where categoryname='MediaGateway' and isSnmpPrimary='P' and nodesysoid is null"
   /usr/bin/psql -t -F: -A -U opennms -h opennmsdb -c "$SQL_COMMAND" | while read line
   do 
      nodeid=`echo $line | cut -d':' -f1`
      ip=`echo $line | cut -d':' -f2 | sed -e "s/\"//g" -e "s/ //g"`
      nodesysdescription=`snmpget -On -c ma918na2116ge -v1 $ip .1.3.6.1.2.1.1.1.0 | awk -F'STRING: ' {'print $2'}`
      nodesysoid=`snmpget -On -c ma918na2116ge -v1 $ip .1.3.6.1.2.1.1.2.0 | awk -F'OID: ' {'print $2'}`
      nodesyscontact=`snmpget -On -c ma918na2116ge -v1 $ip .1.3.6.1.2.1.1.4.0 | awk -F'STRING: ' {'print $2'}`
      nodesysname=`snmpget -On -c ma918na2116ge -v1 $ip .1.3.6.1.2.1.1.5.0 | awk -F'STRING: ' {'print $2'}`
      nodesyslocation=`snmpget -On -c ma918na2116ge -v1 $ip .1.3.6.1.2.1.1.6.0 | awk -F'STRING: ' {'print $2'}`
SQL_UPDATE="UPDATE node set nodesysdescription='$nodesysdescription', nodesysoid='$nodesysoid', nodesyscontact='$nodesyscontact',nodesysname='$nodesysname', nodesyslocation='$nodesyslocation' where nodeid = $nodeid"
echo $SQL_UPDATE
/usr/bin/psql -U opennms -h opennmsdb -c "$SQL_UPDATE" 
   done
