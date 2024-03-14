local button = {}

for i, j in pairs(manager.machine.ioport.ports) do
 for field_name, field in pairs(j.fields) do
  id = field.port.tag .. ',' .. field.mask .. ',' .. field.type
  print(field_name,"->", id)
  button[id] = field
 end
end

local command = {}
for i,j  in pairs(manager.machine.images) do
	print(i,"->",j.software_longname)
	if j.software_longname ~= nil then
    	for token in string.gmatch(j.software_longname, "[^%s]+") do
	    	table.insert(command, token)
		    print(token)
	    end
	end
end

local frame_num = 0
local frame_write = 180
local function process_frame()
	frame_num = frame_num + 1

	if frame_num == 60 then
	    button[":BRK,1,49"]:set_value(1)
	elseif frame_num == 70 then
	    button[":BRK,1,49"]:set_value(0)
	end

	if frame_num == frame_write then
		c = table.remove(command, 1)
		if c ~= nil then
			print("command",c)
			emu.keypost('*')
			emu.keypost(c)
			emu.keypost('\n')
			frame_write = frame_write + 120
		end
	end
end

subscription=emu.add_machine_frame_notifier(process_frame)
