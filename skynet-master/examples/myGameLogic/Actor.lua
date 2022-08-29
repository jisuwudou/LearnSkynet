
local GameEnum = require "GameEnum"
local CMD = {}
local ID,LEVEL,NAME,ACCOUNTID

local skynet = require "skynet"

--snax init
function init()

end

function accept.HandleMsg(sys, cmd, msg)

	skynet.error("Actor HandleMsg() ", sys, cmd, msg)
	if sys == GameEnum.ESYS.FIGHT then
		
		-- elseif sys == GameEnum.ESYS.FIGHT

	end

end


function CMD.DB_INIt(info)
	-- [1] = {
 --                ["id"] = 16,
 --                ["level"] = 1,
 --                ["name"] = "你二大爷",
 --                ["accountid"] = 1415,
 --        },
 	ID,LEVEL,NAME,ACCOUNTID = info.id, info.level,info.name,info.accountid
 	print("Actor INIT ", ID,LEVEL,NAME,ACCOUNTID)
end




return CMD;