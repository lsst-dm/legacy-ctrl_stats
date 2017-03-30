CREATE TABLE IF NOT EXISTS `updates` (
  `id` int(11) unsigned NOT NULL auto_increment,
  `condorId` varchar(24) default NULL,
  `dagNode` varchar(80) default NULL,
  `executionHost` varchar(80) default NULL,
  `slotName` varchar(10) default NULL,
  `utctimestamp` datetime default NULL,
  `imageSize` int(11) default NULL,
  `memoryUsageMb` int(11) default NULL,
  `residentSetSizeKb` int(11) default NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
