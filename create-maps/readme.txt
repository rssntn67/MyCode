Per creare la mappa dell'Italia con regioni e province,
entrare su postgresql sul db di opennms e lanciare i seguenti comandi

Se si vuole resettare il db delle mappe:
delete form map 


COPY map FROM 'path_installazione_opennms/etc/create-maps/map'
COPY element FROM 'path_installazione_opennms/etc/create-maps/element'

Se è stato resettato il db delle mappe:
select setval('mapnxtid',127);

Per creare la struttura per la mappa degli allarmi, lanciare lo script
1) create_alarmed_maps.sql
2) COPY alarmed_map FROM 'path_installazione_opennms/etc/create-maps/map'
   COPY alarmed_element FROM 'path_installazione_opennms/etc/create-maps/element'


N.B.: Il dbms potrebbe dare problemi di privilegi di accesso. 
	  Modificare i privilegi di accesso dei due files e riprovare.
	  
	  
 