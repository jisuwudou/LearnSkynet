


local skynet = require "skynet"
local snax = require "skynet.snax"

local sceneList = {}

function init()
	print("fubenmgr init")
	sceneList = {#sceneList, snax.newservice("Scene")}
	print("fubenmgr init")
end

function response.EnterScene(actor, sceneId, x, y)
	if sceneId == -1 then
		sceneId = 1
	end

	if actor.PROP.SceneId == sceneId then
		skynet.error("FubenMgr, enter same scene ", sceneId)
		return true
	end

	local scene = sceneList[sceneId]
	local ret = false
	if scene then
		ret=scene.req.EnterScene(actor, x, y)
		if ret then
			ret=scene.req.ExitScene(actor)

		end
	end
	print("fubenmgr EnterScene ",actor, sceneId, x, y)

	return ret
end


function response.Move(self,x, y)
	self.PROP.Scene
	return x, y
end