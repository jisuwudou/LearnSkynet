local skynet = require "skynet"

local gateserver = require "snax.gateserver"
local netpack = require "skynet.netpack"
local handler = {}

-- 

function handler.connect(fd, ipaddr)
	skynet.error("ip addr :", ipaddr, "fd = ", fd, "connected!!!")

	gateserver.openclient(fd)
end

function handler.disconnect(fd)
	skynet.error("disconnect!!!!!!!", fd)
end

function handler.message(fd, msg, sz)
	skynet.error("recv message from fd:",fz, msg, sz)
	skynet.error(netpack.tostring(msg, sz))
end

function handler.handshake(id, header, url)
        local addr = websocket.addrinfo(id)
        print("ws handshake from: " .. tostring(id), "url", url, "addr:", addr)
        print("----header-----")
        for k,v in pairs(header) do
            print(k,v)
        end
        print("--------------")


        -- websocket.write(id,"Send by srv,when handshake done!")
    end

function handler.open(source, conf) --testmygateserver
    skynet.error("open by ", skynet.address(source))
    skynet.error("listen on", conf.port)
    skynet.error("client max", conf.maxclient)
    skynet.error("nodelay", conf.nodelay)

    
    print(string.format("accept client socket_id: %s addr:%s", id, addr))
	-- local websocket = require "http.websocket"
    -- local ok, err = websocket.accept(id, handle, protocol, addr)
    -- print("After WB Accept =======",ok, err)
    -- if not ok then
    --     print(err)
    -- end
end
-- ————————————————
-- 版权声明：本文为CSDN博主「吓人的猿」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
-- 原文链接：https://blog.csdn.net/qq769651718/article/details/79435075
skynet.error("mygate server init ", handler.open)
gateserver.start(handler)