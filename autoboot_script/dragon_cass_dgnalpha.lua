local frame_num = 0
local load_done_frame_num = 0
local function process_frame()
        frame_num = frame_num + 1

        if frame_num == 1 then
            emu.keypost('B')
        end

        if frame_num == 200 then
            emu.keypost('CLOAD\n')
            manager.machine.cassettes[":cassette"]:play()
        end

        if frame_num > 350 then
            if load_done_frame_num == 0 then
                if manager.machine.cassettes[":cassette"].motor_state == false then
                    load_done_frame_num = frame_num
                end
            end
        end

        if load_done_frame_num ~= 0 then
            if frame_num == (load_done_frame_num + 30) then
                emu.keypost('RUN\n')
            end
        end
end

emu.register_frame_done(process_frame)
