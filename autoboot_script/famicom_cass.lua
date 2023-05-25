print("This script does nothing")

local button = {}

print("=== Ports ===")
for i, j in pairs(manager.machine.ioport.ports) do
 for field_name, field in pairs(j.fields) do
  id = field.port.tag .. ',' .. field.mask .. ',' .. field.type
  print(field_name,": ", id)
  button[id] = field
 end
end

print("")
print("=== Cassettes ===")
for i, j in pairs(manager.machine.cassettes) do
 print(i)
end

print("")
print("=== Images ===")
for i, j in pairs(manager.machine.images) do
 print(i)
end

local frame_num = 0

local function process_frame()
        frame_num = frame_num + 1

		if manager.machine.cassettes[":exp:fc_keyboard:tape"].is_stopped == false and manager.machine.cassettes[":exp:fc_keyboard:tape"].motor_state == true then
		    manager.machine.video.throttled = false
		    manager.machine.video.frameskip = 12
		else
		    manager.machine.video.throttled = true
		    manager.machine.video.frameskip = 0
		end
end

subscription=emu.add_machine_frame_notifier(process_frame)


