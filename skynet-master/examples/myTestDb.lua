local skynet = require "skynet"

require "skynet.manager"

local command = {}
local db = {}
function command.GET(key )
	return db[key]
end

function command.SET(key, value)
	db[key] = value
end

skynet.start(function()
	skynet.dispatch("lua", function (session, address, cmd,...)
		cmd = cmd:upper()

		local f = command[cmd]
		if f then
			skynet.retpack(f(...))
		else
			skynet.error(string.format("Unkonow command %s", tostring(cmd)))
		end
	end)

	skynet.register ".mydb"
end)