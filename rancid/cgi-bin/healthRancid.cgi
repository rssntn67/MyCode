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
DATUM='/bin/date'
PGREP='/usr/bin/pgrep -u rancid'
LIST='/bin/ls'
FIND_CMD='/usr/bin/find'
TAIL_CMD='/usr/bin/tail'
CUT_CMD='/usr/bin/cut'
CRONTAB_CMD='/usr/bin/crontab'
# opennms REST interface access URL and command
CURL='/usr/bin/curl -X GET -H "Content-Type: application/xml" -u admin:admin '
NODE_REST_URL='opennms.arsinfo.it:8980/opennms/rest/nodes?label='
# commands

LATEST_LOG=`$LIST -tr $LOG_DIR| $TAIL_CMD -1`
LATEST_LOG_GROUP=`echo $LATEST_LOG | $CUT_CMD -d. -f1 `
LATEST_LOG_DAY=`echo $LATEST_LOG | $CUT_CMD -d. -f2 `
LATEST_LOG_TIME=`echo $LATEST_LOG | $CUT_CMD -d. -f3 `
LATEST_LOG_HOUR=`echo $LATEST_LOG_TIME | $CUT_CMD -c 1-2 `
LATEST_LOG_MIN=`echo $LATEST_LOG_TIME | $CUT_CMD -c 3-4 `
LATEST_LOG_SEC=`echo $LATEST_LOG_TIME | $CUT_CMD -c 5-6 `
RANCID_RUNNING=`$PGREP rancid-run | wc -l`
# statistics
ROUTER_COUNT=`cat $ROUTER_DB| wc -l `
ROUTER_COUNT_UP=`$GREP ':up:' $ROUTER_DB| wc -l `
MAX_ROUTER_COUNT_UP=500

LAST_DAYSAVED_CONF=`$FIND_CMD $CONFIGS_DIR -mtime 0 -print | wc -l`
LAST_DAYSAVED_CONF_MIN=250
UNSCHED_ROUT=`$FIND_CMD $CONFIGS_DIR -mtime +24 -print | grep -v CVS | wc -l`
MAX_UNSCHED_ROUT=0
NOW=`$DATUM +%s`
EXEC_DATE=`$DATUM -d "$LATEST_LOG_DAY $LATEST_LOG_HOUR:$LATEST_LOG_MIN:$LATEST_LOG_SEC" +%s`
ELAPSED=$(($NOW-$EXEC_DATE))
MAX_ELAPSED=7200
MAX_ELAPSED_FROM_RUN=46800
IS_OK=0
#
echo "Content-Type: text/html"
echo
echo "<HTML><BODY>"
if [ $ROUTER_COUNT_UP -gt $MAX_ROUTER_COUNT_UP ]
then
echo "<H2>"
IS_OK=1
echo "Attenzione ci sono <b>$ROUTER_COUNT_UP router 'up'</b> nel gruppo $RANCID_GROUP, massimo consentito: $MAX_ROUTER_COUNT_UP"
echo "</H2>"
fi
if [ $LAST_DAYSAVED_CONF_MIN -gt $LAST_DAYSAVED_CONF ]
then
echo "<H2>"
IS_OK=1
echo "Attenzione ci sono <b>$LAST_DAYSAVED_CONF configurazioni salvate nelle ultime 24 ore</b> nel gruppo $RANCID_GROUP, minimo consentito: $LAST_DAYSAVED_CONF_MIN"
echo "</H2>"
fi
if [ $RANCID_RUNNING -gt 0 -a $ELAPSED -gt $MAX_ELAPSED ]
then
echo "<H2>"
IS_OK=1
echo "Attenzione <b>rancid-run in esecuzione da $ELAPSED secondi</b>, massimo consentito: $MAX_ELAPSED"
echo "</H2>"
elif [ $ELAPSED -gt $MAX_ELAPSED_FROM_RUN ]
then
echo "<H2>"
IS_OK=1
echo "Attenzione <b>rancid-run non e' stato eseguito da $ELAPSED secondi</b>, massimo consentito: $MAX_ELAPSED_FROM_RUN"
echo "</H2>"
fi
if [ $UNSCHED_ROUT -gt 0 ]
then
IS_OK=1
echo "<H2>"
echo "Attenzione ci sono<b> $UNSCHED_ROUT nodi che non hanno una schedulazione negli ultimi 25 giorni</b>, massimo consentito: $MAX_UNSCHED_ROUT"
echo "</H2>"
fi
if [ $IS_OK -eq 0 ]
then 
echo "<H2>"
echo "<a href=\"http://opennms.arsinfo.it:8980/opennms/rancid/index.jsp\">Rancid page on opennms</a> or <a href=\"http://opennmsrancid.arsinfo.it/cgi-bin/healthRancid.cgi\">check manually</a>. Rancid Health Check: Successfull"
echo "</H2>"
fi

echo "</HTML></BODY>"
