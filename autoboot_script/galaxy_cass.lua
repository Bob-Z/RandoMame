local load_started = false

local function process_frame()
        print(frame_qty)
		if manager.machine.cassettes[":cassette"].is_stopped == false and manager.machine.cassettes[":cassette"].motor_state == true then
		    manager.machine.video.throttled = false
		    manager.machine.video.frameskip = 12
		    load_started = true
		else
		    if load_started == true then
		        emu.keypost('RUN\n')
		        load_started = false
		    end
		    manager.machine.video.throttled = true
		    manager.machine.video.frameskip = 0
		end
end

subscription=emu.add_machine_frame_notifier(process_frame)

emu.keypost('OLD\n')
manager.machine.cassettes[":cassette"]:play()

