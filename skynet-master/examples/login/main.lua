local skynet = require "skynet"
local snax = require "skynet.snax"
skynet.start(function()
	
	local db = snax.uniqueservice("MyGameMysql")

	local loginserver = skynet.newservice("login/logind")

	local gate = skynet.newservice("login/gated", loginserver)

	skynet.call(gate, "lua", "open" , {
		-- port = 8889,
		port = 9948,
		maxclient = 64,
		servername = "cocos1",
	})

	ser =snax.uniqueservice("EntityMgr")
	print("main.........",ser)
	sss=snax.queryservice("EntityMgr")
	print("main.........",sss)
	skynet.error("login main 77777777777777777")
end)
