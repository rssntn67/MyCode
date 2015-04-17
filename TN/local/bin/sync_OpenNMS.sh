#!/bin/bash

if [ -f /etc/opennms/imports/pending/ARSINFO.xml ]
then
    DIFF=$(diff -I '^<model-import' /etc/opennms/imports/ARSINFO.xml /etc/opennms/imports/pending/ARSINFO.xml)
    #echo "diff è: $DIFF"
    if [[ $DIFF ]]
    then 
        echo "$DIFF" | mail -s "Sync OpenNMS" opennms.adm@arsinfo.it
        #echo "Eseguo sync OpenNMS" 
        curl -s -S -X PUT -H "Content-Type: application/xml" -u admin:admin   http://localhost:8980/opennms/rest/requisitions/ARSINFO/import 
    fi
fi

