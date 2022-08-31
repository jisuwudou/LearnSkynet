
local GameEnum = require "GameEnum"
local CMD = {}
local ID,LEVEL,NAME,ACCOUNTID

local skynet = require "skynet"
local snax = require "skynet.snax"



local Cls = {}



function Cls:New(agent, actorId, level)
    local o = {}
    setmetatable(o, {__index = self})


    o.agent = agent
    o.PROP = {
		ACTOR_ID=actorId,
		LEVEL=level,
		NAME = "NO",
		POS_X = 20,
		POS_Y = 20,
		SceneId = 1,
	}


	
    return o
end

function Cls:Init()

	--DB数据初始化后
	self.fubenMgr = snax.queryservice("FubenMgr")
	print("Actor INIT self.fubenMgr=", self.fubenMgr)
	self.fubenMgr.req.EnterScene(self, self.PROP.SceneId, self.PROP.POS_X, self.PROP.POS_Y)


	return true
end

function Cls:Move(x, y)
	skynet.error("move ==== ", x,y)

	self.PROP.POS_X, self.PROP.POS_Y=self.fubenMgr.req.Move(self,x, y)
end


function Cls:HandleMsg(sys, cmd, msg)

	skynet.error("Actor HandleMsg() ", sys, cmd, msg, GameEnum.ECMD_FIGHT.Move)
	if sys == GameEnum.ESYS.FIGHT then
		
		if cmd == GameEnum.ECMD_FIGHT.Move then
			-- print("move ==== msg=", msg)
			local x,y = string.unpack(">i2i2", msg)
			
			self:Move(x, y)

		end

	end

end


function Cls:DB_INIt(info)
	-- [1] = {
 --                ["id"] = 16,
 --                ["level"] = 1,
 --                ["name"] = "你二大爷",
 --                ["accountid"] = 1415,
 --        },
 	ID,LEVEL,NAME,ACCOUNTID = info.id, info.level,info.name,info.accountid
 	print("Actor INIT ", ID,LEVEL,NAME,ACCOUNTID)
end




return Cls;