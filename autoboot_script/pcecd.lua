local button = {}
local ports = manager:machine():ioport().ports[":JOY_P.0"]
for field_name, field in pairs(ports.fields) do
    button[field_name] = field
end
button["P1 Run"]:set_value(1)
button["P1 Run"]:set_value(0)
