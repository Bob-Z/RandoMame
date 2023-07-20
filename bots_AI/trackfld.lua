--[[
https://github.com/mamedev/mame/blob/master/src/mame/drivers/trackfld.cpp

in0
P1 Button 1
P1 Button 2
P1 Button 3

in2
1 Player Start

MAIN BOARD:
0000-17ff RAM
1800-183f Sprite RAM Pt 1
1C00-1C3f Sprite RAM Pt 2
3800-3bff Color RAM
3000-33ff Video RAM
6000-ffff ROM
1200-12ff IO
]]

local M = {}

local cpu = manager.machine.devices[":maincpu"]
local mem = cpu.spaces["program"]
local ioport = manager.machine.ioport
local in0 = ioport.ports[":IN0"]
local in1 = ioport.ports[":IN1"]
local in2 = ioport.ports[":SYSTEM"]

M.start1   = { in2 = in2, field = in2.fields["1 Player Start"] }
M.RunLeft  = { in0 = in0, field = in0.fields["P1 Button 1"] }
M.Action   = { in0 = in0, field = in0.fields["P1 Button 2"] }
M.RunRight = { in0 = in0, field = in0.fields["P1 Button 3"] }

-- These are all addresses in memory for important things
local START_PISTOL	 	= 0x1F65
local INITIALS_CHECK 	= 0x2800
local GAME_SUBSTATE  	= 0x2803
local CURRENT_LETTER 	= 0x281D
local EVENT_NUMBER   	= 0x2884
local HIGH_JUMP_FOULS   = 0x289F
local HIGH_JUMP_HEIGHT  = 0x28A1
local HORIZONTAL_SCROLL = 0x28A3
local HAMMER_COUNTER	= 0x28BD
local ELEVATION_ANGLE   = 0x28D8
local LETTER_COUNTER 	= 0x299E
local HAMMER_ANGLE		= 0x2A38
local HIGH_JUMPER_POSE  = 0x2AD2

-- This is the location where you should jump in the 100M
local JUMP_SCROLL_100M  = 0x3654

-- This is the location where you should throw in the javelin
local THROW_SCROLL_JAVELIN = 0x360F

-- This is where you should jump for the high jump
local JUMP_SCROLL_HIGH_JUMP = 0x362E

local STATE_STARTUP   = 0
local STATE_INITIALS  = 1
local STATE_100M_DASH = 2
local STATE_LONG_JUMP = 3
local STATE_JAVELIN   = 4
local STATE_HURDLES	  = 5
local STATE_HAMMER    = 6
local STATE_HIGH_JUMP = 7

local EVENT_100M	  = 0


local SUBSTATE_NONE	= 0

-- Enter your Initials substates
local SUBSTATE_INITIALS_1STLETTER = 1
local SUBSTATE_INITIALS_2NDLETTER = 2
local SUBSTATE_INITIALS_3RDLETTER = 3
local SUBSTATE_INITIALS_DONE      = 4

-- 100M dash substates
local SUBSTATE_100M_AWAIT_PISTOL  = 1
local SUBSTATE_100M_RUNNING       = 2

-- Long jump substates
local SUBSTATE_LONG_JUMP_WAIT	  = 0
local SUBSTATE_LONG_JUMP_RUN	  = 1
local SUBSTATE_LONG_JUMP_JUMP	  = 2
local SUBSTATE_LONG_JUMP_ANGLE	  = 3

-- Javelin toss substates
local SUBSTATE_JAVELIN_WAIT	  	  = 0
local SUBSTATE_JAVELIN_RUN	  	  = 1
local SUBSTATE_JAVELIN_THROW	  = 2
local SUBSTATE_JAVELIN_ANGLE	  = 3

-- Hurdles substates
local SUBSTATE_HURDLES_AWAIT_PISTOL  = 1
local SUBSTATE_HURDLES_RUNNING       = 2

