
local GameEnum = require "GameEnum"
local skynet = require "skynet"
local snax = require "skynet.snax"
-- require "skynet.manager"

local Actor = require "Actor"
local entitys = {}

local fubenMgr
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
	-- skynet.register("EntityMgr")
	print("EntityMgr INIT 11")
	-- fubenMgr = snax.queryservice("FubenMgr")
	print("EntityMgr INIT 22")
end

function response.createEntity(agent,type,actorId, level)
	print("EntityMgr 0000000", agent,type,actorId, level)
	if not entitys[type] then
		entitys[type] = {}
	end
	if entitys[type][actorId] then
		skynet.error("EntityMgr re create ", type, actorId)
		return false
	end
	print("EntityMgr 1111111111")
	local actor = Actor:New(agent ,actorId, level)
	if actor:Init() then
		entitys[type][actorId] = actor
	else
		return false
	end
	
	-- local enterRet = fubenMgr.EnterScene(actor, -1, 20, 20)
	-- print("EntityMgr 2222222222", enterRet)
	return true
end

function accept.removeEntity(actorId)
	local entityType = 1--GameEnum.ActorType.Actor
	if entitys[entityType] and entitys[entityType][actorId] then
		entitys[entityType][actorId] = nil
		return true
	else

		skynet.error("======ERRRRRRRR======== EntityMgr,removeentity, when actor not online ", actorId)
		return false
	end

end

function accept.insertMsg(actorId, sys, cmd, msg)
	local type = 1--GameEnum.ActorType.Actor
	if entitys[type] and entitys[type][actorId] then
		entitys[type][actorId]:HandleMsg(sys, cmd, msg)
	else

		skynet.error("======ERRRRRRRR======== recv actor msg, when actor not online ", sys, cmd, msg)
	end

end