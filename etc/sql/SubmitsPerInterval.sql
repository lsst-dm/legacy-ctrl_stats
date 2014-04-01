# submits per interval
select submitTime, count(*) as count from submissions group by submitTime
