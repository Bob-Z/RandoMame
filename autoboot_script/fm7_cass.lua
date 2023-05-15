local frame_num = 0
local load_done_frame_num = 0
local motor_state_false_frame_num = 0
local function process_frame()
        frame_num = frame_num + 1

        if frame_num == 1 then
            emu.keypost('LOAD\n')
            manager.machine.cassettes[":cassette"]:play()
        end

        if frame_num > 150 then
            if motor_state_false_frame_num == 0 then
                if manager.machine.cassettes[":cassette"].motor_state == false then
                    motor_state_false_frame_num = frame_num
                end
            else
                if frame_num > motor_state_false_frame_num + 60 then
                    if load_done_frame_num == 0 then
                        load_done_frame_num = frame_num
                        emu.keypost('RUN\n')
                    end
                end
            end
        end

        if manager.machine.cassettes[":cassette"].motor_state == true then
            motor_state_false_frame_num = 0
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
