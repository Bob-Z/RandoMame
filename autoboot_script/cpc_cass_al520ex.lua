local button = {}
local ports = manager.machine.ioport.ports[":kbrow.2"]
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
		manager.machine().cassettes[":cassette"]:play()
        end

		if manager.machine.cassettes[":cassette"].is_stopped == false and manager.machine.cassettes[":cassette"].motor_state == true then
		    manager.machine.video.throttled = false
		    manager.machine.video.frameskip = 12
		else
		    manager.machine.video.throttled = true
		    manager.machine.video.frameskip = 0
        end
end

emu.register_frame_done(process_frame)

