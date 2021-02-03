cpu = manager.machine.devices[":maincpu"]
mem = cpu.spaces["program"]
base_addr = 0x9E7D
base_file_name_size = 8
ext_file_name_size = 3
next_file = 14
file_index = 0
cat_frame = 0
try_run = 0
type_buffer = {}
type_qty = 0
memory_clean_frame = 0

local function stack_char(char)
    table.insert(type_buffer, 1, char)
    type_qty = type_qty + 1
end

local function cat(frame)
    stack_char("c")
    stack_char("a")
    stack_char("t")
    stack_char("\n")
    cat_frame = frame
end

local function run_file()
    stack_char("r")
    stack_char("u")
    stack_char("n")
    stack_char("\"")
    for c = 0, base_file_name_size-1 do
        addr = base_addr + file_index * next_file + c
        char = mem:read_u8(addr)
        if char ~= 0x20 then
            char = char & 0x7F
            stack_char(string.char(char))
        end
    end

    stack_char("\n")
end

local function read_file_name()
    start_file = mem:read_u8(base_addr + file_index * next_file)
    if start_file ~= 0 then
        run_file()
        try_run = 1
    end
end

local function wait_for_clean_memory(frame)
    if memory_clean_frame ~= 0 then
        if frame > memory_clean_frame + 25 then
            try_run = 0
            cat_frame = 0
            memory_clean_frame = 0
            file_index = file_index + 1
        end
    else
        start_file = mem:read_u8(base_addr + file_index * next_file)
        if start_file == 0 then
            memory_clean_frame = frame
        end
    end
end

local function unstack_char()
    if type_qty > 0 then
        char = table.remove(type_buffer)
        type_qty = type_qty - 1
        emu.keypost(char)
    end
end

frame_num = 0
local function process_frame()
    frame_num = frame_num + 1

    if cat_frame == 0 then
        if frame_num > 250 then
            cat(frame_num)
        end
    else
        if try_run == 0 then
            if frame_num > cat_frame + 250 then
                read_file_name()
            end
        else
            wait_for_clean_memory(frame_num)
        end
    end

    if frame_num % 5 == 0 then
        unstack_char()
    end
end

emu.keypost("|disc\n")
emu.keypost("run\"disc\n")
emu.register_frame_done(process_frame)
