local M = {}

local cpu = manager.machine.devices[":maincpu"]
local mem = cpu.spaces["program"]
local ioport = manager.machine.ioport
local in0 = ioport.ports[":P1_P2"]
local in1 = ioport.ports[":SYSTEM"]

M.RunLeft  = { in0 = in0, field = in0.fields["P1 Button 1"] }
M.Action   = { in0 = in0, field = in0.fields["P1 Button 2"] }
M.RunRight = { in0 = in0, field = in0.fields["P1 Button 3"] }
M.start1   = { in1 = in1, field = in1.fields["1 Player Start"] }

local ARCHERY_SPRITE    = 0x1000
local HORSE_SPRITE_POS  = 0x101C
local SPIN_COUNTER		= 0x3048
local ARCHERY_WIND		= 0x305D
local EVENT_NUMBER   	= 0x3068
local ITERATION_NUMBER  = 0x306A
local ARROWS_LEFT		= 0x30A8
local CURRENT_POWER	    = 0x30B0
local ARCHERY_ANGLE   	= 0x30C1	-- 16-bit!
local ELEVATION_ANGLE   = 0x30C4
local STROKE_COUNTER	= 0x3157
local SWIMMING_PISTOL   = 0x31C0 	-- 0->1
local LETTER_COUNTER 	= 0x3402
local CURRENT_LETTER 	= 0x3420
local LIFT_READY		= 0x3628
local CHOOSE_WEIGHT		= 0x36D0
local SCREEN_SCROLL	    = 0x36DE
local JUDGE_LIGHTS		= 0x3771


-- Main States
local STATE_STARTUP   	= 0
local STATE_INITIALS  	= 1
local STATE_SWIMMING  	= 2
local STATE_SKEET_SKEET = 3
local STATE_LONG_HORSE  = 4
local STATE_ARCHERY     = 5
local STATE_TRIPLE_JUMP = 6
local STATE_WEIGHT_LIFT = 7
local STATE_POLE_VAULT  = 8

-- Universal "Nothing going on" state
local SUBSTATE_NONE				  = 0

-- Enter your Initials substates
local SUBSTATE_INITIALS_1STLETTER = 1
local SUBSTATE_INITIALS_2NDLETTER = 2
local SUBSTATE_INITIALS_3RDLETTER = 3
local SUBSTATE_INITIALS_DONE      = 4

-- Swimming substates
local SUBSTATE_SWIMMING_WAITING   = 1
local SUBSTATE_SWIMMING_SWIMMING  = 2
local SUBSTATE_SWIMMING_BREATHE	  = 3
local SUBSTATE_SWIMMING_DONE	  = 4

-- Skeeting substates
local SUBSTATE_SKEET_WAITING	  = 1

-- Horse Jump substates
local SUBSTATE_HORSE_WAITING	  = 1
local SUBSTATE_HORSE_RUNNING	  = 2
local SUBSTATE_HORSE_JUMPING	  = 3
local SUBSTATE_HORSE_VAULTING	  = 4
local SUBSTATE_HORSE_LANDING	  = 5

-- Archery substates
local SUBSTATE_ARCHERY_WAITING	  = 1
local SUBSTATE_ARCHERY_WIND		  = 2
local SUBSTATE_ARCHERY_TARGET	  = 3
local SUBSTATE_ARCHERY_ANGLE	  = 4

-- Triple jump substates
local SUBSTATE_TRIPLE_WAITING	  = 1
local SUBSTATE_TRIPLE_JUMP1		  = 2
local SUBSTATE_TRIPLE_JUMP2		  = 3
local SUBSTATE_TRIPLE_JUMP3		  = 4
local SUBSTATE_TRIPLE_JUMP4		  = 5
local SUBSTATE_TRIPLE_JUMP5		  = 6

-- Weight lifting substates
local SUBSTATE_WEIGHT_WAITING	  = 1
local SUBSTATE_WEIGHT_FLASH	      = 2
local SUBSTATE_WEIGHT_LIFT		  = 3

