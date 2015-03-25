package org.opennms.netmgt.utils;

import java.util.ArrayList;
import java.util.List;

import org.opennms.core.utils.BeanUtils;
import org.opennms.core.utils.ThreadCategory;
import org.opennms.netmgt.dao.AlarmDao;
import org.opennms.netmgt.dao.NotificationDao;
import org.opennms.netmgt.model.OnmsAcknowledgment;
import org.opennms.netmgt.model.OnmsAcknowledgmentCollection;
import org.opennms.netmgt.model.OnmsAlarm;
import org.opennms.netmgt.model.OnmsNotification;
import org.opennms.netmgt.model.acknowledgments.AckService;
import org.opennms.netmgt.xml.event.Event;
import org.springframework.beans.factory.access.BeanFactoryReference;
import org.springframework.transaction.PlatformTransactionManager;
import org.springframework.transaction.annotation.Transactional;

public class Acknowledger {
	private List<AcknowledgePolicy> m_ackpolicies=  new ArrayList<AcknowledgePolicy>();

	private AlarmDao m_alarmDao;

    private NotificationDao m_notificationDao;
    
    private AckService m_ackService;

    private PlatformTransactionManager m_transactionManager;

    private ThreadCategory log;

    public Acknowledger() {
        log=ThreadCategory.getInstance(this.getClass());
        log.debug("Acknowledger Session Constructor: loaded");
        BeanFactoryReference bf = BeanUtils.getBeanFactory("daoContext");
        m_alarmDao = BeanUtils.getBean(bf,"alarmDao", AlarmDao.class);
        m_notificationDao = BeanUtils.getBean(bf,"notificationDao", NotificationDao.class);
        m_transactionManager = BeanUtils.getBean(bf,"transactionManager", PlatformTransactionManager.class);
        
        BeanFactoryReference bfn = BeanUtils.getBeanFactory("ackdContext");
        m_ackService = BeanUtils.getBean(bfn,"ackService", AckService.class);

    }

    public AlarmDao getAlarmDao() {
		return m_alarmDao;
	}

	public void setAlarmDao(AlarmDao alarmDao) {
		m_alarmDao = alarmDao;
	}

	public NotificationDao getNotificationDao() {
		return m_notificationDao;
	}

	public void setNotificationDao(NotificationDao notificationDao) {
		m_notificationDao = notificationDao;
	}

	public AckService getAckService() {
		return m_ackService;
	}

	public void setAckService(AckService ackService) {
		m_ackService = ackService;
	}

	public PlatformTransactionManager getTransactionManager() {
		return m_transactionManager;
	}

	public void setTransactionManager(PlatformTransactionManager transactionManager) {
		m_transactionManager = transactionManager;
	}

	public void addAcknowledgePolicy(AcknowledgePolicy ackexec) {
		m_ackpolicies.add(ackexec);
		log.debug("AcknowlodgePolicy added: " + ackexec);
	}
	
	public List<AcknowledgePolicy> getAckPolicies() {
		return m_ackpolicies;
	}

	public void flushEvent(Event event){
		for (AcknowledgePolicy ackpolicy: m_ackpolicies) {
			if (ackpolicy.match(event)) {
				m_ackService.processAcks(getAcks(event,ackpolicy));
			}
		}
	}

	public  OnmsAcknowledgmentCollection getAcks(Event event, AcknowledgePolicy policy) {
		if (policy.isNotifAck())
			return getNotifications(event, policy);
		return getAlarms(event, policy);
	}

	@Transactional
	protected OnmsAcknowledgmentCollection getAlarms(Event event, AcknowledgePolicy policy) {
		OnmsAcknowledgmentCollection coll = new OnmsAcknowledgmentCollection(); 
		for (OnmsAlarm alarm: m_alarmDao.findMatching(policy.getCriteria(event))) {
			if (policy.matchParameters(event, alarm.getLastEvent())) {
				OnmsAcknowledgment 	ack = new OnmsAcknowledgment(alarm);
				ack.setAckAction(policy.getAckAction());
				coll.add(ack);
			}
		}
		return coll;
	}
	
	@Transactional
	protected OnmsAcknowledgmentCollection getNotifications(Event event, AcknowledgePolicy policy) {
		OnmsAcknowledgmentCollection coll = new OnmsAcknowledgmentCollection(); 
		for (OnmsNotification notif: m_notificationDao.findMatching(policy.getCriteria(event))) {
			if (policy.matchParameters(event, notif.getEvent())) {
				OnmsAcknowledgment 	ack = new OnmsAcknowledgment(notif);
				ack.setAckAction(policy.getAckAction());
				coll.add(ack);
			}
		}
		return coll;
	}

}
