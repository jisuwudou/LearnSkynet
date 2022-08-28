

local skynet = require "skynet"
require "skynet.manager"
local function TestLocal()
	skynet.error("TestLocal")
end

local handler = {}

handler.Buy = function(id,count)
	skynet.error("Buy Some() ", id, count)
	return true
end

skynet.start(function ()
	skynet.dispatch("lua", function(session, address, ...)

		skynet.error("On Recv lua info  ", session, address, skynet.address(address))
		local args = {...}
		for i,v in ipairs(args) do
			skynet.error("arg"..i..":", v,type(v))
		end

		if #args > 0 and handler[args[1]] then
			-- skynet.error("retpack",session)
			skynet.retpack( handler[args[1]](args[2],args[2]))
		else
			skynet.retpack("None Call func")
		end
	end)

	skynet.register(".TestLocal")
end)