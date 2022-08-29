local skynet = require "skynet"
local mc = require "skynet.multicast"
local channel


function task()
	local i = 0
	while(i < 100) do
		skynet.sleep(100)
		-- skynet.error("======start publish =======")
		channel:publish("data"..i)
		-- skynet.error("======end publish =======")
		i=i+1
	end

	channel:delete()
	skynet.exit()
end

skynet.start(function ( )
	channel = mc.new()
	skynet.error("new channel ID=", channel.channel)
	skynet.fork(task)
end)