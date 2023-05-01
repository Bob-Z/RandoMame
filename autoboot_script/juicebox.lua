local button = {}
local ports = manager.machine.ioport.ports[":PORTG"]
for field_name, field in pairs(ports.fields) do
    button[field_name] = field
end

local frame_num = 0
local function process_frame()
	frame_num = frame_num + 1

	if frame_num == 1  then
    	button["PLAY"]:set_value(1)
    end
	if frame_num > 50  then
		button["PLAY"]:set_value(0)
	end
end

emu.add_machine_frame_notifier(process_frame)



