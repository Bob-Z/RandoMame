local frame_num = 0
local function process_frame()
        frame_num = frame_num + 1

        if frame_num == 1 then
                emu.keypost('Ö')
        elseif frame_num == 15 then
		emu.keypost('TAPE\nRUN"\n\n')
		manager:machine().cassettes[":cassette"]:play()
        end
end

emu.register_frame_done(process_frame)