-- Hammer throw substates
local SUBSTATE_HAMMER_THROW_WAIT  = 0
local SUBSTATE_HAMMER_THROW_SPIN  = 1
local SUBSTATE_HAMMER_THROW_THROW = 2
local SUBSTATE_HAMMER_THROW_ANGLE = 3

-- High jump substates
local SUBSTATE_HIGH_JUMP_WAIT	  = 0
local SUBSTATE_HIGH_JUMP_RUN	  = 1
local SUBSTATE_HIGH_JUMP_JUMP	  = 2
local SUBSTATE_HIGH_JUMP_ANGLE1	  = 3
local SUBSTATE_HIGH_JUMP_ANGLE2	  = 4
local SUBSTATE_HIGH_JUMP_ANGLE3	  = 5

-- Bit defines for player buttons
local RIGHT   = 1
local ACTION  = 2
local LEFT    = 4

-- Member variable declaration/initialization
M.currentState = STATE_STARTUP
M.subState = SUBSTATE_NONE
M.pressed = 0
M.buttonHoldTimer = 0
M.frameCounter = 0
M.temp = 0
M.iteration = 0
M.laps = 1



-- function to press the run buttons to obtain the desired speed
function M.run()

	value = math.fmod(M.frameCounter, 4)
	
	if value == 0 then
		M.RunLeft.field:set_value(1)
	elseif value == 1 then
		M.RunLeft.field:set_value(0)
		M.RunRight.field:set_value(0)
	elseif value == 2 then
		M.RunRight.field:set_value(1)
	elseif value == 3 then
		M.RunLeft.field:set_value(0)
		M.RunRight.field:set_value(0)	
	else
		print("Got unknown value " .. value)
	end
end

-- function called every frame
function M.updateMem()

	M.frameCounter = M.frameCounter + 1
	
	-- This whole thing has to be run via state machine
	if M.currentState == STATE_STARTUP then
		-- If we're here, we're just waiting for the signal that we're on the "Enter your initials" screen
		if mem:read_u8(INITIALS_CHECK) == 2 then
			-- Unpress the start button
			M.start1.field:set_value(0)
			-- Move us on to the next state
			M.currentState = STATE_INITIALS
			M.subState = SUBSTATE_INITIALS_1STLETTER
		end
	elseif M.currentState == STATE_INITIALS then
		if M.subState == SUBSTATE_INITIALS_1STLETTER then
			if mem:read_u8(CURRENT_LETTER) == 0x48 then
				-- Stop moving if we're on the right letter
				M.RunRight.field:set_value(0)
				M.pressed = M.pressed & ~RIGHT
				
				-- Press the ACTION button to select it.
				M.Action.field:set_value(1)
				M.pressed = M.pressed | ACTION
				-- Go to next substate
				M.subState = SUBSTATE_INITIALS_2NDLETTER
				return
			else
				if M.pressed & RIGHT ~= RIGHT then
					M.RunRight.field:set_value(1)
					M.pressed = M.pressed | RIGHT
				end
			end
		elseif M.subState == SUBSTATE_INITIALS_2NDLETTER then
			-- Wait for the counter to change
			if mem:read_u8(LETTER_COUNTER) ~= 1 then
				M.buttonHoldTimer = M.buttonHoldTimer + 1
				if M.buttonHoldTimer > 10 then
					M.buttonHoldTimer = 0
					if in0:read() == 253 then
						M.Action.field:set_value(0)
					else
						M.Action.field:set_value(1)
					end
				end
				return
			else
				M.Action.field:set_value(0)			
				M.pressed = M.pressed & ~ACTION
			end
			
			if mem:read_u8(CURRENT_LETTER) == 0x4E then
				-- Stop moving if we're on the right letter
				M.RunLeft.field:set_value(0)
				M.pressed = M.pressed & ~LEFT
				
				-- Press the ACTION button to select it.
				M.Action.field:set_value(1)
				M.pressed = M.pressed | ACTION
				
				-- Go to next substate
				M.subState = SUBSTATE_INITIALS_3RDLETTER
				return
			else
				if M.pressed & LEFT ~= LEFT then
					M.RunLeft.field:set_value(1)
					M.pressed = M.pressed | LEFT
				end
			end
		elseif M.subState == SUBSTATE_INITIALS_3RDLETTER then
			-- Wait for the counter to change
			if mem:read_u8(LETTER_COUNTER) ~= 2 then
				M.buttonHoldTimer = M.buttonHoldTimer + 1
				if M.buttonHoldTimer > 10 then
					M.buttonHoldTimer = 0
					if in0:read() == 253 then
						M.Action.field:set_value(0)
					else
						M.Action.field:set_value(1)
					end
				end
				return
			else
				M.Action.field:set_value(0)			
				M.pressed = M.pressed & ~ACTION
			end
			
			if mem:read_u8(CURRENT_LETTER) == 0x50 then
				-- Press the ACTION button to select it.
				-- Stop moving if we're on the right letter
				M.RunRight.field:set_value(0)
				M.pressed = M.pressed & ~RIGHT
				
				-- Press the ACTION button to select it.
				M.Action.field:set_value(1)
				M.pressed = M.pressed | ACTION
				
				-- Go to next state
				M.subState = SUBSTATE_INITIALS_DONE
				return
			else
				if M.pressed & RIGHT ~= RIGHT then
					M.RunRight.field:set_value(1)
					M.pressed = M.pressed | RIGHT
				end
			end
		elseif M.subState == SUBSTATE_INITIALS_DONE then
			-- Wait for the counter to change
			if mem:read_u8(LETTER_COUNTER) ~= 0 then
				M.buttonHoldTimer = M.buttonHoldTimer + 1
				if M.buttonHoldTimer > 10 then
					M.buttonHoldTimer = 0
					if in0:read() == 253 then
						M.Action.field:set_value(0)
					else
						M.Action.field:set_value(1)
					end
				end
				return
			else
				-- We're done here, release the action button
				M.Action.field:set_value(0)
				M.pressed = M.pressed & ~ACTION

				-- Go to next state
				M.currentState = STATE_100M_DASH
				M.subState	   = SUBSTATE_100M_AWAIT_PISTOL
