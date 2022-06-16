local button = {}
for i, j in  ipairs(manager.machine.ioport.ports) do
 for field_name, field in pairs(j.fields) do
  print("")
  print(field_name)
  button[field_name] = field
 end
end

local frame_num = 0
local down_frame = 20
local up_frame = 0
local count = 0

local function process_frame()
        frame_num = frame_num + 1

        if frame_num == down_frame then
            if button["Time"] ~= nil and count < 3 then
                button["Time"]:set_value(1)
            end

            if button["Power On/Start"] ~= nil then
                button["Power On/Start"]:set_value(1)
            end

            down_frame = 0
            up_frame = frame_num + 20
    	end

        if frame_num == up_frame then
            if button["Time"] ~= nil and count < 3 then
                button["Time"]:set_value(0)
                count = count + 1
            end

            if button["Power On/Start"] ~= nil then
                button["Power On/Start"]:set_value(0)
            end

            up_frame = 0
            down_frame = frame_num + 20
    	end
end

emu.register_frame_done(process_frame)


