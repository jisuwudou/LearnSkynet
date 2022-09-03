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
local client_fd --ps
local curFubenId--ps

local CMD = {}
local _entityMgr
local function GetEntityMgr()
	if not _entityMgr then
		_entityMgr = snax.queryservice("EntityMgr")
	end
	return _entityMgr  
end 

local function GetFubenMgr()
	if not _fubenMgr then
		skynet.error(" GetFubenMgr 111")
		_fubenMgr = snax.queryservice("FubenMgr")
		skynet.error(" GetFubenMgr 222")
	end
	return _fubenMgr  
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
		-- local entityMgr = GetEntityMgr()
		-- createRet = entityMgr.req.createEntity(skynet.self(),1,playerInfo.id, playerInfo.level)
		

		-- user_actor[userid] = playerInfo.id 
		-- playerInfo.id

		print("MsgAgent ", userid, playerInfo.id)
	end


	skynet.error("==msgagent== login()", ret)
end

function CMD.setfd(source, fd)
	client_fd = fd
end

local function logout()
	skynet.error("===msgagent logout ===" ,gate)
	if gate then
		skynet.call(gate, "lua", "logout", userid, subid)
	end

	-- local entityMgr = GetEntityMgr()
	-- entityMgr.post.removeEntity(user_actor[userid])
	curFubenId = nil
	client_fd = nil
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

-- skynet.error("==msgagent== lua init=========")

skynet.start(function()
	-- If you want to fork a work thread , you MUST do it in CMD.login
	-- print("==msgagent== start begin==")
	skynet.dispatch("lua", function(session, source, command, ...)
		local f = assert(CMD[command])

		skynet.error("[msgagent]== recv Type:lua",session, source,  command,... )

		skynet.ret(skynet.pack(f(source, ...)))
	end)

	skynet.dispatch("client", function(_,_,  msg)
		-- the simple echo service
		-- client_fd = fd
		-- skynet.error("[msgagent]== recv Type:client", msg)
		local systemId,cmd = string.unpack(">BB", msg)
		-- skynet.error("MsgAgent=============================CLIENT systemId,cmd", client_fd, systemId,cmd)
		if systemId == 1 then
			if cmd == 1 then --进入房间
				local fubenId = string.unpack(">I2",msg:sub(3))
				
				local fubenMgr = GetFubenMgr()
				skynet.error("call fubegmr ", fubenMgr)
				local ret = fubenMgr.req.EnterFuben(client_fd, fubenId)
				skynet.error("玩家进入房间 ",fubenId, ret)
				if ret then
					curFubenId = fubenId
				end
			elseif cmd == 2 then --同步按键状态
				local player_keys = string.unpack(">I4",msg:sub(3))

				if not curFubenId then
					skynet.error("ERRRRR commit player_keys curFubenId=nil")
					return
				end
				skynet.error("同步按键状态 ",player_keys)
				local fubenMgr = GetFubenMgr()
				fubenMgr.req.CommitPlayerKeys(client_fd, curFubenId,player_keys)
			end
		end

		
		-- skynet.sleep(10)	-- sleep a while
		skynet.ret(msg)
	end)

	-- print("==msgagent== start finisth==")
end)
