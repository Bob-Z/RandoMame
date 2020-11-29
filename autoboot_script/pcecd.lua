local button = {}
local ports = manager:machine():ioport().ports[":JOY_P.0"]
for field_name, field in pairs(ports.fields) do
    button[field_name] = field
end
local value_to_be_set = 1
button["P1 Run"]:set_value(value_to_be_set)
