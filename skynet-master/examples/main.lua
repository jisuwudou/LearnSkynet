-- local skynet = require "skynet"
-- local sprotoloader = require "sprotoloader"

-- local max_client = 64

-- skynet.start(function()
-- 	skynet.error("Server start")
-- 	skynet.uniqueservice("protoloader")
-- 	if not skynet.getenv "daemon" then
-- 		local console = skynet.newservice("console")
-- 	end
-- 	skynet.newservice("debug_console",8000)
-- 	skynet.newservice("simpledb")
-- 	local watchdog = skynet.newservice("watchdog")
-- 	skynet.call(watchdog, "lua", "start", {
-- 		port = 9999,
-- 		maxclient = max_client,
-- 		nodelay = true,
-- 	})
-- 	skynet.error("Watchdog listen on", 9999)
-- 	skynet.exit()
-- end)




-- local skynet = require "skynet"

-- skynet.start(function() --skynet.start以function初始化服务
-- 	skynet.error("[Pmain] start")
--  	local ping1 = skynet.newservice("my_ping")
--  	local ping2 = skynet.newservice("my_ping")

--  	skynet.send(ping1, "lua", "testfunc", ping2)

--  	skynet.send(ping1, "lua", "start", ping2)
--  	skynet.exit()
-- end)





-- local skynet = require "skynet"
-- local socket = require "skynet.socket"

-- local clients = {}

-- function connect(fd, addr)
-- 	--启用连接，开始等待接收客户端消息
-- 	print(fd .. " connected addr:" .. addr)
-- 	socket.start(fd)
-- 	clients[fd] = {}
-- 	--消息处理
-- 	while true do
-- 		local readdata = socket.read(fd) --利用协程实现阻塞模式
-- 		--正常接收
-- 		if readdata ~= nil then
-- 			print(fd .. " recv " .. readdata)
-- 			for k,v in pairs(clients) do --广播
-- 				socket.write(k, readdata)
-- 			end
-- 		--断开连接
-- 		else 
-- 			print(fd .. " close ")
-- 			socket.close(fd)
-- 			clients[fd] = nil
-- 		end	
-- 	end
-- end

-- skynet.start(function()
-- 	local listenfd = socket.listen("0.0.0.0", 9999) --监听所有ip，端口8888
-- 	socket.start(listenfd, connect) --新客户端发起连接时，conncet方法将被调用。
-- end)




local skynet = require "skynet"

skynet.start(function() --skynet.start以function初始化服务
	skynet.error("[Pmain] start")

	skynet.newservice("debug_console", 8000)

	local ping1 = skynet.newservice("my_ping")
	local ping2 = skynet.newservice("my_ping")
	local ping3 = skynet.newservice("my_ping")

	skynet.send(ping1, "lua", "start", ping2)
	skynet.send(ping2, "lua", "start", ping3)
	skynet.exit()
end)

