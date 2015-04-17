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
function getElapsedString {
TIME_SPEC1="secondo"
TIME_SPEC2="secondi"
if [ $1 -gt 86400 ]
then
NUMOF=$(($1/86400))
TIME_SPEC1="giorno"
TIME_SPEC2="giorni"
echo "<br>Sono passati $GIORNI giorni"
elif [ $1 -gt 3600 ]
then
NUMOF=$(($1/3600))
TIME_SPEC1="ora"
TIME_SPEC2="ore"
elif [ $1 -gt 60 ]
then
NUMOF=$(($1/60))
TIME_SPEC1="minuto"
TIME_SPEC2="minuti"
else
NUMOF=$1
fi
if [ $NUMOF -eq 1 ]
then
echo "$NUMOF $TIME_SPEC1"
else
echo "$NUMOF $TIME_SPEC2"
fi
}

LATEST_LOG=`$LIST -tr $LOG_DIR| $TAIL_CMD -1`
LATEST_LOG_GROUP=`echo $LATEST_LOG | $CUT_CMD -d. -f1 `
LATEST_LOG_DAY=`echo $LATEST_LOG | $CUT_CMD -d. -f2 `
LATEST_LOG_TIME=`echo $LATEST_LOG | $CUT_CMD -d. -f3 `
LATEST_LOG_HOUR=`echo $LATEST_LOG_TIME | $CUT_CMD -c 1-2 `
LATEST_LOG_MIN=`echo $LATEST_LOG_TIME | $CUT_CMD -c 3-4 `
LATEST_LOG_SEC=`echo $LATEST_LOG_TIME | $CUT_CMD -c 5-6 `
RANCID_RUNNING=`$PGREP rancid-run | wc -l`
# statistics
ROUTER_COUNT_TYPE_KNOWN=0;
ROUTER_COUNT_TYPE_UNKNOWN=0;
ROUTER_COUNT=`cat $ROUTER_DB| wc -l `
ROUTER_COUNT_UP=`$GREP ':up:' $ROUTER_DB| wc -l `
TCOMWIRE_ROUTER_COUNT=`$GREP ':3comwireless:' $ROUTER_DB | wc -l `
TCOMWIRE_ROUTER_COUNT_UP=`$GREP ':3comwireless:up:' $ROUTER_DB | wc -l `
ROUTER_COUNT_TYPE_KNOWN=$((ROUTER_COUNT_TYPE_KNOWN + TCOMWIRE_ROUTER_COUNT))
ALCATEL_ROUTER_COUNT=`$GREP ':alcatel:' $ROUTER_DB | wc -l `
ALCATEL_ROUTER_COUNT_UP=`$GREP ':alcatel:up:' $ROUTER_DB | wc -l `
ROUTER_COUNT_TYPE_KNOWN=$((ROUTER_COUNT_TYPE_KNOWN + ALCATEL_ROUTER_COUNT))
ALCATELSW_ROUTER_COUNT=`$GREP ':alcatel6400:' $ROUTER_DB | wc -l `
ALCATELSW_ROUTER_COUNT_UP=`$GREP ':alcatel6400:up:' $ROUTER_DB | wc -l `
ROUTER_COUNT_TYPE_KNOWN=$((ROUTER_COUNT_TYPE_KNOWN + ALCATELSW_ROUTER_COUNT))
ALVARION_ROUTER_COUNT=`$GREP ':alvarion:' $ROUTER_DB | wc -l `
ALVARION_ROUTER_COUNT_UP=`$GREP ':alvarion:up:' $ROUTER_DB | wc -l `
ROUTER_COUNT_TYPE_KNOWN=$((ROUTER_COUNT_TYPE_KNOWN + ALVARION_ROUTER_COUNT))
BELKIN_ROUTER_COUNT=`$GREP ':belkin:' $ROUTER_DB | wc -l `
ROUTER_COUNT_TYPE_UNKNOWN=$((ROUTER_COUNT_TYPE_UNKNOWN + BELKIN_ROUTER_COUNT))
#BELKIN_ROUTER_COUNT_UP=`$GREP ':belkin:up:' $ROUTER_DB | wc -l `
CISCO_ROUTER_COUNT=`$GREP ':cisco:' $ROUTER_DB | wc -l `
CISCO_ROUTER_COUNT_UP=`$GREP ':cisco:up:' $ROUTER_DB | wc -l `
ROUTER_COUNT_TYPE_KNOWN=$((ROUTER_COUNT_TYPE_KNOWN + CISCO_ROUTER_COUNT))
CISCOONS_ROUTER_COUNT=`$GREP ':cisco-ons:' $ROUTER_DB | wc -l `
ROUTER_COUNT_TYPE_UNKNOWN=$((ROUTER_COUNT_TYPE_UNKNOWN + CISCOONS_ROUTER_COUNT))
#CISCOONS_ROUTER_COUNT_UP=`$GREP ':cisco-ons:up:' $ROUTER_DB | wc -l `
CISCOXR_ROUTER_COUNT=`$GREP ':cisco-xr:' $ROUTER_DB | wc -l `
CISCOXR_ROUTER_COUNT_UP=`$GREP ':cisco-xr:up:' $ROUTER_DB | wc -l `
ROUTER_COUNT_TYPE_KNOWN=$((ROUTER_COUNT_TYPE_KNOWN + CISCOXR_ROUTER_COUNT))
CODIAN_ROUTER_COUNT=`$GREP ':codian:' $ROUTER_DB | wc -l `
ROUTER_COUNT_TYPE_UNKNOWN=$((ROUTER_COUNT_TYPE_UNKNOWN + CODIAN_ROUTER_COUNT))
#CODIAN_ROUTER_COUNT_UP=`$GREP ':codian:up:' $ROUTER_DB | wc -l `
LINUX_ROUTER_COUNT=`$GREP ':linux:' $ROUTER_DB | wc -l `
ROUTER_COUNT_TYPE_UNKNOWN=$((ROUTER_COUNT_TYPE_UNKNOWN + LINUX_ROUTER_COUNT))
#LINUX_ROUTER_COUNT_UP=`$GREP ':linux:up:' $ROUTER_DB | wc -l `
MIKROTIK_ROUTER_COUNT=`$GREP ':mikrotik:' $ROUTER_DB | wc -l `
MIKROTIK_ROUTER_COUNT_UP=`$GREP ':mikrotik:up:' $ROUTER_DB | wc -l `
ROUTER_COUNT_TYPE_KNOWN=$((ROUTER_COUNT_TYPE_KNOWN + MIKROTIK_ROUTER_COUNT))
MOTOROLA_ROUTER_COUNT=`$GREP ':motorola:' $ROUTER_DB | wc -l `
ROUTER_COUNT_TYPE_UNKNOWN=$((ROUTER_COUNT_TYPE_UNKNOWN + MOTOROLA_ROUTER_COUNT))
#MOTOROLA_ROUTER_COUNT_UP=`$GREP ':motorola:up:' $ROUTER_DB | wc -l `
PATTON_ROUTER_COUNT=`$GREP ':patton:' $ROUTER_DB | wc -l `
PATTON_ROUTER_COUNT_UP=`$GREP ':patton:up:' $ROUTER_DB | wc -l `
ROUTER_COUNT_TYPE_KNOWN=$((ROUTER_COUNT_TYPE_KNOWN + PATTON_ROUTER_COUNT))
PHOENIXTEC_ROUTER_COUNT=`$GREP ':phoenixtec:' $ROUTER_DB | wc -l `
ROUTER_COUNT_TYPE_UNKNOWN=$((ROUTER_COUNT_TYPE_UNKNOWN + PHOENIXTEC_ROUTER_COUNT))
#PHOENIXTEC_ROUTER_COUNT_UP=`$GREP ':phoenixtec:up:' $ROUTER_DB | wc -l `
POWERWARE_ROUTER_COUNT=`$GREP ':powerware:' $ROUTER_DB | wc -l `
ROUTER_COUNT_TYPE_UNKNOWN=$((ROUTER_COUNT_TYPE_UNKNOWN + POWERWARE_ROUTER_COUNT))
#POWERWARE_ROUTER_COUNT_UP=`$GREP ':powerware:up:' $ROUTER_DB | wc -l `
RITTAL_ROUTER_COUNT=`$GREP ':rittal:' $ROUTER_DB | wc -l `
ROUTER_COUNT_TYPE_UNKNOWN=$((ROUTER_COUNT_TYPE_UNKNOWN + RITTAL_ROUTER_COUNT))
#RITTAL_ROUTER_COUNT_UP=`$GREP ':rittal:up:' $ROUTER_DB | wc -l `
STRATEX_ROUTER_COUNT=`$GREP ':stratex:' $ROUTER_DB | wc -l `
ROUTER_COUNT_TYPE_UNKNOWN=$((ROUTER_COUNT_TYPE_UNKNOWN + STRATEX_ROUTER_COUNT))
#STRATEX_ROUTER_COUNT_UP=`$GREP ':stratex:up:' $ROUTER_DB | wc -l `
TANDBERG_ROUTER_COUNT=`$GREP ':tandberg:' $ROUTER_DB | wc -l `
ROUTER_COUNT_TYPE_UNKNOWN=$((ROUTER_COUNT_TYPE_UNKNOWN + TANDBERG_ROUTER_COUNT))
#TANDBERG_ROUTER_COUNT_UP=`$GREP ':tandberg:up:' $ROUTER_DB | wc -l `
TECNO_ROUTER_COUNT=`$GREP ':tecnolabs:' $ROUTER_DB | wc -l `
ROUTER_COUNT_TYPE_UNKNOWN=$((ROUTER_COUNT_TYPE_UNKNOWN + TECNO_ROUTER_COUNT))
#TECNO_ROUTER_COUNT_UP=`$GREP ':tecnolabs:up:' $ROUTER_DB | wc -l `
TPLINK_ROUTER_COUNT=`$GREP ':tplink:' $ROUTER_DB | wc -l `
ROUTER_COUNT_TYPE_UNKNOWN=$((ROUTER_COUNT_TYPE_UNKNOWN + TPLINK_ROUTER_COUNT))
#TPLINK_ROUTER_COUNT_UP=`$GREP ':tplink:up:' $ROUTER_DB | wc -l `
UBI_ROUTER_COUNT=`$GREP ':ubiquiti:' $ROUTER_DB | wc -l `
ROUTER_COUNT_TYPE_UNKNOWN=$((ROUTER_COUNT_TYPE_UNKNOWN + UBI_ROUTER_COUNT))
#UBI_ROUTER_COUNT_UP=`$GREP ':ubiquiti:up:' $ROUTER_DB | wc -l `
WIFLESS_ROUTER_COUNT=`$GREP ':wifless:' $ROUTER_DB | wc -l `
WIFLESS_ROUTER_COUNT_UP=`$GREP ':wifless:up:' $ROUTER_DB | wc -l `
ROUTER_COUNT_TYPE_KNOWN=$((ROUTER_COUNT_TYPE_KNOWN + WIFLESS_ROUTER_COUNT))
WINDOWS_ROUTER_COUNT=`$GREP ':windows:' $ROUTER_DB | wc -l `
ROUTER_COUNT_TYPE_UNKNOWN=$((ROUTER_COUNT_TYPE_UNKNOWN + WINDOWS_ROUTER_COUNT))
#WINDOWS_ROUTER_COUNT_UP=`$GREP ':windows:up:' $ROUTER_DB | wc -l `
ZYXEL_ROUTER_COUNT=`$GREP ':zyxel:' $ROUTER_DB | wc -l `
ROUTER_COUNT_TYPE_UNKNOWN=$((ROUTER_COUNT_TYPE_UNKNOWN + ZYXEL_ROUTER_COUNT))
#ZYXEL_ROUTER_COUNT_UP=`$GREP ':zyxel:up:' $ROUTER_DB | wc -l `
UNKNOWN_ROUTER_COUNT=`$GREP ':unknown:' $ROUTER_DB | wc -l `
#UNKNOWN_ROUTER_COUNT_UP=`$GREP ':unknown:up:' $ROUTER_DB | wc -l `
#
LAST_DAYSAVED_CONF=`$FIND_CMD $CONFIGS_DIR/*.it -mtime 0 -print | grep -v CVS | wc -l`
WITHOUT_CONF=`$FIND_CMD $CONFIGS_DIR -size 0 -print | wc -l`
UNSCHED_ROUT=`$FIND_CMD $CONFIGS_DIR -mtime +23 -print | grep -v CVS | wc -l`
NOW=`$DATUM +%s`
EXEC_DATE=`$DATUM -d "$LATEST_LOG_DAY $LATEST_LOG_HOUR:$LATEST_LOG_MIN:$LATEST_LOG_SEC" +%s`
ELAPSED=$(($NOW-$EXEC_DATE))
#
echo "Content-Type: text/html"
echo
echo "<HTML><BODY>"
echo "<H2>"
echo "Situazione Rancid"
echo "</H2>"
echo 
echo "Trovati <b>$ROUTER_COUNT router</b> nel gruppo $RANCID_GROUP, di cui:"
echo "<br>"
echo "$ROUTER_COUNT_UP 'router up'"
echo "<br>"
echo "$ROUTER_COUNT_TYPE_KNOWN 'router con download configurazione supportato da rancid' "
echo "<br>"
echo "$ROUTER_COUNT_TYPE_UNKNOWN 'router con download configurazione non supportato da rancid' "
echo "<br>"
echo "$UNKNOWN_ROUTER_COUNT 'router con device type: unknown'"
echo "<br>"
echo "Ci sono <b>$LAST_DAYSAVED_CONF configurazioni salvate nelle ultime 24 ore</b> nel gruppo $RANCID_GROUP"
echo "<br>"
echo "<br>"
if [ $RANCID_RUNNING -gt 0 ]
then
echo "In esecuzione: <b>rancid-run</b>:"
else
echo "Ultima esecuzione <b>rancid-run</b>:"
fi
echo " Gruppo $LATEST_LOG_GROUP - Giorno `echo $LATEST_LOG_DAY | $CUT_CMD -c 7-8` - Mese `echo $LATEST_LOG_DAY | $CUT_CMD -c 5-6` - Anno `echo $LATEST_LOG_DAY | $CUT_CMD -c 1-4` - Ora $LATEST_LOG_HOUR:$LATEST_LOG_MIN:$LATEST_LOG_SEC - Elapsed: "
getElapsedString $ELAPSED
echo "<br>"
echo "<br>Esecuzione programmata di <b>rancid-run</b>: "
$CRONTAB_CMD -l | $GREP rancid-run | $GREP -v '#' | while read line
do echo "<br>$line"
done
echo "<br>"
echo "<H2>"
echo "Router con download della configurazione supportato"
echo "</H2>"
echo "<ul>"
echo "<li>"
echo "devicetype 3comwireless: $TCOMWIRE_ROUTER_COUNT router: $TCOMWIRE_ROUTER_COUNT_UP up."
echo "</li>"
echo "<li>"
echo "devicetype alcatel: $ALCATEL_ROUTER_COUNT router: $ALCATEL_ROUTER_COUNT_UP up."
echo "</li>"
echo "<li>"
echo "devicetype alcatel6400:  $ALCATELSW_ROUTER_COUNT router: $ALCATELSW_ROUTER_COUNT_UP up."
echo "</li>"
echo "<li>"
echo "devicetype alvarion: $ALVARION_ROUTER_COUNT router: $ALVARION_ROUTER_COUNT_UP up."
echo "</li>"
echo "<li>"
echo "devicetype cisco-xr: $CISCOXR_ROUTER_COUNT router:  $CISCOXR_ROUTER_COUNT_UP up."
echo "</li>"
echo "<li>"
echo "devicetype cisco: $CISCO_ROUTER_COUNT router:  $CISCO_ROUTER_COUNT_UP up."
echo "</li>"
echo "<li>"
echo "devicetype mikrotik: $MIKROTIK_ROUTER_COUNT router: $MIKROTIK_ROUTER_COUNT_UP up."
echo "</li>"
echo "<li>"
echo "devicetype patton: $PATTON_ROUTER_COUNT router: $PATTON_ROUTER_COUNT_UP up."
echo "</li>"
echo "<li>"
echo "devicetype wifless: $WIFLESS_ROUTER_COUNT router: $WIFLESS_ROUTER_COUNT_UP up."
echo "</li>"
echo "</ul>"
echo "<div>"
echo "Elenca i <a href=\"/cgi-bin/checkRancidWithoutConfMin.cgi\" target=\"_blank\">$WITHOUT_CONF Router</a> che non hanno ancora una configurazione salvata."
echo "</div>"
echo "<br>"
echo "<div>"
echo "Dettagli sugli apparati <a href=\"/cgi-bin/checkRancidWithoutConf.cgi\" target=\"_blank\">$WITHOUT_CONF Router</a> che non hanno ancora una configurazione salvata."
echo "</div>"
echo "<br>"
echo "<div>"
echo "Elenca i <a href=\"http://opennms.arsinfo.it:8980/opennms/event/list?sortby=id&acktype=unack&limit=500&filter=msgsub%3Drancid&filter=exactUei%3Duei.opennms.org%2Fstandard%2Francid%2Ftraps%2FrancidTrapDownloadFailure&multiple=0\"  target=\"_blank\">gli ultimi 500 eventi</a> di download failure ."
echo "</div>"
echo "<br>"
echo "<H2>"
echo "Router con download della configurazione non supportato"
echo "</H2>"
echo "<ul>"
echo "<li>"
echo "devicetype belkin      :  $BELKIN_ROUTER_COUNT router."
echo "</li>"
echo "<li>"
echo "devicetype cisco-ons   :  $CISCOONS_ROUTER_COUNT router."
echo "</li>"
echo "<li>"
echo "devicetype codian      :  $CODIAN_ROUTER_COUNT router."
echo "</li>"
echo "<li>"
echo "devicetype linux       :  $LINUX_ROUTER_COUNT router."
echo "</li>"
echo "<li>"
echo "devicetype motorola    :  $MOTOROLA_ROUTER_COUNT router."
echo "</li>"
echo "<li>"
echo "devicetype phoenixtec   :  $PHOENIXTEC_ROUTER_COUNT router."
echo "</li>"
echo "<li>"
echo "devicetype powerware   :  $POWERWARE_ROUTER_COUNT router."
echo "</li>"
echo "<li>"
echo "devicetype rittal      :  $RITTAL_ROUTER_COUNT router."
echo "</li>"
echo "<li>"
echo "devicetype stratex     :  $STRATEX_ROUTER_COUNT router."
echo "</li>"
echo "<li>"
echo "devicetype tandberg    :  $TANDBERG_ROUTER_COUNT router."
echo "</li>"
echo "<li>"
echo "devicetype tecnolabs   :  $TECNO_ROUTER_COUNT router."
echo "</li>"
echo "<li>"
echo "devicetype tplink      :  $TPLINK_ROUTER_COUNT router."
echo "</li>"
echo "<li>"
echo "devicetype ubiquiti    :  $UBI_ROUTER_COUNT router."
echo "</li>"
echo "<li>"
echo "devicetype windows    :  $WINDOWS_ROUTER_COUNT router."
echo "</li>"
echo "<li>"
echo "devicetype zyxel       :  $ZYXEL_ROUTER_COUNT router."
echo "</li>"
echo "</ul>"
echo "<br>"
echo "<h2>"
echo "Router di tipo sconosciuto"
echo "</h2>"
echo "<ul>"
echo "<li>"
echo "devicetype unknown:  $UNKNOWN_ROUTER_COUNT router."
echo "</li>"
echo "</ul>"
echo "<br>"
echo "<div>"
echo "Visualizza <a href=\"/cgi-bin/checkRancidUnknown.cgi\"  target=\"_blank\">$UNKNOWN_ROUTER_COUNT Router</a> unknown."
echo "</div>"
echo "<br>"
echo "<h2>Altre Informazioni e Utilita'</h2>"
echo "<div>"
if [ $UNSCHED_ROUT -gt 0 ]
then
echo "Per <a href=\"/cgi-bin/checkRancidOldScheduled.cgi\"  target=\"_blank\">$UNSCHED_ROUT Router</a> non e' stato programmato un download negli ultimi 24 giorni."
else
echo "Per tutti i router e' stato programmato un download negli ultimi 24 giorni."
fi
echo "</div>"
echo "<div>"
echo "Cerca <a href=\"/cgi-bin/checkRancidOldBackUp.cgi\"  target=\"_blank\">Router</a> con una configurazione salvata piu' vecchia di 30 giorni."
echo "</div>"
echo "<br>"
echo "<h2>"
echo "Collegamenti ad altre pagine web utili per rancid"
echo "</h2>"
echo "<div>"
echo "Il repository CVS ha una interfaccia web: <a href=\"http://opennmsrancid.arsinfo.it\"  target=\"_blank\">viewvc</a>, per accedere utilizzate username e password di sistema"
echo "</div>"
echo "<div>"
echo "<a href=\"http://opennmsrancid.arsinfo.it/viewvc/rancid/ARSINFO/configs/?sortby=date&sortdir=down#dirlist\"  target=\"_blank\">Click here<a>"
echo "per visualizzare la lista dei backup delle configurazioni di router per ordine inverso dalla data di backup:"
echo "</div>"
echo "<div>"
echo "<a href=\"http://opennmsrancid.arsinfo.it/viewvc/rancid/ARSINFO/configs/?sortby=date&sortdir=down#dirlist\"  target=\"_blank\">Click here</a>"
echo "per visualizzare la lista degli apparati che non hanno ancora un backup. Tutte le entry"
echo "del repository che hanno la dicitura new router denotano un apparato senza una configurazione salvata"
echo "</div>"
echo "<div>"
echo "Rancid invia mail alle seguenti caselle di posta elettronica ogni volta che viene eseguito:"
echo "rancid@ARSINFO.it"
echo "rancid.adm@ARSINFO.it"
echo "Per dettagli sui run di rancid accedete alle sopra citate caselle di posta elettronica"
echo "</div>"
echo "<div>"
echo "La applicazione di integrazione fra rancid ed opennms provvede ad inviare trap ad ogni esecuzione di rancid verso opennms."
echo "<br>"
echo "<a href=\"http://opennms.arsinfo.it:8980/opennms/event/list?limit=10&sortby=id&filter=msgsub%3Drancid\"  target=\"_blank\">Click here</a>"
echo "per visualizzare la lista degli eventi rancid su opennms"
echo "</div>"
echo "</HTML></BODY>"
