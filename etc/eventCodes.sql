DROP TABLE IF EXISTS `eventCodes`;
CREATE TABLE `eventCodes` (
  `eventCode` char(3) NOT NULL default '',
  `eventName` char(80) default NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

LOCK TABLES `eventCodes` WRITE;
INSERT INTO `eventCodes` VALUES ('000','Job submitted'),('001','Job executing'),('002','Error in executable'),('003','Job was checkpointed'),('004','Job evicted from machine'),('005','Job Terminated'),('006','Image size of job updated'),('007','Shadow exception'),('008','Generic log event'),('009','Job aborted'),('010','Job was suspended'),('011','Job was unsuspended'),('012','Job was held'),('013','Job was released'),('014','Parallel node executed'),('015','Parallel node terminated'),('016','POST script terminated'),('017','Job submitted to Globus'),('018','Globus submit failed'),('019','Globus resource up'),('020','Detected Down Globus Resource'),('021','Remote error'),('022','Remote system call socket lost'),('023','Remote system call socket reestablished'),('024','Remote system call reconnect failure'),('025','Grid Resource Back Up'),('026','Detected Down Grid Resource'),('027','Job submitted to grid resource'),('028','Job ad information event was triggered'),('029','The job\'s remote status is unknown'),('030','The job\'s remote statis is known again'),('031','unused'),('032','unused'),('033','Attribute update');
UNLOCK TABLES;
