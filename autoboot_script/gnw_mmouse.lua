button = {}

-- ACL	: 	:ACL,1,30
-- Infinite Lives (Cheat)	: 	:BA,1,6
-- P1 Left Stick/Down	: 	:IN.1,4,60
-- P1 Right Stick/Down	: 	:IN.1,1,56
-- P1 Right Stick/Up	: 	:IN.1,2,55
-- P1 Left Stick/Up	: 	:IN.1,8,59
-- Alarm	: 	:IN.2,8,31
-- Time	: 	:IN.2,1,47
-- Game A	: 	:IN.2,4,7
-- Game B	: 	:IN.2,2,8

for i, j in pairs(manager.machine.ioport.ports) do
 for field_name, field in pairs(j.fields) do
  id = field.port.tag .. ',' .. field.mask .. ',' .. field.type
  print(field_name,": ", id)
  button[id] = field
 end
end

frame_num = 0
previous = {0,0,0,0}
name = {"3.2.1","2.0.0","8.2.1","0.3.1"}
button_name = {":IN.1,8,59",":IN.1,4,60",":IN.1,2,55",":IN.1,1,56"}
available = {}
available_qty = 0
current = 0

function process_frame()
        frame_num = frame_num + 1

	if frame_num == 30 then
		button[":IN.2,2,8"]:set_value(1)
	end
	if frame_num == 40 then
		button[":IN.2,2,8"]:set_value(0)
	end

	for i = 1, 4 do
		if previous[i] == 0 and manager.machine.output:get_value(name[i]) == 1 then
			print("Egg detected ",i)
			table.insert(available,1,i)
			available_qty = available_qty + 1
		end
		previous[i] = manager.machine.output:get_value(name[i])
	end

	if current ~= 0 then
		if manager.machine.output:get_value(name[current]) == 0 then
			print("Release button ", button_name[current])
			button[button_name[current]]:set_value(0)
			current = 0
		end
	end

	if current == 0 then
		if available_qty > 0 then
			-- get latest index and remove it
			current = available[available_qty]
			table.remove(available,available_qty)
			available_qty = available_qty - 1
			button[button_name[current]]:set_value(1)
			print("Press button ", button_name[current])
		end
	end
end

subscription = emu.add_machine_frame_notifier(process_frame)
--emu.add_machine_reset_notifier(process_frame)


