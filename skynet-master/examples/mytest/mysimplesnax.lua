local snax = require "skynet.snax"
local skynet = require "skynet"
local i = 10
gname = "nengzhong"

function init( ... )
	skynet.error("snax init", ...)
end

function exit(...)
	skynet.error("snax exit ", ...)


end

function accept.quit( ... )
	snax.exit()
end

function response.GET( ... )
	return 123
end

function accept.SET(v)
	skynet.error("accept, SET ", v)
end




function accept.hello(...) --通过obj.post.hello
    skynet.error("hello", i,  gname, ...)
end