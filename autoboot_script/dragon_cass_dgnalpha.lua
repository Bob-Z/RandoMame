local frame_num = 0
local load_done_frame_num = 0
local try_qty = 0
local last_try_frame = 0

local function load_process(start_frame, command)
        if frame_num == start_frame+1 then
            emu.keypost(command)
            manager.machine.cassettes[":cassette"]:play()
        end

        if frame_num > start_frame + 150 then
            if load_done_frame_num == 0 then
                if manager.machine.cassettes[":cassette"].motor_state == false then
                    load_done_frame_num = frame_num
                end
            end
        end

        if load_done_frame_num ~= 0 then
            if frame_num == start_frame + (load_done_frame_num + 30) then
                emu.keypost('RUN\n')
                try_qty = try_qty + 1
                manager.machine.cassettes[":cassette"]:seek(0.0,"set")
                load_done_frame_num = 0
                last_try_frame = frame_num
            end
        end
end

local function process_frame()
        frame_num = frame_num + 1

        if frame_num == 1 then
            emu.keypost('B')
        end

        if frame_num > 200 and try_qty == 0 then
            load_process(200,'CLOAD\n')
        end

        if try_qty == 1 then
            load_process(last_try_frame + 50,'CLOADM\n')
        end
end

emu.register_frame_done(process_frame)
