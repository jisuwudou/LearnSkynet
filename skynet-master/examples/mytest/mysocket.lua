local socket = require "skynet.socket"
local skynet = require "skynet"

function echo(cID, addr)
	skynet.error("====echo :", cID, addr)
	socket.start(cID)
	while true do
		local str = socket.read(cID)
		if str then
			skynet.error("=====recv ", str)
			socket.write(cID, "------------------")
			socket.write(cID, "<!DOCTYPE html><html><head><meta charset=\"utf-8\"><title>菜鸟教程(runoob.com)</title></head><body>    <h1>我的第一个标题</h1>    <p>我的第一个段落。</p></body></html>")
		else
			-- socket.close(cID)
			skynet.error(addr ,"finish read ====disconnect===")
			break
		end
	end
end

function echoline(cID, addr)
	skynet.error("====echoline :", cID, addr)
	socket.start(cID)

	socket.write(cID, "----------Server Accepted--------")
	while true do
		local str, endstr = socket.readline(cID)
		if str then
			skynet.error("=====recv line ", str)
			socket.write(cID, "------------------")
			socket.write(cID, "<!DOCTYPE html><html><head><meta charset=\"utf-8\"><title>菜鸟教程(runoob.com)</title></head><body>    <h1>我的第一个标题</h1>    <p>我的第一个段落。</p></body></html>")
		else
			if endstr then
				skynet.error("===========recv line endstr=", endstr)
			end

			socket.close(cID)
			skynet.error(addr ,"finish read ====disconnect===")
			break
		end
	end
end

function accept(cID, addr)

	skynet.error(addr, "Accepted")

	skynet.fork(echo, cID, addr)
	-- skynet.fork(echoline, cID, addr)
	
end

skynet.start(function ()
	local addr = "0.0.0.0:9948"
	skynet.error("listen "..addr)
	local l_id = socket.listen(addr)
	assert(l_id)
	-- socket.start(l_id,accept)
	socket.start(l_id, function(cID, addr)
		skynet.error(addr .. " client accepted")
		skynet.newservice("socketagent", cID, addr)
	end)
end)