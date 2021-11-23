local function process_frame()
		if manager.machine.cassettes[":cassette"].is_stopped == false and manager.machine.cassettes[":cassette"].motor_state == true then
		    manager.machine.video.throttled = false
		    manager.machine.video.frameskip = 12
		else
		    manager.machine.video.throttled = true
		    manager.machine.video.frameskip = 0
		end
end

emu.keypost('RUN"\n')
manager.machine.cassettes[":cassette"]:play()

emu.register_frame_done(process_frame)