--[[
				-- Use this to go STRAIGHT to an event for debugging
				mem:write_u8(EVENT_NUMBER, 4)
				M.currentState = STATE_HAMMER
				M.subState = SUBSTATE_HAMMER_THROW_WAIT
				return
]]				
			end
		end
	elseif M.currentState == STATE_100M_DASH then
		if M.subState == SUBSTATE_100M_AWAIT_PISTOL then
			if mem:read_u8(START_PISTOL) & 0x01 ~= 0x01 then
				return
			else
				-- We get here when the pistol has fired, so RUN!
				M.subState = SUBSTATE_100M_RUNNING
				return
			end
		elseif M.subState == SUBSTATE_100M_RUNNING then
			if mem:read_u8(EVENT_NUMBER) ~= EVENT_100M then
				M.currentState = STATE_LONG_JUMP
				M.subState = SUBSTATE_LONG_JUMP_WAIT
				M.iteration = 0
			else
				M.run()
			end
		end
	elseif M.currentState == STATE_LONG_JUMP then
		-- Wait for the starter's whistle thing
		if M.subState == SUBSTATE_LONG_JUMP_WAIT then
			if mem:read_u8(GAME_SUBSTATE) == 0x02 then
				M.temp = 0
				M.subState = SUBSTATE_LONG_JUMP_RUN
			end
		elseif M.subState == SUBSTATE_LONG_JUMP_RUN then
			if mem:read_u16(HORIZONTAL_SCROLL) == JUMP_SCROLL_100M then
				if M.temp == 2 then
					M.subState = SUBSTATE_LONG_JUMP_JUMP
				else
					M.run()
					M.temp = M.temp + 1
				end
			else
				M.run()
			end
		elseif M.subState == SUBSTATE_LONG_JUMP_JUMP then
			M.Action.field:set_value(1)
			M.subState = SUBSTATE_LONG_JUMP_ANGLE
		elseif M.subState == SUBSTATE_LONG_JUMP_ANGLE then
			-- It takes a frame for the game to read the angle, so we have to go 1 less.
			if mem:read_u8(ELEVATION_ANGLE) == 41 then
				M.Action.field:set_value(0)
			end
			
			if mem:read_u8(GAME_SUBSTATE) == 0x01 then
				M.subState = SUBSTATE_LONG_JUMP_WAIT
			elseif mem:read_u8(GAME_SUBSTATE) == 0x05 then
				-- Go to Javelin here
				M.currentState = STATE_JAVELIN
				M.subState = SUBSTATE_JAVELIN_WAIT
			end
		end
	elseif M.currentState == STATE_JAVELIN then
		-- Wait for the starter's whistle thing
		if M.subState == SUBSTATE_JAVELIN_WAIT then
			if mem:read_u8(GAME_SUBSTATE) == 0x02 then
				M.temp = 0
				M.subState = SUBSTATE_JAVELIN_RUN
			end
		elseif M.subState == SUBSTATE_JAVELIN_RUN then
			if mem:read_u16(HORIZONTAL_SCROLL) == THROW_SCROLL_JAVELIN then
				if M.temp == 3 then
					M.subState = SUBSTATE_JAVELIN_THROW
				else
					M.run()
					M.temp = M.temp + 1
				end
			else
				M.run()
			end
		elseif M.subState == SUBSTATE_JAVELIN_THROW then
			M.Action.field:set_value(1)
			M.subState = SUBSTATE_JAVELIN_ANGLE
		elseif M.subState == SUBSTATE_JAVELIN_ANGLE then
			-- It takes a frame for the game to read the angle, so we have to go 1 less.
			if mem:read_u8(ELEVATION_ANGLE) == 41 then
				M.Action.field:set_value(0)
			end
			
			if mem:read_u8(GAME_SUBSTATE) == 0x01 then
				M.subState = SUBSTATE_JAVELIN_WAIT
			elseif mem:read_u8(GAME_SUBSTATE) == 0x05 then
				-- Go to Hurdles here
				M.currentState = STATE_HURDLES
				M.subState = SUBSTATE_HURDLES_AWAIT_PISTOL
			else
				M.run()
			end
		end		
	elseif M.currentState == STATE_HURDLES then
		if M.subState == SUBSTATE_HURDLES_AWAIT_PISTOL then
			if mem:read_u8(START_PISTOL) & 0x01 ~= 0x01 then
				return
			else
				-- We get here when the pistol has fired, so RUN!
				M.subState = SUBSTATE_HURDLES_RUNNING
				-- Number of steps between hurdles
				M.temp = 0
				-- Number of hurdles cleared
				M.iteration = 0
				return
			end
		elseif M.subState == SUBSTATE_HURDLES_RUNNING then
			if M.iteration == 0 then
				M.steps = 70
			elseif M.iteration == 5 then
				M.steps = 8
			else
				M.steps = 9
			end
			
			if (M.temp > M.steps) and (M.iteration < 40) then
				M.Action.field:set_value(1)
				M.temp = 0
				M.iteration = M.iteration + 1
			else
				M.Action.field:set_value(0)
				M.temp = M.temp + 1
				M.run()
			end
			
			if mem:read_u8(GAME_SUBSTATE) == 0x05 then
				-- Go to Hammer Throw here
				M.currentState = STATE_HAMMER
				M.subState = SUBSTATE_HAMMER_THROW_WAIT
				M.iteration = 0
				return
			end
		end
	elseif M.currentState == STATE_HAMMER then
		if M.iteration < 3 then
			if M.subState == SUBSTATE_HAMMER_THROW_WAIT then
				if mem:read_u8(GAME_SUBSTATE) == 0x02 then
					M.subState = SUBSTATE_HAMMER_THROW_SPIN
				end
			elseif M.subState == SUBSTATE_HAMMER_THROW_SPIN then
				-- Wait for the hammer counter to hit the sweet spot
				if mem:read_u8(HAMMER_COUNTER) == 0x3A then
					M.subState = SUBSTATE_HAMMER_THROW_THROW
					return
				else
					-- This causes the spin to start instead of waiting on the timeout
					M.run()
				end
			elseif M.subState == SUBSTATE_HAMMER_THROW_THROW then
				-- THROW it! (Err, press the button)
				M.Action.field:set_value(1)
				M.subState = SUBSTATE_HAMMER_THROW_ANGLE
			elseif M.subState == SUBSTATE_HAMMER_THROW_ANGLE then
				-- Wait for the correct angle
				if mem:read_u8(HAMMER_ANGLE) == 41 then
					-- Then release the button.
					M.Action.field:set_value(0)
					-- And run like hell, it might help!
					M.run()
				end
				
				-- Wait for the end of this attempt
				if mem:read_u8(GAME_SUBSTATE) == 0x03 then
					M.iteration = M.iteration + 1
					M.subState = SUBSTATE_HAMMER_THROW_WAIT
					return
				end
			end
		else
			-- Wait for the current event to end
			if mem:read_u8(GAME_SUBSTATE) == 0x01 then
				M.currentState = STATE_HIGH_JUMP
				M.subState = SUBSTATE_HIGH_JUMP_WAIT
				return
			end
		end
	elseif M.currentState == STATE_HIGH_JUMP then
		if M.subState == SUBSTATE_HIGH_JUMP_WAIT then
			state = mem:read_u8(GAME_SUBSTATE)
			if state == 0x05 then
				M.currentState = STATE_100M_DASH
				M.subState	   = SUBSTATE_100M_AWAIT_PISTOL
				print("Lap " .. M.laps .. " Complete")
				M.laps = M.laps + 1
				return
			elseif state == 0x02 then
				M.subState 	   = SUBSTATE_HIGH_JUMP_RUN
				return
			end
		elseif M.subState == SUBSTATE_HIGH_JUMP_RUN then
			if mem:read_u16(HORIZONTAL_SCROLL) == JUMP_SCROLL_HIGH_JUMP then
				M.Action.field:set_value(1)
				M.subState = SUBSTATE_HIGH_JUMP_JUMP
			else
				M.run()
			end
		elseif M.subState == SUBSTATE_HIGH_JUMP_JUMP then
			M.Action.field:set_value(0)
			M.run()
			
			if mem:read_u8(HIGH_JUMP_HEIGHT) == 0x59 then
				M.subState = SUBSTATE_HIGH_JUMP_ANGLE1
				M.Action.field:set_value(1)
				M.run()
			end
		elseif M.subState == SUBSTATE_HIGH_JUMP_ANGLE1 then
			-- Set the first angle to 75 degrees
			if mem:read_u8(ELEVATION_ANGLE) == 75 then
				M.Action.field:set_value(0)
			end
			
			-- Watch for the pose to change
			if mem:read_u8(HIGH_JUMPER_POSE) == 0x03 then
				M.subState = SUBSTATE_HIGH_JUMP_ANGLE2
				M.Action.field:set_value(1)
			end
			M.run()
		elseif M.subState == SUBSTATE_HIGH_JUMP_ANGLE2 then
			if mem:read_u8(ELEVATION_ANGLE) == 30 then
				M.Action.field:set_value(0)
			end
			
			if mem:read_u8(GAME_SUBSTATE) == 0x03 then
				M.subState = SUBSTATE_HIGH_JUMP_WAIT
			end
			M.run()
		end
	end	
end

-- start game
function M.start()
    -- Press 1-player start button
    M.start1.field:set_value(1)
	
    -- register update loop callback function
    emu.register_frame_done(M.updateMem, "frame")		
end

M.start()

return M
