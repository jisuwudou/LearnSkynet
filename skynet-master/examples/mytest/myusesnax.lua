local skynet = require "skynet"

local snax = require "skynet.snax"

function init(...)
	local obj = snax.newservice("mysimplesnax")
	skynet.error("new snax ", obj)

	local ret = obj.req.GET()
	local retPost = obj.post.SET(2344)
	skynet.error("new snax REQ()", ret, retPost)


	local uniqueObj = snax.uniqueservice("mysimplesnax", "")
	local uniqueObj2 = snax.uniqueservice("mysimplesnax", "")
	local obj2 = snax.newservice("mysimplesnax")

	skynet.error("new snax srv ", uniqueObj, uniqueObj2, obj2)


	obj.post.hello("更新测试11111")

	local r = snax.hotfix(obj, [[

		function accept.hello(...)
			--skynet.error("fix skynet.error")
            print("fix hello", i, gname, ...) --skynet.error不能用了
        end
		]])

	obj.post.hello("更新测试22222")


	local r1 = snax.hotfix(obj, [[
		local i
		local skynet
		function accept.hello(...)
            skynet.error("fix hello", i, gname, ...) --skynet.error不能用了
        end
		]])

	obj.post.hello("更新测试33333",r1)

	obj.post.quit()

	snax.kill(obj)

	skynet.exit()
end