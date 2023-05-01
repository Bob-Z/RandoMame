package.path = './autoboot_script/?.lua;' .. package.path

msx1_cass_base = require("msx1_cass_base")

local frame_num = 0
local command = nil
local is_run_required = false

local function process_frame()
    frame_num = frame_num + 1

    if frame_num == 1 then
        emu.keypost('2')
    elseif frame_num > 250 then
        msx1_cass_base.post_command(frame_num, command)
    end

    msx1_cass_base.manage_frame(frame_num, is_run_required)
end

command, is_run_required = msx1_cass_base.get_command()

emu.add_machine_frame_notifier
