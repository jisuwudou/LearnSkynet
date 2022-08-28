local login = require "snax.loginserver"
local crypt = require "skynet.crypt"
local skynet = require "skynet"
local snax = require "skynet.snax"
local server = {
	-- host = "127.0.0.1",
	-- port = 8001,
	host = "0.0.0.0",
	port = 9947,
	multilogin = false,	-- disallow multilogin
	name = "login_master",
}

local server_list = {}
local user_online = {}
local user_login = {}


local mysqld

function server.auth_handler(token)
	-- the token is base64(user)@base64(server):base64(password)
	skynet.error("logind=== ", token)
	local user, server, password = token:match("([^@]+)@([^:]+):(.+)")
	skynet.error("logind=== ", user, server, password)
	user = crypt.base64decode(user)
	server = crypt.base64decode(server)
	password = crypt.base64decode(password)
	skynet.error("logind=== ", user, server, password)
	-- assert(password == "password", "Invalid password")

	--------------------我的修改，数据库查找对应的密码----------------------

	
	mysqld = snax.queryservice("MyGameMysql")
	skynet.error("snax.queryservice ", mysqld)
	local ret,accountId = mysqld.req.CheckPassword(user, password)
	skynet.error("===auth_handler ", user, type(user),accountId)
	assert(ret, "Invalid password")
	-------------------我的修改-----------------------
	return server, user,accountId
end

function server.login_handler(server, uid, secret, accountId)
	-- print(string.format("%s@%s is login, secret is %s", uid, server, crypt.hexencode(secret)))
	print(string.format("%s@%s is login, secret is %s accountId=%d", uid, server, "加密临时跳过", accountId))

	-- for k,v in pairs(server_list) do
	-- 	print("Logind==server_list=="..k,v, skynet.address(v)) --login/gated
	-- end

	local gameserver = assert(server_list[server], "Unknown server")-- gameserver => login/gated
	-- only one can login, because disallow multilogin
	local last = user_online[uid]
	if last then
		skynet.call(last.address, "lua", "kick", uid, last.subid)
	end
	if user_online[uid] then
		error(string.format("user %s is already online", uid))
	end
	
	local subid = tostring(skynet.call(gameserver, "lua", "login", uid, secret, accountId)) -- 
	user_online[uid] = { address = gameserver, subid = subid , server = server}
	return subid
end

local CMD = {}

function CMD.register_gate(server, address)
	server_list[server] = address
end

function CMD.logout(uid, subid)
	local u = user_online[uid]
	if u then
		print(string.format("%s@%s is logout", uid, u.server))
		user_online[uid] = nil
		
	end
end

function server.command_handler(command, ...)
	local f = assert(CMD[command])
	return f(...)
end

login(server)
