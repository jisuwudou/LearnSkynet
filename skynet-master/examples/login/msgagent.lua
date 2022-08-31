local skynet = require "skynet"
local snax = require "skynet.snax"


skynet.register_protocol {
	name = "client",
	id = skynet.PTYPE_CLIENT,
	unpack = skynet.tostring,
}

local gate
local userid, subid
local user_actor = {}

local CMD = {}
local _entityMgr
local function GetEntityMgr()
	return _entityMgr or snax.queryservice("EntityMgr")
end 

function CMD.login(source, uid, sid, secret, ancountId)
	-- you may use secret to make a encrypted data stream
	skynet.error(string.format("===msgagent== uid:%s is login", uid))
	gate = source
	userid = uid
	subid = sid
	-- you may load user data from database

	mysqld = snax.queryservice("MyGameMysql")
	skynet.error("snax.queryservice ", mysqld)
	local ret,playerInfo = mysqld.req.GetActor(uid, ancountId)

	if ret then
		print("MsgAgent ", 111111111)
		local entityMgr = GetEntityMgr()
		print("MsgAgent ", 222222222, entityMgr)
		createRet = entityMgr.req.createEntity(skynet.self(),1,playerInfo.id, playerInfo.level)
		

		user_actor[userid] = playerInfo.id 
		-- playerInfo.id

		print("MsgAgent ", userid, playerInfo.id)
	end


	skynet.error("==msgagent== login()", ret)
end

local function logout()
	skynet.error("===msgagent logout ===" ,gate)
	if gate then
		skynet.call(gate, "lua", "logout", userid, subid)
	end

	local entityMgr = GetEntityMgr()
	entityMgr.post.removeEntity(user_actor[userid])

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

		local mgr = GetEntityMgr()
		mgr.post.insertMsg(user_actor[userid], systemId, cmd, msg:sub(3))

		print("=================================CLIENT systemId,cmd", systemId,cmd)
		skynet.sleep(10)	-- sleep a while
		skynet.ret(msg)
	end)

	print("==msgagent== start finisth==")
end)
