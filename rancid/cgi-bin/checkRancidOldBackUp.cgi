#! /bin/bash
# configuration to let the script work
echo "Content-Type: text/plain"
echo
BASEDIR=/var/lib/rancid/var; export BASEDIR
PATH=/var/lib/rancid/bin:/usr/bin:/usr/sbin:/bin:/usr/local/bin:/usr/bin; export PATH
CVSROOT=$BASEDIR/CVS; export CVSROOT
HOME=/var/lib/rancid; export HOME
RANCID_REPOSITORY=$BASEDIR'/ARSINFO'
LOG_DIR=$BASEDIR'/logs'
ROUTER_DB=$RANCID_REPOSITORY'/router.db'
CONFIGS_DIR=$RANCID_REPOSITORY'/configs'
CVS_CMD='/usr/bin/cvs'
# opennms REST interface access URL and command
CURL='/usr/bin/curl -X GET -H "Content-Type: application/xml" -u admin:admin '
NODE_REST_URL='opennms.arsinfo.it:8980/opennms/rest/nodes?label='
# commands
GREP='/bin/grep'
FIND_CMD='/usr/bin/find'
# statistics
MONTH_AGO=`date --date="30 days ago" +%Y/%m/%d`
echo "Elenco degli apparati con una configurazione salvata piu' vecchia di 30 giorni"
echo
echo "Rancid salva la configurazione solo se necessario"
echo "Una configurazione viene salvata solo se differisce da quella salvata precedentemente"
echo "Questa lista e' puramente indicativa e da una idea dello stato delle configurazioni salvate" 
echo "Questa lista include anche i router, unknown, non supportati e senza backup" 
echo "Accedere alla lista dei router unknown per avere la lista dettagliata"
echo "Accedere alla lista dei router senza configurazione per avere la lista dettagliata"
echo
PRINT_LINE=0
PRINT_HEAD=0
COUNT=0
HOWMANY=`$CVS_CMD log -S -l -rHEAD -d "<$MONTH_AGO" $CONFIGS_DIR | grep 'RCS file:' | grep -v Attic | wc -l ` 
echo "Trovati $HOWMANY Routers con configurazione piu' vecchia di 30 giorni"
echo 
$CVS_CMD log -S -l -rHEAD -d "<$MONTH_AGO" $CONFIGS_DIR | grep 'RCS file:' | grep -v Attic | sed -e "s/Working file://g"  -e "s/RCS file: \/var\/lib\/rancid\/var\/CVS\/ARSINFO\/configs\///g" -e "s/,v//g" 
#| while read line
#do DO_RCS=`echo $line |  $GREP 'RCS file: ' | grep -v Attic | wc -l`
#
#if [ $DO_RCS -eq 1 ]
#then DEVICE=`echo $line | sed -e "s/RCS file: \/var\/lib\/rancid\/var\/CVS\/ARSINFO\/configs\///g" -e "s/,v//g"` 
#ERRORS=`$GREP $DEVICE $LOG_DIR/* | $GREP -i error | wc -l`
#EORNOTFOUND=`$GREP $DEVICE $LOG_DIR/* | $GREP -i 'End of run not found' | wc -l`
   #if [ $ERRORS -gt 0 -o $EORNOTFOUND -gt 0 ]
   #then PRINT_LINE=1
   #fi
#fi
#
#if [ $PRINT_LINE -eq 1 -a $PRINT_HEAD -eq 0 ]
#then DO_HEAD=`echo $line | grep 'head: ' | wc -l`
   #if [ $DO_HEAD -eq 1 ]
   #then HEAD=`echo $line | sed -e "s/head://g" -e "s/ //g"`
      #if [ "$HEAD" != '1.1' ]
      #then echo $DEVICE
           #echo
           #echo Log Entry for device:
            #$GREP $DEVICE $LOG_DIR/* | sed 4q
           #echo
           #echo
           #PRINT_HEAD=1
           #COUNT=`expr $COUNT + 1`
      #fi
   #fi
#fi
#if [ $PRINT_LINE -eq 1 -a $PRINT_HEAD -eq 1 ]
#then echo $line
#fi
#DO_END=`echo $line | grep '=============================================================================' | wc -l`
#if [ $DO_END -eq 1 ]
#then PRINT_LINE=0;PRINT_HEAD=0
#fi
#done
#echo
#echo "Found $COUNT Router with obsolete downloaded configuration"
