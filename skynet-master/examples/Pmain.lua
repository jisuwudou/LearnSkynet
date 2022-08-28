local skynet = require "skynet"
local websocket = require "http.websocket"
local socket = require "skynet.socket"
skynet.start(function() --skynet.start以function初始化服务
	skynet.error("[Pmain] start")

	
 	local handle = {}
 	function handle.connect(id)
        print("ws connect from: " .. tostring(id))
    end

    function handle.handshake(id, header, url)
        local addr = websocket.addrinfo(id)
        print("ws handshake from: " .. tostring(id), "url", url, "addr:", addr)
        print("----header-----")
        for k,v in pairs(header) do
            print(k,v)
        end
        print("--------------")


        -- websocket.write(id,"Send by srv,when handshake done!")
    end

    function handle.message(id, msg, msg_type)
        assert(msg_type == "binary" or msg_type == "text")

        print("----------handle.message----------")
        print(id,msg,msg_type)
        websocket.write(id, msg)
    end

    function handle.ping(id)
        print("ws ping from: " .. tostring(id) .. "\n")
    end

    function handle.pong(id)
        print("ws pong from: " .. tostring(id))
    end

    function handle.close(id, code, reason)
        print("ws close from: " .. tostring(id), code, reason)
    end

    function handle.error(id)
        print("ws error from: " .. tostring(id))
    end

    skynet.trace()

	local protocol = "ws"
    local id = socket.listen("0.0.0.0", 9948)
    skynet.error(string.format("Listen websocket port 9948,protocal:%s",protocol))
    socket.start(id, function (id, addr)

    	local websocket = require "http.websocket"
    	print(string.format("accept client socket_id: %s addr:%s", id, addr))
		
    	local ok, err = websocket.accept(id, handle, protocol, addr)
    	print("After WB Accept =======",ok, err)
        if not ok then
            print(err)
        end


    end)

 	-- skynet.newservice("login/main")
 	-- skynet.newservice("testmysql")
end)


-- skynet.error("111111111111111111111")
-- local skynet = require "skynet"
-- skynet.error("2222222222222222222222")
-- skynet.newservice("login/main")
-- skynet.error("3333333333333333333333")

-- local skynet = require "skynet"
-- -- 
-- skynet.start(function()
--     skynet.error("[Pmain]Server start new ssh client")
--     local gateserver = skynet.newservice("gate") --启动刚才写的网关服务
--     skynet.call(gateserver, "lua", "open", {   --需要给网关服务发送open消息，来启动监听
--         port = 9948,            --监听的端口
--         maxclient = 64,         --客户端最大连接数
--         nodelay = true,         --是否延迟TCP
--     })
-- -- 
--     skynet.error("gate server setup on", 9948)
--     skynet.exit()

	
-- 	-- local gateserver = skynet.newservice("simpleweb") --启动刚才写的网关服务
-- end)
-- ————————————————
-- 版权声明：本文为CSDN博主「吓人的猿」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
-- 原文链接：https://blog.csdn.net/qq769651718/article/details/79435075





------------------ snax.gateserver ------------
-- local mygateserver = require "mygateserver"
-- local skynet = require "skynet"
-- require "skynet.manager"

-- local harbor = require "skynet.harbor"

-- skynet.start(function ()
-- 	skynet.error("======== start mygateserver ========")
-- 	-- local mygateserver = skynet.newservice("mygateserver")
-- 	-- skynet.call(mygateserver, "lua", "open",{
-- 	-- 	port=9948,
-- 	-- 	maxclient=2,
-- 	-- 	nodelay=true
-- 	-- })
-- 	-- skynet.error("gate server setup on", 9948)


-- 	local testsrv1 = skynet.newservice("myTestNewService")

-- 	skynet.name(".TestNameSrv",testsrv1)
-- 	skynet.name("TestNameSrv",testsrv1)
-- 	local ret = skynet.localname(".TestNameSrv")

-- 	local globalRet = harbor.queryname(".TestNameSrv")

-- 	skynet.error("local name = ",ret,skynet.address(ret),skynet.address(globalRet))

-- 	-- local testsrv2 = skynet.newservice("myTestNewService")
-- 	-- local uniqueSrv1 = skynet.uniqueservice("myTestNewService")
-- 	-- local testsrv3 = skynet.newservice("myTestNewService")
-- 	-- local uniqueSrv2 = skynet.uniqueservice("myTestNewService")
-- 	-- local uniqueSrvAllHarbors = skynet.uniqueservice(true,"myTestNewService")
-- 	-- skynet.error("uniqueSrv ",uniqueSrv1,uniqueSrv2)



-- 	--返回当前进程的启动 UTC 时间（秒）。
-- 	skynet.error(skynet.starttime() , skynet.now()/100, skynet.time()   )
	
-- 	--返回当前进程启动后经过的时间 (0.01 秒) 。
-- 	-- skynet.now()
	
-- 	--通过 starttime 和 now 计算出当前 UTC 时间（秒）。
-- 	-- skynet.time()   
-- 	local function aa()
-- 		skynet.error("timout handler")
-- 		skynet.exit()
-- 	end
-- 	skynet.timeout(100,aa)

	
-- end)


-------------------- coroutine ---------
-- local skynet = require "skynet"
-- local cos = {}

-- function task1()
--     skynet.error("task1 begin task")
--     skynet.error("task1 wait")
--     skynet.wait()               --task1去等待唤醒
--     --或者skynet.wait(coroutine.running())
--     skynet.error("task1 end task")
-- end


-- function task2()
--     skynet.error("task2 begin task")
--     skynet.error("task2 wakeup task1")
--     skynet.wakeup(cos[1])           --task2去唤醒task1，task1并不是马上唤醒，而是等task2运行完
--     skynet.error("task2 end task")
-- end

-- function test2( ... )
-- 	skynet.error("On test222():",coroutine.running())
-- 	skynet.wakeup(cos[3])
-- end

-- function test()
-- 	skynet.error("On test():",coroutine.running())
-- 	skynet.timeout(200,test2)
-- 	cos[3] = coroutine.running()
-- 	skynet.sleep(500)
	
-- 	skynet.error("On test():Sleep(500)",coroutine.running())
-- end

-- skynet.start(function ()
--     -- cos[1] = skynet.fork(task1)  --保存线程句柄
--     -- cos[2] = skynet.fork(task2)
--     skynet.timeout(200,test)
-- end)

--[[
[:01000009] task1 begin task
[:01000009] task1 wait
[:01000009] task2 begin task
[:01000009] task2 wakeup task1
[:01000009] task2 end task
[:01000009] task1 end task
[:01000002] KILL self

]]