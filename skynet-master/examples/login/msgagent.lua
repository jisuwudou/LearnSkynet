local skynet = require "skynet"
local snax = require "skynet.snax"
skynet.register_protocol {
	name = "client",
	id = skynet.PTYPE_CLIENT,
	unpack = skynet.tostring,
}

local gate
local userid, subid

local CMD = {}

function CMD.login(source, uid, sid, secret, ancountId)
	-- you may use secret to make a encrypted data stream
	skynet.error(string.format("===msgagent== uid:%s is login", uid))
	gate = source
	userid = uid
	subid = sid
	-- you may load user data from database

	mysqld = snax.queryservice("MyGameMysql")
	skynet.error("snax.queryservice ", mysqld)
	local ret = mysqld.req.GetActor(uid, ancountId)

	skynet.error("==msgagent== login()", ret)
end

local function logout()
	skynet.error("===msgagent logout ===" ,gate)
	if gate then
		skynet.call(gate, "lua", "logout", userid, subid)
	end
	skynet.exit()
end

function CMD.logout(source)
	-- NOTICE: The logout MAY be reentry
	skynet.error(string.format("%s is logout", userid))
	logout()
end

function CMD.afk(source)
	-- the connection is broken, but the user may back
	skynet.error(string.format("AFK: the connection is broken, but the user may back"))
end

skynet.error("==msgagent== lua init=========")

skynet.start(function()
	-- If you want to fork a work thread , you MUST do it in CMD.login
	print("==msgagent== start begin==")
	skynet.dispatch("lua", function(session, source, command, ...)
		local f = assert(CMD[command])

		skynet.error("[msgagent]== recv Type:lua",session, source,  command,... )

		skynet.ret(skynet.pack(f(source, ...)))
	end)

	skynet.dispatch("client", function(_,_, msg)
		-- the simple echo service

		-- skynet.error("[msgagent]== recv Type:client", msg)
		local systemId,cmd = string.unpack(">BB", msg)
		print("=================================CLIENT systemId,cmd", systemId,cmd)
		skynet.sleep(10)	-- sleep a while
		skynet.ret(msg)
	end)

	print("==msgagent== start finisth==")
end)
