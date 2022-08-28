local skynet = require "skynet"
local snax = require "skynet.snax"


skynet.start(function()


	local loginserver = skynet.newservice("logind")
	local gate = skynet.newservice("gated", loginserver)

	skynet.call(gate, "lua", "open" , {
		port = 8888,
		maxclient = 64,
		servername = "sample",
	})




end)
