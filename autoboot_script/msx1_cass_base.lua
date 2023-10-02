local msx1_cass_base = {}

local throttle_qty = 0
local throttle_asked = 0
local keypost_run_frame_num = 0
local command_index = 1
local command_frame_num = -1
local default_command_list = {'\nRUN"CAS:"\n', '\nRUN@CAS\'@\n', '\nRUN@CAS>@\n', '\nRUN3cqs.3\n', '\nRUN"CAS~"\n' }

function msx1_cass_base.get_command()
    is_run_required = false

    info_usage = os.getenv("RANDOMAME_INFO_USAGE")

    if info_usage ~= nil and info_usage ~= "" then
        command = string.gsub(info_usage,"Load with ", "")
        command = string.gsub(command,". The game requires 64k in slot 2","")
        command = command .. '\n'
    else
        command = default_command_list
    end

    if command == "CLOAD + RUN\n" then
        command = {'\nCLOAD\n','\nCLOQD\n'}
        is_run_required = true
    end

    if command == 'RUN"CAS:"\n' then
        command = default_command_list
    end

    if command == 'BLOAD"CAS:",R\n' then
        command = {'\nBLOAD"CAS:",R\n', '\nBLOAD@CAS\'@,R\n','\nbloqd3cqs.3mR\n','\nBLOAD@CAS>@,R\n', '\nBLOAD"CAS~",R\n',}
    end

    return command, is_run_required
end

function msx1_cass_base.manage_frame(frame_num, is_run_required)
    if manager.machine.cassettes[":cassette"].is_stopped == false and manager.machine.cassettes[":cassette"].motor_state == true then
        if throttle_asked == 0 then
            throttle_qty = throttle_qty + 1
            throttle_asked = 1

            manager.machine.video.throttled = false
            manager.machine.video.frameskip = 12
        end
    else
        if throttle_asked == 1 then
            throttle_asked = 0

            manager.machine.video.throttled = true
            manager.machine.video.frameskip = 0

            if throttle_qty == 1 and is_run_required == true then
                keypost_run_frame_num = frame_num + 100
            end
        end
    end

    if frame_num == keypost_run_frame_num then
        emu.keypost("RUN\n\nRUN\n\n")
    end
end

function msx1_cass_base.post_command(frame_num, command)
    if command_frame_num == -1 then
        command_frame_num = frame_num
    end

    if command_index <= #command and command_frame_num == frame_num then
        print(command[command_index])
        emu.keypost(command[command_index])
        command_index = command_index + 1
        command_frame_num = command_frame_num + 180
    end
end

return msx1_cass_base
