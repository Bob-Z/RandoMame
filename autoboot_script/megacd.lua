local button = {}
local ports = manager.machine.ioport.ports[":PAD1_3B"]
for field_name, field in pairs(ports.fields) do
    button[field_name] = field
end
button["P1 Start"]:set_value(1)
button["P1 Start"]:set_value(0)
