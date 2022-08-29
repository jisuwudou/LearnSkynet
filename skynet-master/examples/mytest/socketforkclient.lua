local skynet    = require "skynet"
local socket    = require "skynet.socket"

local function recv(id)
    skynet.error("Start Recv id=", id)
   local i = 0
   while(i < 3) do
    local str = socket.readline(id)
    skynet.error("socket.readline str=", str)
    if str then
            skynet.error("CLIENT:recv " .. str)
    else
            skynet.error("disconnect")
    end
    i = i + 1
   end
   socket.close(id)       --未接收完不要关闭
   skynet.exit()
end

local function send(id)    --不用管有没接受到数据直接发送三次
    skynet.error("Start send id=", id)
    local i = 0
    while(i < 3) do
    skynet.error("send data"..i)
    socket.write(id, "data"..i.."\n")
        i = i + 1
    end
end

skynet.start(function()
    local addr = "127.0.0.1:9948"
    skynet.error("connect ".. addr)
    local id  = socket.open(addr)
    assert(id)
    --启动读协程
    skynet.fork(recv, id)
    --启动写协程
    skynet.fork(send, id)
end)
