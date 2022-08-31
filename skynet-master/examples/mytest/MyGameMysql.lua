local skynet = require "skynet"
local mysql = require"skynet.db.mysql"
-- require "skynet.manager"
local db


local function dump(obj)
    local getIndent, quoteStr, wrapKey, wrapVal, dumpObj
    getIndent = function(level)
        return string.rep("\t", level)
    end
    quoteStr = function(str)
        return '"' .. string.gsub(str, '"', '\\"') .. '"'
    end
    wrapKey = function(val)
        if type(val) == "number" then
            return "[" .. val .. "]"
        elseif type(val) == "string" then
            return "[" .. quoteStr(val) .. "]"
        else
            return "[" .. tostring(val) .. "]"
        end
    end
    wrapVal = function(val, level)
        if type(val) == "table" then
            return dumpObj(val, level)
        elseif type(val) == "number" then
            return val
        elseif type(val) == "string" then
            return quoteStr(val)
        else
            return tostring(val)
        end
    end
    dumpObj = function(obj, level)
        if type(obj) ~= "table" then
            return wrapVal(obj)
        end
        level = level + 1
        local tokens = {}
        tokens[#tokens + 1] = "{"
        for k, v in pairs(obj) do
            tokens[#tokens + 1] = getIndent(level) .. wrapKey(k) .. " = " .. wrapVal(v, level) .. ","
        end
        tokens[#tokens + 1] = getIndent(level - 1) .. "}"
        return table.concat(tokens, "\n")
    end
    return dumpObj(obj, 0)
end


function init() 

    skynet.error("======Mysql init========")

    local function on_connect(t_db)
        t_db:query("set charset utf8mb4");
    end

    db=mysql.connect({
        host="127.0.0.1",
        port=3306,
        database="juan_cocos",
        user="root",
        password="123456abc",
        charset="utf8mb4",
        max_packet_size=1024 * 1024,
        on_connect = on_connect
    })

    if not db then
        print("Mysql failed to connect")
    end
    assert(db)
    print("mysql onnect success")

    local res = db:query("create table actors"
        .." (id serial primary key,".."name varchar(10))")
    
    -- local user = 'test2'
    -- local retCreate = db:query("INSERT INTO useraccount values(null, 123,'".. user   .."')")
    -- print(dump(retCreate))
    -- skynet.register("mysqld")
end


function response.CheckPassword(user, checkPass)
    local ret = db:query("select password,accountid from useraccount where account='"..user.."'")
    print(dump(ret))
    -- print("check password",user, checkPass, ret.password)
    if ret.errno then
        print("CheckPassword ERR=", ret.errno, ret.err)
        return false
    else
        if ret[1] --[[and ret[1].password == checkPass 先不验证密码]] then
            return true,ret[1].accountid
        else
            -- skynet.error("==CheckPassword== Not Right #ret=",#ret, checkPass) 
            -- return false
            --没找到账号信息，自动创建
            local retCreate = db:query("INSERT INTO useraccount values(null, 123,'".. user .."')")
            print("Crerate ERR=", retCreate.errno, retCreate.err)
            if retCreate.errno then
                -- assert(retCreate.errno == 0, "Create Account ERR user="..user)
                return false
            else
                return true
            end

        end
    end


    return false
end


--获取玩家基础数据
function response.GetActor(user, accountId)
    local ret = db:query("select * from actors where accountid='"..accountId.."'")
    print("==SQL=== GetActor ",user,dump(ret))
    print("check password",ret.errno)
    if ret.errno then
        print("GetActor ERR=", ret.errno, ret.err, ret[1])
        return false
    else
        if ret[1] --[[and ret[1].password == checkPass 先不验证密码]] then

            -- [1] = {
            --     ["id"] = 16,
            --     ["level"] = 1,
            --     ["name"] = "你二大爷",
            --     ["accountid"] = 1415,
            -- },

            return true,ret[1]
        else

            --没找到信息，自动创建。  
            -- local newId = os.date("%Y%m%d")
            local st = os.date("%Y%m%d")
            print(string.sub(st,3))

            local randomName = {"你大爷","你二大爷","你爷爷"}

            randomName = randomName[math.random(1, #randomName)]

            local retCreate = db:query("INSERT INTO actors values(null,"..accountId.." ,'"..randomName.."',1)")
            print("Crerate ERR=", retCreate.errno, retCreate.err)
            if retCreate.errno then
                -- assert(retCreate.errno == 0, "Create Account ERR user="..user)
                dump(retCreate)
                return false
            else
                print("==============Mysql==============",retCreate)
                -- dump(retCreate)
                -- for k,v in pairs(retCreate) do
                --     print(k,v)
                -- end
                -- affected_rows   1
                -- warning_count   0
                -- server_status   2
                -- insert_id       7

                return true,retCreate[1]
            end

        end
    end


    return false
end