-- Pole vaulting substates
local SUBSTATE_VAULT_WAITING	  = 1
local SUBSTATE_VAULT_UP			  = 2
local SUBSTATE_VAULT_OVER		  = 3


-- Bit defines for player buttons
local RIGHT   = 1
local ACTION  = 2
local LEFT    = 4

-- Temp variable initializations
M.frameCounter = 0
M.pressed = 0
M.buttonHoldTimer = 0
M.currentState  = STATE_STARTUP
M.subState = SUBSTATE_NONE
M.horseTarget = 0
M.targetLine = 0

M.BoxL  ={x=0, y=0}
M.BoxR  ={x=0, y=0}
M.Skeet ={x=0, y=0}

M.delay = 0
M.iteration = 0
M.temp = 0

-- Reset all the buttons and states
function M.reset()
	M.Action.field:set_value(0)
	M.RunLeft.field:set_value(0)
	M.RunRight.field:set_value(0)
	M.pressed = 0
end

-- Press the run buttons, alternate half way through the amount specified.
function M.run(amount)
	value = math.fmod(M.frameCounter, amount)
	
	if value == 0 then
		M.RunLeft.field:set_value(1)
		M.RunRight.field:set_value(0)
	elseif value == math.ceil(amount / 2) then
		M.RunLeft.field:set_value(0)
		M.RunRight.field:set_value(1)
	end
end

-- Since Lua is missing one (without external libs)
function M.endianSwap(value)
	hi = (value & 0x00FF) << 8
	lo = (value & 0xFF00) >> 8
	return lo + hi		
end

