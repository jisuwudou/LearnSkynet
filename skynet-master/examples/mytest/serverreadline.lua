local skynet    = require "skynet"
local socket    = require "skynet.socket"

--简单echo服务
function echo(cID, addr)
    socket.start(cID)
    while true do
        local str = socket.readline(cID)
        if str then
            skynet.fork(function()
                skynet.error("SRV:recv " ..str)
                skynet.sleep(math.random(1, 5) * 100)
                socket.write(cID, string.upper(str) .. "\n")
            end)
        else
            socket.close(cID)
            skynet.error(addr .. " disconnect")
            return
        end
    end
end

function accept(cID, addr)
    skynet.error(addr .. " accepted")
    skynet.fork(echo, cID, addr)
end

--服务入口
skynet.start(function()
    local addr = "0.0.0.0:9948"
    skynet.error("listen " .. addr)
    local lID = socket.listen(addr)
    assert(lID)
    socket.start(lID, accept)
end)
