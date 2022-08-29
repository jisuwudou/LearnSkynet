

local skynet = require "skynet"

local sc = require "skynet.socketchannel"

local channel = sc.channel{
	host = "127.0.0.1",
	port = 9948,
}

function response(sock)
	-- body
	return true, sock:read()
end

local function task()
	local resp
	local i = 0
	while(i < 3) do
		--第一参数是需要发送的请求，第二个参数是一个函数，用来接收响应的数据。
        --调用channel:request会自动连接指定的TCP服务，并且发送请求消息。
        --该函数阻塞，返回读到的内容。
		resp = channel:request("data"..i.."\n", response)
		skynet.error("client recv ", resp)
		i = i + 1
	end

	skynet.exit()
end

skynet.start(function ()
	skynet.fork(task)
end)