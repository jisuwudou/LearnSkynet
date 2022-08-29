local skynet = require "skynet"

local socket = require "skynet.socket"

function echo(cID, addr)
    socket.start(cID)
    while true do
        local str = socket.read(cID)
        if str then
            skynet.error("recv " ..str)
            socket.write(cID, string.upper(str))  
        else
            socket.close(cID)
            skynet.error(addr .. " disconnect")
            return
        end
    end
end

local cID, addr = ...
cID = tonumber(cID)

skynet.start(function (  )
    skynet.error("Sokcet Agent Start!!!!!")
	skynet.fork(function (  )
        skynet.error("Sokcet Agent Fork!!!!!")
		echo(cID, addr)
		skynet.exit()
	end)

    skynet.error("Sokcet Agent After!!!!!")
end)