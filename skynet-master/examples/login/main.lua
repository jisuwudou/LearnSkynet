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

	snax.uniqueservice("EntityMgr")
	snax.uniqueservice("FubenMgr")
end)
