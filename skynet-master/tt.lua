local function getMem()
	return  collectgarbage("count")
end
collectgarbage("stop")
local before = getMem()
local a = ""
local after = getMem()
print( (after-before)*1024)

