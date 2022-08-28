local skynet = require "skynet" 
-- ​
local args = { ... }
if(#args == 0) then
    table.insert(args, "uniqueservice")
end
skynet.start(function()
    local us
    skynet.error("start query service")
    --如果test服务未被创建，该接口将会阻塞，后面的代码将不会执行
    if ( #args == 2 and args[1] == "true" )  then
        us = skynet.queryservice(true, args[2])
    else
        us = skynet.queryservice(args[1])  
    end
    skynet.error("end query service handler:", skynet.address(us))
end)
-- ​
-- ————————————————
-- 版权声明：本文为CSDN博主「吓人的猿」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
-- 原文链接：https://blog.csdn.net/qq769651718/article/details/79432858