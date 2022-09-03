--副本/房间/场景


local skynet = require "skynet"
local snax = require "skynet.snax"

local socketdriver = require "skynet.socketdriver"

local fubenList = {}
local FUBEN_MAX_MEMBER = 4


local FubenStatus = {
	WAITING = 1,
	PLAYING = 2,
}

local function PackFubenInfo(id)

	local fuben = fubenList[id]
	
	if not fuben then
		return
	end

	local memberCnt = #fuben.keybroadInfo
	skynet.error("PackFubenInfo", id, fuben, memberCnt)
	if memberCnt <= 0 then
		return
	end

	local pack
	local fmt = ">BBB"
	local packTable = {}
	packTable[1] = 1
	packTable[2] = 2 --给客户端同步按键信息
	packTable[3] = memberCnt

	for i,v in ipairs(fuben.playerFd) do
		-- print(i,v)
		-- if fuben.playerFd[i] 
		fmt = fmt .. "I4"
		packTable[#packTable + 1] = fuben.keybroadInfo[i] or 0
		skynet.error("Send fd key =", fuben.keybroadInfo[i] or 0)
	end

	fuben.keybroadInfo = {}--重置按键信息
	print("broad =============",fmt, table.unpack(packTable))
	local pack = string.pack(fmt, table.unpack(packTable))
	pack = string.pack(">s2", pack)

	for i,fd in ipairs(fuben.playerFd) do
		socketdriver.send(fd, pack)
	end
	
end

-- local bInterbal = 
function init()
	skynet.error("FubenMgr INIT `````````````")
	-- skynet.timeout(10, function()
	-- 	skynet.error("FubenMgr, timeout ",fubenList)
	-- 	for fubenId,v in ipairs(fubenList) do
	-- 		PackFubenInfo(fubenId)
	-- 	end
	-- end)
	
end

function accept.StartTimer()
	skynet.error("FubenMgr StartTimer()")
	while true do
		skynet.sleep(20)
		-- skynet.error("FubenMgr, timeout ",fubenList)
		-- for fubenId,v in ipairs(fubenList) do
		-- 	PackFubenInfo(fubenId)
		-- end
		for k,v in pairs(fubenList) do
			PackFubenInfo(k)
		end
	end

end

function response.EnterFuben(fd,fubenId)
	skynet.error("fubenMgr EnterFuben()", fd, fubenId)
	if not fubenList[fubenId] then
		fubenList[fubenId] = {
			playerFd={},
			keybroadInfo={},
			status = FubenStatus.WAITING,
		}
	end

	local fubenInfo = fubenList[fubenId]
	local fubenMember = #fubenInfo.playerFd
	if fubenMember >= FUBEN_MAX_MEMBER then
		return false
	end

	table.insert(fubenInfo.playerFd, fd)

	skynet.error("==FubenMgr Enter FUBEN DONE!!!", fd, fubenId)

	return true
end


function accept.LeaveFuben(fd)


end

function response.CommitPlayerKeys(fd, fubenId, player_keys)
	local fuben = fubenList[fubenId]
	if not fuben then
		return false
	end

	-- for _,v in pairs(fuben) do
	-- 	print(v)
	-- 	if type(v) == "table" then

	-- 	for k2,v in pairs(v) do
	-- 		print(k2,v)
	-- 	end
	-- end
	-- end

	for i,v in ipairs(fuben.playerFd) do
		if fd == v then
			fuben.keybroadInfo[i] = player_keys
			print("commit ",i, fubenId, player_keys)
			return true
		end
	end

	return false
end

