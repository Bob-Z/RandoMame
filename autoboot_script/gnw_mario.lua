button = {}

-- P1 Right Stick/Down	: 	:IN.0,1,56
-- P1 Right Stick/Up	: 	:IN.0,2,55
-- P1 Left Stick/Up	: 	:IN.0,4,59
-- P1 Left Stick/Down	: 	:IN.0,8,60
-- Game B	: 	:IN.1,2,8
-- Game A	: 	:IN.1,4,7

for i, j in pairs(manager.machine.ioport.ports) do
 for field_name, field in pairs(j.fields) do
  id = field.port.tag .. ',' .. field.mask .. ',' .. field.type
  print(field_name,": ", id)
  button[id] = field
 end
end

frame_num = 0
previous_crate_value = {{0,0,0},{0,0,0}}
-- SVG names are up to down so index 1 is up and index 3 is down
crate_svg_name = {{"0.4.2","0.4.1","1.6.0"},{"1.9.3","1.7.1","1.11.1"}}
button_name = {{":IN.0,4,59",":IN.0,8,60"},{":IN.0,2,55",":IN.0,1,56"}}
ready_crate_index_list = {{},{}}
target_crate_index = {0,0}
mario_svg = {{"1.3.2","0.3.0","0.3.3"},{"1.10.3","0.10.2","0.11.2"}}

function process_frame()
        frame_num = frame_num + 1

	-- auto start Game B
	if frame_num == 60 then
		button[":IN.1,4,7"]:set_value(1)
	end
	if frame_num == 65 then
		button[":IN.1,4,7"]:set_value(0)
	end

	for screen = 1, 2 do
		-- check for new crate
		for i = 1, 3 do
			if previous_crate_value[screen][i] == 0 and manager.machine.output:get_value(crate_svg_name[screen][i]) == 1 then
				table.insert(ready_crate_index_list[screen],1,i)
			end
			previous_crate_value[screen][i] = manager.machine.output:get_value(crate_svg_name[screen][i])
		end

		-- check for target crate cleared
		if target_crate_index[screen] ~= 0 then
			if manager.machine.output:get_value(crate_svg_name[screen][target_crate_index[screen]]) == 0 then
				--print("no more crate")
				target_crate_index[screen] = 0
			end
		end

		-- set target crate
		if target_crate_index[screen] == 0 then
			if #ready_crate_index_list[screen] > 0 then
				-- get latest index and remove it
				target_crate_index[screen] = ready_crate_index_list[screen][#ready_crate_index_list[screen]]
				table.remove(ready_crate_index_list[screen],#ready_crate_index_list[screen])
				-- check if crate is still there (may happen when truck leaves: crates about to fall are cleared)
				if manager.machine.output:get_value(crate_svg_name[screen][target_crate_index[screen]]) == 0 then
					--print("Current crate is not here anymore ",target_crate_index[screen])
					target_crate_index[screen] = 0
				end
			end
		end

		-- Push buttons
		-- where is Mario
		for i = 1, 3 do
			if manager.machine.output:get_value(mario_svg[screen][i]) == 1 then
				mario_pos = i
				break
			end
		end
		mario_target = target_crate_index[screen]
		-- if no crate try to wait in the middle
		if target_crate_index[screen] == 0 then
			mario_target = 2
		end
	
		if mario_target > mario_pos then
				button[button_name[screen][2]]:set_value(1)
		elseif mario_target < mario_pos then
				button[button_name[screen][1]]:set_value(1)
		else
			button[button_name[screen][1]]:set_value(0)
			button[button_name[screen][2]]:set_value(0)
		end
	end
end

subscription = emu.add_machine_frame_notifier(process_frame)


