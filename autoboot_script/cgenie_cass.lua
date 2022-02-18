local frame_num = 0
local is_cload = false
local is_system = false
local  keypost_run_frame_num = -1
local system_cmd = nil
local throttle_asked = 0
local throttle_qty = 0
local mem_size = nil

local function process_frame()
    frame_num = frame_num + 1

    if frame_num == 100 then
        if is_cload == true then
            emu.keypost("CLOAD" .. '\n')
        end
        if is_system == true then
            emu.keypost("SYSTEM" .. '\n')
        end
    elseif frame_num == 150 then
        if is_system == true then
            emu.keypost(system_cmd .. '\n')
        end
    elseif frame_num == 200 then
        manager.machine.cassettes[":cassette"]:play()
    end

    manage_frame(frame_num)
end

function manage_frame(frame_num)
    if manager.machine.cassettes[":cassette"].is_stopped == false then
        if throttle_asked == 0 then
            throttle_qty = throttle_qty + 1
            throttle_asked = 1

            manager.machine.video.throttled = false
            manager.machine.video.frameskip = 12
        end
    else
        if throttle_asked == 1 then
            throttle_asked = 0

            manager.machine.video.throttled = true
            manager.machine.video.frameskip = 0

            if throttle_qty == 1 then
                keypost_run_frame_num = frame_num + 10
            end
        end
    end

    if frame_num == keypost_run_frame_num then
        if is_cload == true then
            print("RUN")
            emu.keypost("RUN\n")
        elseif is_system == true then
            print("/")
            emu.keypost("/\n")
        end
    end
end

info_usage = os.getenv("RANDOMAME_INFO_USAGE")

if info_usage ~= nil and info_usage ~= "" then
    if string.find(info_usage, "CLOAD") ~= nil then
        print("CLOAD")
        is_cload = true
    elseif string.find(info_usage, "SYSTEM") ~= nil then
        print("SYSTEM")
        system_cmd=string.match(info_usage,'.*ype SYSTEM and load with (.*),')
        if system_cmd == nil then
            system_cmd=string.match(info_usage,'.*ype SYSTEM and load with (.*) %(')
            if system_cmd == nil then
                system_cmd=string.match(info_usage,'.*ype SYSTEM and load with (.*)$')
            end
        end

        print("Command: " .. system_cmd)
        is_system = true
    end
end

emu.keypost('\n')

emu.register_frame_done(process_frame)
