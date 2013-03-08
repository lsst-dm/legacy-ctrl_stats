# show the of times a particular slot is used on a each machine.
select executionHost, slotName, COUNT(*) from submissions  GROUP BY executionHost, slotName