-- function called every frame
function M.updateMem()
	M.frameCounter = M.frameCounter + 1
	
	if M.currentState == STATE_STARTUP then
		-- If we're here, we're just waiting for the signal that we're on the "Enter your initials" screen
		if mem:read_u8(CURRENT_LETTER) == 0x11 then
			-- Unpress the start button
			M.start1.field:set_value(0)
			-- Move us on to the next state
			M.currentState = STATE_INITIALS
			M.subState = SUBSTATE_INITIALS_1STLETTER
		end
	elseif M.currentState == STATE_INITIALS then
		if M.subState == SUBSTATE_INITIALS_1STLETTER then
			-- 'F' is 0x16
			if mem:read_u8(CURRENT_LETTER) == 0x16 then
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
			if mem:read_u8(LETTER_COUNTER) ~= 0x51 then
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

			-- 'A' is 0x11
			if mem:read_u8(CURRENT_LETTER) == 0x11 then
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
			if mem:read_u8(LETTER_COUNTER) ~= 0x52 then
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

			-- 'B' is 0x12
			if mem:read_u8(CURRENT_LETTER) == 0x12 then
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
				M.currentState = STATE_SWIMMING
				M.subState	   = SUBSTATE_SWIMMING_WAITING
			end
		end
	elseif M.currentState == STATE_SWIMMING then
		-- Make sure we're still in this event
		event = math.fmod(mem:read_u8(EVENT_NUMBER), 7)
		if  event ~= 0 then
			M.reset()
			M.currentState = STATE_SKEET_SKEET
			M.subState = SUBSTATE_SKEET_WAITING
			return
		end
		-- Waiting for the starter's pistol
		if M.subState == SUBSTATE_SWIMMING_WAITING then
			if mem:read_u8(SWIMMING_PISTOL) ~= 0x01 then
				return
			else
				M.subState = SUBSTATE_SWIMMING_SWIMMING
				return
			end
		elseif M.subState == SUBSTATE_SWIMMING_SWIMMING then
			if mem:read_u8(STROKE_COUNTER) ~= 4 then
				M.run(4)
			else
				M.Action.field:set_value(1)
				M.subState = SUBSTATE_SWIMMING_BREATHE
				return
			end
		elseif M.subState == SUBSTATE_SWIMMING_BREATHE then
			M.Action.field:set_value(0)
			M.subState = SUBSTATE_SWIMMING_SWIMMING
		end
	elseif M.currentState == STATE_SKEET_SKEET then
		-- Check for event number change
		event = math.fmod(mem:read_u8(EVENT_NUMBER), 7)
		if  event ~= 1 then
			M.reset()
			M.currentState = STATE_LONG_HORSE
			M.subState = SUBSTATE_HORSE_WAITING
			M.iteration = 0
		end
	
		-- Wait for spite memory to be initialized, AND populated
		if (mem:read_u8(0x101F) == 0) or (mem:read_u8(0x101F) == 0xF8) then
			return
		end
		
		-- This game is fast enough that we only need to hold the button down for 1 frame!
		if M.pressed & RIGHT ~= 0 then
			M.RunRight.field:set_value(0)
			M.pressed = M.pressed & ~RIGHT
		elseif M.pressed & LEFT ~= 0 then
			M.RunLeft.field:set_value(0)
			M.pressed = M.pressed & ~LEFT
		end

		-- 8 in just a guess.  I'm doubting that there are more than 8 clays on the screen at once.
		for x = 0, 8
		do
			-- grab the X of the skeet sprite
			M.Skeet.x = mem:read_u8(0x1053 + (x * 8))
			-- grab the TYPE of the sprite, we don't want to shoot at the shadows!
			_type = mem:read_u8(0x1052 + (x * 8))
			
			-- check the values for sanity (so that we don't process empty sprite cells)
			if (M.Skeet.x ~= 0) and (M.Skeet.x ~= 0xF8) and (_type ~= 0x4D) then
				-- As the sight grows, we need to adjust the "fireable width".
				Ldiff = 12 - (mem:read_u8(0x100F) - mem:read_u8(0x1017))
				Rdiff = 12 - (mem:read_u8(0x101F) - mem:read_u8(0x1027))
			
				-- If the target is between the edges of the sight
				if (M.Skeet.x >= mem:read_u8(0x100F)) and (M.Skeet.x <= (mem:read_u8(0x100F) + Ldiff)) then
					-- Then shoot it!
					M.RunLeft.field:set_value(1)
					M.pressed = M.pressed | LEFT
				elseif (M.Skeet.x >= mem:read_u8(0x101F)) and (M.Skeet.x <= (mem:read_u8(0x101F) + Rdiff)) then
					-- Then shoot it!
 					M.RunRight.field:set_value(1)
					M.pressed = M.pressed | RIGHT
				end
			end
		end
	elseif M.currentState == STATE_LONG_HORSE then
		-- Check for event number change
		event = math.fmod(mem:read_u8(EVENT_NUMBER), 7)
		if  event ~= 2 then
			M.reset()
			M.currentState = STATE_ARCHERY
			M.subState = SUBSTATE_ARCHERY_WAITING
		else
			if mem:read_u8(EVENT_NUMBER) == 9 then
				M.temp = 1
			else
				M.temp = 0
			end
		end
	
		if M.subState == SUBSTATE_HORSE_WAITING then		
			M.run(4)
			if mem:read_u16(SCREEN_SCROLL) ~= 0 then
				M.subState = SUBSTATE_HORSE_RUNNING
			end
		elseif M.subState == SUBSTATE_HORSE_RUNNING then
		
			-- We need to byte swap
			value = M.endianSwap(mem:read_u16(SCREEN_SCROLL))
		
			if (value >= 0x022F) then
				M.delay = 0
				M.Action.field:set_value(1)
				M.pressed = ACTION
				M.subState = SUBSTATE_HORSE_JUMPING
				M.horseTarget = 0
			end
		elseif M.subState == SUBSTATE_HORSE_JUMPING then
			if M.pressed & ACTION then
				M.Action.field:set_value(0)
				M.pressed = M.pressed & ~ACTION
			end
			value = M.endianSwap(mem:read_u16(SCREEN_SCROLL))
			
			if (M.horseTarget == 0) then
				M.horseTarget = value + 0x31
			end
			
			if (value >= M.horseTarget) then
				if M.delay >= 35 then
					M.Action.field:set_value(1)
					M.pressed = ACTION
					M.subState = SUBSTATE_HORSE_VAULTING
					M.delay = 0
				else
					M.delay = M.delay + 1
				end
			else
				M.run(4)
			end
		elseif M.subState == SUBSTATE_HORSE_VAULTING then
			if M.pressed & ACTION then
				M.Action.field:set_value(0)
				M.pressed = M.pressed & ~ACTION
			end
			
			-- 10 frames (when you're upright) after the 14th spin is registered, stick the landing
			if M.endianSwap(mem:read_u16(SPIN_COUNTER)) >= 0x0104 then
				if M.delay == 10 then
					M.reset()
					M.Action.field:set_value(1)
					M.pressed = ACTION
					M.subState = SUBSTATE_HORSE_LANDING
				else
					M.delay = M.delay + 1
					M.run(4)
				end
			else
				M.run(4)
			end
		elseif M.subState == SUBSTATE_HORSE_LANDING then		
			if M.pressed & ACTION then
				M.Action.field:set_value(0)
				M.pressed = M.pressed & ~ACTION
			end
			if mem:read_u8(ITERATION_NUMBER) ~= M.iteration then
				M.iteration = M.iteration + 1
				M.subState = SUBSTATE_HORSE_WAITING
			end
		end
	elseif M.currentState == STATE_ARCHERY then
		-- Check for event number change
		event = math.fmod(mem:read_u8(EVENT_NUMBER), 7)
		if  event ~= 3 then
			M.reset()
			M.currentState = STATE_TRIPLE_JUMP
			M.subState = SUBSTATE_TRIPLE_WAITING
		end
		
		if M.subState == SUBSTATE_ARCHERY_WAITING then
			M.reset()
			if mem:read_u8(ARCHERY_WIND) == 3 then
				M.subState = SUBSTATE_ARCHERY_WIND
			end
		elseif M.subState == SUBSTATE_ARCHERY_WIND then
			-- I could choose anything, so why not be studly, and do 0?
			if mem:read_u8(ARCHERY_WIND) == 0 then
				M.Action.field:set_value(1)
				M.RunLeft.field:set_value(1)
				M.pressed = ACTION
				M.subState = SUBSTATE_ARCHERY_TARGET
			end
		elseif M.subState == SUBSTATE_ARCHERY_TARGET then
			if M.pressed & ACTION == ACTION then
				M.Action.field:set_value(0)
				M.RunLeft.field:set_value(0)
				M.pressed = M.pressed & ~ACTION
			end
			
			if (mem:read_u32(ARCHERY_SPRITE) == 0x408299F0) or (mem:read_u32(ARCHERY_SPRITE) == 0x608C5EED) then
				M.Action.field:set_value(1)
				M.pressed = ACTION
				M.subState = SUBSTATE_ARCHERY_ANGLE
			end
		elseif M.subState == SUBSTATE_ARCHERY_ANGLE then
			if mem:read_u16(ARCHERY_ANGLE) == 0x0500 then
				M.Action.field:set_value(0)
				M.pressed = M.pressed & ~ACTION
				M.subState = SUBSTATE_ARCHERY_TARGET
			end
		end
	elseif M.currentState == STATE_TRIPLE_JUMP then
		-- Check for event number change
		event = math.fmod(mem:read_u8(EVENT_NUMBER), 7)
		if  event ~= 4 then
			M.reset()
			M.currentState = STATE_WEIGHT_LIFT
			M.subState = SUBSTATE_WEIGHT_WAITING
			M.temp = 0
		end

		if M.subState == SUBSTATE_TRIPLE_WAITING then
			-- The screen scroll is at A3 or A4 when you've reached the line.  (Location depends on the speed you're running!
			-- Running super fast, the scroll register skips A3, so you have to jump at A2, or risk fouling.
			if mem:read_u8(SCREEN_SCROLL) == 0xA2 or mem:read_u8(SCREEN_SCROLL) == 0xA3 then			
				-- OK, at the line, press the UP button
				M.Action.field:set_value(1)
				M.pressed = ACTION
				M.subState = SUBSTATE_TRIPLE_JUMP1
			else
				M.run(4)
			end
		elseif M.subState == SUBSTATE_TRIPLE_JUMP1 then
			-- Hold the UP button until elevation hits 35
			if mem:read_u8(ELEVATION_ANGLE) == 35 then
				M.reset()
				M.subState = SUBSTATE_TRIPLE_JUMP2
			else
				M.run(4)
			end
		elseif M.subState == SUBSTATE_TRIPLE_JUMP2 then
			if mem:read_u8(SCREEN_SCROLL) == 0xB1 then
				M.RunRight.field:set_value(0)
				M.RunLeft.field:set_value(0)
				M.Action.field:set_value(1)
				M.pressed = ACTION
				M.subState = SUBSTATE_TRIPLE_JUMP3
			else
				M.run(4)
			end
		elseif M.subState == SUBSTATE_TRIPLE_JUMP3 then
			if mem:read_u8(ELEVATION_ANGLE) == 41 then
				M.reset()
				M.subState = SUBSTATE_TRIPLE_JUMP4
			else
				M.run(4)
			end
		elseif M.subState == SUBSTATE_TRIPLE_JUMP4 then
			if mem:read_u8(SCREEN_SCROLL) == 0xC5 then
				M.Action.field:set_value(1)
				M.pressed = ACTION
				M.subState = SUBSTATE_TRIPLE_JUMP5
			else
				M.run(4)
			end
		elseif M.subState == SUBSTATE_TRIPLE_JUMP5 then
			if mem:read_u8(ELEVATION_ANGLE) == 45 then
				if M.pressed & ACTION == ACTION then
					M.reset()
				end
			else
				M.run(4)
			end
			
			if mem:read_u8(SCREEN_SCROLL) == 0x00 then
				M.temp = 1
				M.subState = SUBSTATE_TRIPLE_WAITING
			else
				M.run(4)
			end
		end		
	elseif M.currentState == STATE_WEIGHT_LIFT then
		-- Check for event number change
		event = math.fmod(mem:read_u8(EVENT_NUMBER), 7)
		if  event ~= 5 then
			M.currentState = STATE_POLE_VAULT
			M.subState = SUBSTATE_VAULT_WAITING
			
			if M.pressed & ACTION == ACTION then
				M.Action.field:set_value(0)
				M.pressed = M.pressed & ~ACTION
			end			
		end

		if M.subState == SUBSTATE_WEIGHT_WAITING then
			-- We are waiting for the screen to change
			if M.temp == 0 then
				M.reset()
				M.buttonHoldTimer = 0
				-- FF means we're on the "choose your weight" screen
				-- This monitors the "Scroll RAM" that is used to tell how much of the screen has scrolled.
				if mem:read_u16(CHOOSE_WEIGHT) == 0x00FF then
					-- Look for the "CHOOSE WEIGHT" line to turn RED (00 is white, 01 is Cyan, 02 is Blue, 03 is Red)
					if mem:read_u8(0x2AA0) == 0x03 then
						-- It seems that the number of items on the list decreases on later rounds
						-- And we always want to do the HEAVIEST, so we have to figure out what that is.
						-- These values represent the weight classes on the screen, in the color RAM.
						M.targetLine = 0x2B60
						for x = 0x2B60,0x2D60,0x40
						do							
							-- If the line is WHITE, then it's populated
							if mem:read_u8(x) == 0x00 or mem:read_u8(x) == 0x03 then
								-- Save it as possibly the last line
								M.targetLine = x
							else
								-- Else, we've found the end, and it was the last line.
								break
							end
						end
						M.temp = 1
					end
				end
			-- We are now on the Choose Weight screen, we need to scroll to the bottom.
			elseif M.temp == 1 then			
				-- 03 means the target line is red, and ready to be selected.
				if mem:read_u8(M.targetLine) == 0x03 then
					M.Action.field:set_value(1)
					M.pressed = M.pressed | ACTION
					M.temp = 2
					M.buttonHoldTimer = 0
				else
					if M.pressed & LEFT == LEFT then
						if M.buttonHoldTimer == 10 then
							M.RunLeft.field:set_value(0)
							M.pressed = M.pressed & ~LEFT
							M.buttonHoldTimer = 0
						else
							M.buttonHoldTimer = M.buttonHoldTimer + 1
						end
					else
						if M.buttonHoldTimer == 10 then
							M.RunLeft.field:set_value(1)
							M.pressed = M.pressed | LEFT
							M.buttonHoldTimer = 0
						else
							M.buttonHoldTimer = M.buttonHoldTimer + 1
						end
					end
				end
			-- We're now ready to lift
			elseif M.temp == 2 then
				-- 00 means we're back to the lift screen
				if mem:read_u16(CHOOSE_WEIGHT) == 0x0000 then
					if M.pressed & ACTION == ACTION then
						M.Action.field:set_value(0)
						M.pressed = M.pressed & ~ACTION
					end
					M.subState = SUBSTATE_WEIGHT_FLASH
					M.temp = 0
				end
			end
				
		elseif M.subState == SUBSTATE_WEIGHT_FLASH then
			if mem:read_u8(LIFT_READY) ~= 0x60 then
				M.RunLeft.field:set_value(0)
				M.RunRight.field:set_value(0)
				M.Action.field:set_value(1)
				M.pressed = ACTION
				M.subState = SUBSTATE_WEIGHT_PRESS
				M.delay = 0
				M.temp = 0
				M.buttonHoldTimer = 0
			else
				-- This is the LIFTING state
				M.run(4)
			end
		elseif M.subState == SUBSTATE_WEIGHT_PRESS then
			-- Release the UP button after 10 frames.
			if M.pressed & ACTION == ACTION then
				if M.buttonHoldTimer == 10 then
					M.buttonHoldTimer = 0
					M.Action.field:set_value(0)
					M.pressed = M.pressed & ~ACTION
				else
					M.buttonHoldTimer = M.buttonHoldTimer + 1
				end
			end
			
			-- Wait here until the "power" reaches 1700, then press.
			if mem:read_u32(CURRENT_POWER) >= 0x01070000 then
				-- Press the UP button, and lift!
				if M.pressed & ACTION ~= ACTION then
					M.RunLeft.field:set_value(0)
					M.RunRight.field:set_value(0)
					M.Action.field:set_value(1)
					M.pressed = ACTION				
				end
				
				-- Wait for the "Judges" to signify good lift.  0x94 = "All 3 lights", it goes 0, 1, 2, 0x94
				if mem:read_u8(JUDGE_LIGHTS) == 0x94 then
					M.subState = SUBSTATE_WEIGHT_WAITING
				else
					M.run(4)
				end
			else
				M.run(4)
			end
		end	
	elseif M.currentState == STATE_POLE_VAULT then		
		-- Check for event number change
		event = math.fmod(mem:read_u8(EVENT_NUMBER), 7)
		if  event ~= 6 then
			M.currentState = STATE_SWIMMING
			M.subState = SUBSTATE_SWIMMING_WAITING
			M.reset()
			M.temp = 0
			return
		end
	
		if M.subState == SUBSTATE_VAULT_WAITING then
			-- Start to plant the pole here
			if mem:read_u16(SCREEN_SCROLL) == 0x9C00 then
				M.Action.field:set_value(1)
				M.pressed = ACTION
				M.subState = SUBSTATE_VAULT_UP
			end
			M.run(4)
		elseif M.subState == SUBSTATE_VAULT_UP then
			-- Release the pole here
			if mem:read_u32(0x1028) >= 0x41ABA665 then
				if M.pressed & ACTION == ACTION then
					M.Action.field:set_value(0)
					M.pressed = M.pressed & ~ACTION
					M.subState = SUBSTATE_VAULT_OVER
					M.temp = M.frameCounter
				end
			end			
			M.run(4)
		elseif M.subState == SUBSTATE_VAULT_OVER then
			if M.frameCounter >= M.temp + 85 then
				if M.frameCounter >= M.temp + 250 then
					M.subState = SUBSTATE_VAULT_WAITING					
				end
				if M.pressed & ACTION == ACTION then
					M.Action.field:set_value(0)
					M.pressed = M.pressed & ~ACTION
				else
					M.Action.field:set_value(1)
					M.pressed = ACTION
				end
			end
			M.run(4)
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
