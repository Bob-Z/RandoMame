local frame_num = 0
local run_frame = 0

local function process_frame()
        frame_num = frame_num + 1

        if frame_num == 30 then
            emu.keypost('GD000\n')
        elseif frame_num == 150 then
		    emu.keypost('LOAD\n')
        elseif frame_num == 300 then
		    manager.machine.cassettes[":cassette"]:play()
		elseif frame_num > 500 then
		    if run_frame == 0 then
		        if manager.machine.cassettes[":cassette"].motor_state == false then
    		        run_frame = frame_num + 60
	    	    end
            elseif frame_num == run_frame then
		        emu.keypost('RUN\n')
		    end
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