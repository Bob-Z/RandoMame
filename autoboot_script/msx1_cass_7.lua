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
        print('7')
        io[':KEY0,128,49']:set_value(1)
    elseif frame_num == 200 then
        io[':KEY0,128,49']:set_value(0)
    elseif frame_num > 900 then
        msx1_cass_base.post_command(frame_num, command)
    end

    msx1_cass_base.manage_frame(frame_num, is_run_required)
end

command, is_run_required = msx1_cass_base.get_command()
io = io_base.get()

subscription=emu.add_machine_frame_notifier(process_frame)

