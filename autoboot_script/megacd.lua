local button = {}
local ports = manager:machine():ioport().ports[":PAD1_3B"]
for field_name, field in pairs(ports.fields) do
    button[field_name] = field
end
local value_to_be_set = 1
button["P1 Start"]:set_value(value_to_be_set)
