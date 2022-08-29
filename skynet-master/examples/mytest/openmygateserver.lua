
local skynet = require "skynet"


skynet.start(function ()
	skynet.error("Server start")
	local gateserver = skynet.newservice("mygateserver")
	skynet.call(gateserver, "lua", "open", {
		port=9948,
		maxclient=64,
		nodelay=true,
	})
	skynet.error("gate server setup on ", 9948)
	skynet.exit()
end)