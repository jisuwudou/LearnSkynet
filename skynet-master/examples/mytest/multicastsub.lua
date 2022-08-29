local channel
local channelID = ...

channelID = tonumber(channelID)

local skynet = require "skynet"
local mc = require "skynet.multicast"

local function recvChannel(channel, source, msg, ...)
	-- skynet.error("channel")
	skynet.error("channel ID:", channel.channel, "source:", source, skynet.address(source), msg)
end


skynet.start(function ()
	skynet.error("Bind channelid=", channelID, type(channelID))
	channel = mc.new {
		channel = channelID,
		dispatch = recvChannel,
	}
	channel:subscribe()
	skynet.timeout(500, function() channel:unsubscribe() end)
end) 