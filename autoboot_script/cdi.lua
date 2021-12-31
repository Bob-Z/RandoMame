local button = {}
for i, j in  ipairs(manager.machine.ioport.ports) do
 for field_name, field in pairs(j.fields) do
  print("")
  print(field_name)
  --print("  tag", field.port.tag)
  --print("  mask", field.mask)
  --print("  type", field.type)
  id = field.port.tag .. ',' .. field.mask .. ',' .. field.type
  print("id:", id)
  button[id] = field
 end
end

local boot_end_frame = 410
local frame_num = 0
local function process_frame()
        frame_num = frame_num + 1

        if frame_num < boot_end_frame then
		    manager.machine.video.throttled = false
		    manager.machine.video.frameskip = 12
		else
		    if frame_num < boot_end_frame + 20 then
	  		    manager.machine.video.throttled = true
    		    manager.machine.video.frameskip = 0

		        button[":slave_hle:MOUSEBTN,1,64"]:set_value(1)
		    else
		        if frame_num < boot_end_frame + 40 then
		            button[":slave_hle:MOUSEBTN,1,64"]:set_value(0)
		        end
		    end
		end
end

emu.register_frame_done(process_frame)


