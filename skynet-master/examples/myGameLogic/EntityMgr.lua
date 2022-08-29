
local GameEnum = require "myGameLogic.GameEnum"
local skynet = require "skynet"
require "skynet.manager"
local entitys = {}


local function RunTime()
	for _,entitys in ipairs(entitys) do
		for k,v in pairs(entitys) do
			print(k,v)
		end
	end

end

function init()

	skynet.error("ENTITYMGR INIT ")
	skynet.timeout(10, RunTime)
	skynet.register("EntityMgr")
end

function response.createEntity(type,actorId, ...)
	if not entitys[type] then
		entitys[type] = {}
	end
	if entitys[type][actorId] then
		skynet.error("EntityMgr re create ", type, actorId)
		return false
	end

	entitys[type][actorId] = {}
	entitys[type][actorId].level = level

	local actorService = snax.newservice("Actor", actorId, ...)
	entitys[type][actorId].service = actorService
end

function accept.removeEntity(actorId)
	local entityType = GameEnum.ActorType.Actor
	if entitys[entityType] and entitys[entityType][actorId] then
		entitys[entityType][actorId] = nil
		return true
	else

		skynet.error("======ERRRRRRRR======== EntityMgr,removeentity, when actor not online ", actorId)
		return false
	end

end

function accept.insertMsg(uid, sys, cmd, msg)
	local type = GameEnum.ActorType.Actor
	if entitys[type] and entitys[type][uid] then
		entitys[type][uid].post.HandleMsg(sys, cmd, msg)
	else

		skynet.error("======ERRRRRRRR======== recv actor msg, when actor not online ", sys, cmd, msg)
	end

end