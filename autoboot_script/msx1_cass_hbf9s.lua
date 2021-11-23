print("tick")

local button = {}
for key, ports in pairs(manager.machine.ioport.ports) do
	for field_name, field in pairs(ports.fields) do
	    button[field_name] = field
	end
end


local frame_num = 0
local function process_frame()
        frame_num = frame_num + 1

        if frame_num == 1 then
		button["Cursor Down"]:set_value(1)
        elseif frame_num == 10 then
		button["Cursor Down"]:set_value(0)
        elseif frame_num == 20 then
		button["Cursor Down"]:set_value(1)
        elseif frame_num == 40 then
		button["Cursor Down"]:set_value(0)
        elseif frame_num == 60 then
		button["Cursor Down"]:set_value(1)
        elseif frame_num == 80 then
		button["Cursor Down"]:set_value(0)
        elseif frame_num == 100 then
		button["Space"]:set_value(1)
        elseif frame_num == 120 then
		button["Space"]:set_value(0)
        elseif frame_num == 200 then
		emu.keypost('RUN"CAS:"\n')
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

