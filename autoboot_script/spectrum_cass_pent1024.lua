local frame_num = 0
local function process_frame()
        frame_num = frame_num + 1

        if frame_num == 100 then
		emu.keypost('a')
        elseif frame_num == 125 then
		emu.keypost('a\n')
        elseif frame_num == 450 then
		emu.keypost('\nj""\n')
		manager:machine().cassettes[":cassette"]:play()
        end
end

emu.register_frame_done(process_frame)

