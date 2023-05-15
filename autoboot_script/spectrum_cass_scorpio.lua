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

	if manager.machine.cassettes[":cassette"].is_stopped == false and manager.machine.cassettes[":cassette"].motor_state == true then
	    manager.machine.video.throttled = false
	    manager.machine.video.frameskip = 12
	else
	    manager.machine.video.throttled = true
	    manager.machine.video.frameskip = 0
	end
end

subscription=emu.add_machine_frame_notifier(process_frame)



