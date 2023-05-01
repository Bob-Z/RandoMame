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
        print("Start Cursor down")
        io[':KEY4,64,49']:set_value(1)
    elseif frame_num == 10 then
        print("Stop Cursor down")
        io[':KEY4,64,49']:set_value(0)
    elseif frame_num == 40 then
        print("Start Cursor down")
        io[':KEY4,64,49']:set_value(1)
    elseif frame_num == 50 then
        print("Stop Cursor down")
        io[':KEY4,64,49']:set_value(0)
    elseif frame_num == 80 then
        print("Start Cursor down")
        io[':KEY4,64,49']:set_value(1)
    elseif frame_num == 90 then
        print("Stop Cursor down")
        io[':KEY4,64,49']:set_value(0)

    elseif frame_num == 120 then
        print("Space")
        io[':KEY4,1,49']:set_value(1)
    elseif frame_num == 130 then
        -- Space
        io[':KEY4,1,49']:set_value(0)
    elseif frame_num > 400 then
        msx1_cass_base.post_command(frame_num, command)
    end

    msx1_cass_base.manage_frame(frame_num, is_run_required)
end

command, is_run_required = msx1_cass_base.get_command()
io = io_base.get()

emu.add_machine_frame_notifier
