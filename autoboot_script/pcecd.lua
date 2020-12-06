local button = {}
local ports = manager:machine():ioport().ports[":JOY_P.0"]
for field_name, field in pairs(ports.fields) do
    button[field_name] = field
end

local frame_num = 0
local function process_frame()
	frame_num = frame_num + 1

	if frame_num < 25 then
		button["P1 Run"]:set_value(1)
	else
		button["P1 Run"]:set_value(0)
	end
end

emu.register_frame_done(process_frame)



