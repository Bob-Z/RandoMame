local button = {}
local ports = manager:machine():ioport().ports[":kbrow.2"]
for field_name, field in pairs(ports.fields) do
    button[field_name] = field
    print(field_name)
end

button["Shift"]:set_value(1)


local frame_num = 0
local function process_frame()
        frame_num = frame_num + 1

        if frame_num == 75 then
		button["Shift"]:set_value(0)
		emu.keypost('|TAPE\nRUN"\n\n')
		manager:machine().cassettes[":cassette"]:play()
        end
end

emu.register_frame_done(process_frame)

