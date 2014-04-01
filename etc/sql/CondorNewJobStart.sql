# Counts the number of seconds it takes from the time a job in one slot ends 
# until another job starts in the same slot
select t1.dagNode, t1.executionHost, t1.executionStartTime, t1.executionStopTime, t1.slotName, UNIX_TIMESTAMP(
    (
        select min(t2.executionStartTime) as started
        from totals as t2
        where t2.executionStartTime > t1.executionStopTime
        and t1.executionHost = t2.executionHost
        and t1.slotName = t2.slotName
    )
) - UNIX_TIMESTAMP(t1.executionStopTime) as inSeconds
from totals as t1
