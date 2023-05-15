button = {}

-- P1 Right Stick/Down	: 	:IN.0,1,56
-- P1 Right Stick/Up	: 	:IN.0,2,55
-- P1 Left Stick/Up	: 	:IN.0,4,59
-- P1 Left Stick/Down	: 	:IN.0,8,60

for i, j in pairs(manager.machine.ioport.ports) do
 for field_name, field in pairs(j.fields) do
  id = field.port.tag .. ',' .. field.mask .. ',' .. field.type
  print(field_name,": ", id)
  button[id] = field
 end
end

frame_num = 0
previous_left = {0,0,0}
previous_right = {0,0,0}
-- name are up to down so index 1 is up and index 3 is down
name_left = {"0.4.2","0.4.1","1.6.0"}
name_right = {"1.9.3","1.7.1","1.11.1"}
button_name_left = {":IN.0,4,59",":IN.0,8,60"}
button_name_right = {":IN.0,2,55",":IN.0,1,56"}
available_left = {}
available_right = {}
available_qty_left = 0
available_qty_right = 0
current_left = 0
current_right = 0
mario_svg_left = {"1.3.2","0.3.0","0.3.3"}
mario_svg_right = {"1.10.3","0.10.2","0.11.2"}
mario_left=0
mario_right=0
push_button_left = false
push_button_time_left = 2
push_button_right = false
push_button_time_right = 2

function process_frame()
        frame_num = frame_num + 1

	-- check for new crate
	for i = 1, 3 do
		if previous_left[i] == 0 and manager.machine.output:get_value(name_left[i]) == 1 then
			--print("Left detected ",i)
			table.insert(available_left,1,i)
			available_qty_left = available_qty_left + 1
		end
		previous_left[i] = manager.machine.output:get_value(name_left[i])

		if previous_right[i] == 0 and manager.machine.output:get_value(name_right[i]) == 1 then
			--print("Right detected ",i)
			table.insert(available_right,1,i)
			available_qty_right = available_qty_right + 1
		end
		previous_left[i] = manager.machine.output:get_value(name_left[i])
		previous_right[i] = manager.machine.output:get_value(name_right[i])
	end

	-- check for current crate cleared
	if current_left ~= 0 then
		if manager.machine.output:get_value(name_left[current_left]) == 0 then
			--print("Left no more crate")
			current_left = 0
		end
	end
	if current_right ~= 0 then
		if manager.machine.output:get_value(name_right[current_right]) == 0 then
			--print("Right no more crate")
			current_right = 0
		end
	end

	-- Set new crate
	if current_left == 0 then
		if available_qty_left > 0 then
			-- get latest index and remove it
			current_left = available_left[available_qty_left]
			table.remove(available_left,available_qty_left)
			available_qty_left = available_qty_left - 1
			-- check if crate is still ther
			if manager.machine.output:get_value(name_left[current_left]) == 0 then
				print("Current crate is not here anymore ",current_left)
				current_left = 0
			end
		end
	end

	if current_right == 0 then
		if available_qty_right > 0 then
			-- get latest index and remove it
			current_right = available_right[available_qty_right]
			table.remove(available_right,available_qty_right)
			available_qty_right = available_qty_right - 1
			-- check if crate is still ther
			if manager.machine.output:get_value(name_right[current_right]) == 0 then
				print("Current crate is not here anymore ",current_right)
				current_right = 0
			end
		end
	end

	-- Push buttons
	-- where is Mario
	for i = 1, 3 do
		if manager.machine.output:get_value(mario_svg_left[i]) == 1 then
			mario_left = i
			break
		end
	end
	mario_target_left = current_left
	-- if no crate try to wait in the middle
	if current_left == 0 then
		mario_target_left = 2
	end

	if mario_target_left > mario_left then
			button[button_name_left[2]]:set_value(1)
	elseif mario_target_left < mario_left then
			button[button_name_left[1]]:set_value(1)
	else
		button[button_name_left[1]]:set_value(0)
		button[button_name_left[2]]:set_value(0)
		push_button_left = false
		push_button_time_left = 2
	end

	-- where is Mario
	for i = 1, 3 do
		if manager.machine.output:get_value(mario_svg_right[i]) == 1 then
			mario_right = i
			break
		end
	end
	mario_target_right = current_right
	-- if no crate try to wait in the middle
	if mario_target_right == 0 then
		mario_target_right = 2
	end

	if mario_target_right > mario_right then
			button[button_name_right[2]]:set_value(1)
	elseif mario_target_right < mario_right then
			button[button_name_right[1]]:set_value(1)
	else
		button[button_name_right[1]]:set_value(0)
		button[button_name_right[2]]:set_value(0)
		push_button_right = false
		push_button_time_right = 2
	end
end

subscription = emu.add_machine_frame_notifier(process_frame)
--emu.add_machine_reset_notifier(process_frame)


