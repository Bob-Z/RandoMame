local frame_num = 0
local function process_frame()
        frame_num = frame_num + 1
        if frame_num == 1 then
            manager.machine.cassettes[":cassette"]:stop()
        end
        if frame_num == 150 then
            manager.machine.cassettes[":cassette"]:play()
		    emu.keypost('CLOAD""\n')
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
