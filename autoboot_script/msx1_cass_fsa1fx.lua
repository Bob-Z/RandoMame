local frame_num = 0
local function process_frame()
        frame_num = frame_num + 1

        if frame_num == 1 then
		emu.keypost('6')
        elseif frame_num == 500 then
		emu.keypost('RUN"CAS:"\n')
        end
end

emu.register_frame_done(process_frame)

