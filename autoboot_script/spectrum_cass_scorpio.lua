local button = {}
local ports = manager.machine.ioport.ports[":PLUS1"]
for field_name, field in pairs(ports.fields) do
    button[field_name] = field
    print(field_name)
end

local frame_num = 0
local function process_frame()
	frame_num = frame_num + 1

	if frame_num ==  250 then
		button["Cursor Down"]:set_value(1)
	elseif frame_num == 260 then
		button["Cursor Down"]:set_value(0)

	elseif frame_num == 300 then
		emu.keypost('\n\nload ""\n')
                manager.machine.cassettes[":cassette"]:play()
	end
end

emu.register_frame_done(process_frame)



