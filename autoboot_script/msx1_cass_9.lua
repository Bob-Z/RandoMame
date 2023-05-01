package.path = './autoboot_script/?.lua;' .. package.path

msx1_cass_base = require("msx1_cass_base")
io_base = require("io_base")

local frame_num = 0
local command = nil
local is_run_required = false
local io = nil

local function process_frame()
    frame_num = frame_num + 1

    if frame_num == 1 then
        -- Key 9
        io[':KEY0,512,49']:set_value(1)
    elseif frame_num == 10 then
        -- Key 9
        io[':KEY0,512,49']:set_value(0)
    elseif frame_num == 100 then
        emu.keypost('\n')
    elseif frame_num > 600 then
        msx1_cass_base.post_command(frame_num, command)
    end

    msx1_cass_base.manage_frame(frame_num, is_run_required)
end

command, is_run_required = msx1_cass_base.get_command()
io = io_base.get()

emu.add_machine_frame_notifier
