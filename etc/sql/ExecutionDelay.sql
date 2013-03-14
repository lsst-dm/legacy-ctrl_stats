# display the delay time (in second) of when a job is submitted and started
select dagNode, executionHost, slotName, submitTime, executionStartTime, UNIX_TIMESTAMP(executionStartTime)-UNIX_TIMESTAMP(submitTime) as delay from submissions
