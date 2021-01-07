local frame_num = 0
local function process_frame()
        frame_num = frame_num + 1

        if frame_num == 40 then
		emu.keypost('BC\n')
        elseif frame_num == 90 then
		emu.keypost('\n')
		elseif frame_num == 190 then
		emu.keypost('LMEM""\n')
		elseif frame_num == 220 then
		manager.machine.cassettes[":cassette"]:play()
        end
end

emu.register_frame_done(process_frame)
