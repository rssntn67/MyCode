package org.opennms.netmgt.utils;

import java.util.ArrayList;
import java.util.List;

import org.hibernate.criterion.Restrictions;
import org.opennms.netmgt.xml.event.Event;
import org.opennms.netmgt.xml.event.Parm;
import org.opennms.netmgt.model.AckAction;
import org.opennms.netmgt.model.OnmsAlarm;
import org.opennms.netmgt.model.OnmsCriteria;
import org.opennms.netmgt.model.OnmsEvent;
import org.opennms.netmgt.model.OnmsNotification;

public class AcknowledgePolicy {

	AckAction m_action = AckAction.ACKNOWLEDGE;
	List<String> m_matchparms = new ArrayList<String>();

	boolean m_isNotifAck = true;

	final String m_uei;
	final String m_ackuei;

	boolean m_usedbid=false;
    
	public void useDbid() {
		m_usedbid = true;
	}
	
	public boolean match(Event event) {
		return m_uei.equals(event.getUei());
	}
	
	public boolean matchParameters(Event event, OnmsEvent onmsEvent) {
		for (String parameterName: m_matchparms) {
			for (Parm parm: event.getParms().getParmCollection()) {
				if (parm.getParmName().equals(parameterName)) {
					if (!onmsEvent.getEventParms().contains(parameterName+"="+parm.getValue().getContent())) 
						return false;
				}
			}
		}
		return true;
	}
	
	public AcknowledgePolicy(String uei, String ackuei) {
		m_uei=uei;
		m_ackuei = ackuei;
	}

	public void setAction(String action) {
        if (action == null) {
            action = "ack";
        }
        
        if ("ack".equals(action)) {
            m_action = AckAction.ACKNOWLEDGE;
        } else if ("unack".equals(action)) {
        	m_action = AckAction.UNACKNOWLEDGE;
        } else if ("clear".equals(action)) {
        	m_action= AckAction.CLEAR;
        } else if ("esc".equals(action)) {
        	m_action= AckAction.ESCALATE;
        } else {
            throw new IllegalArgumentException(
            "Must supply the 'action' parameter, set to either 'ack, 'unack', 'clear', or 'esc'");
        }

	}

	public OnmsCriteria getCriteria(Event event) {
		String sql="eventuei = '" + m_ackuei +"'";
        if (m_usedbid && m_isNotifAck) 
        	sql+= " and eventid = " + event.getDbid(); 
        else if (m_usedbid)
           	sql+= " and lasteventid = " + event.getDbid(); 
        else if (m_isNotifAck)
            sql+= " and notifications.nodeid = " + event.getNodeid(); 
        else
            sql+= " and alarms.nodeid = " + event.getNodeid(); 
        	
		OnmsCriteria criteria;
		if (m_isNotifAck) {
			 criteria= new OnmsCriteria(OnmsNotification.class);
		} else {
			criteria = new OnmsCriteria(OnmsAlarm.class);
		}
		criteria.add(Restrictions.sqlRestriction(sql));	
			 
		return criteria;	 
	}
	
	public void addParameterName(String parameterName) {
		m_matchparms.add(parameterName);
	}
	
	public AckAction getAckAction() {
		return m_action;
	}

	public boolean isNotifAck() {
		return m_isNotifAck;
	}
	
	public void notifAck() {
		m_isNotifAck = true;
	}
	
	public void alarmAck() {
		m_isNotifAck = false;
	}
}
