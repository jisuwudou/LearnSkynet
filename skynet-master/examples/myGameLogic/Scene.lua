local actors = {}
function init()

	print("One Scene INIT")
end

function response.EnterScene(actor, x, y)
	for i,v in ipairs(actors) do
		if v == actor then
			return false
		end
	end

	actors[#actors] = actor

	return true
end

function response.ExitScene(actor)
	for i,v in ipairs(actors) do
		if v == actor then
			return true
		end
	end
	skynet.error("ExitScene Not Exit ", actor)
	return false
end

function accept.BroadEnter()
	for i,v in ipairs(actors) do
		print("同步 出现在场景",v.PROP.ACTOR_ID,v.agent)
		
	end
end