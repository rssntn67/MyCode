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
FIND_CMD='/usr/bin/find'
# opennms REST interface access URL and command
CURL='/usr/bin/curl -X GET -H "Content-Type: application/xml" -u admin:admin '
NODE_REST_URL='opennms.arsinfo.it:8980/opennms/rest/nodes?label='
#
echo "Content-Type: text/plain"
echo
echo "Riepilogo Router Senza BackUp nel Gruppo ARSINFO"
echo 
echo "Le cause piu' comuni sono: "
echo "1) router non attivo"
echo "2) le credenziali di accesso - username,password,metodo di accesso, sono errati"
echo "3) il nome dns e' errato"
echo "4) il router e' temporaneamente down e l'ultimo backup e' fallito, in questo caso trovate una versione del repository che non e' la 1.1"
echo ""
echo "Elenco dei router senza configurazione con le informazioni relative dei log file:"
echo ""
# start loop for no configuration found
cd $CONFIGS_DIR
$FIND_CMD . -size 0 -print | sed -e "s/\.\///g" | while read router
do echo;echo; echo "Router $router"
done
