local frame_num = 0
local wait_for_cload = false
local ready_for_run = false
local bload_frame = -1

local function process_frame()
        frame_num = frame_num + 1

        if frame_num == 1 then
		    emu.keypost('CLOAD\n')
		    manager.machine.cassettes[":cassette"]:play()
		    wait_for_cload = true
		end

		if wait_for_cload == true and manager.machine.cassettes[":cassette"].motor_state == true then
		    wait_for_cload = false
		    ready_for_run = true
		end

		if ready_for_run == true and manager.machine.cassettes[":cassette"].motor_state == false then
		    ready_for_run = false
            bload_frame = frame_num + 50
		    emu.keypost('RUN\n')
		end

		if bload_frame == frame_num and manager.machine.cassettes[":cassette"].motor_state == false then
		    manager.machine.cassettes[":cassette"]:seek(0.0,"set")
		    emu.keypost('BLOAD "CAS:",R\n')
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

emu.add_machine_frame_notifier(process_frame)

