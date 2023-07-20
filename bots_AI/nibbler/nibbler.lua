-- Let's play Nibbler!

--[[
There are 11 fruit patterns and 8 mazes

There are 45 patterns required to cover all of them at every speed.

{maze=MAZE_1, pattern=FRUIT_PATTERN_01},    -- Level 01
{maze=MAZE_1, pattern=FRUIT_PATTERN_03},    -- Level 07

{maze=MAZE_2, pattern=FRUIT_PATTERN_01},    -- Level 02
{maze=MAZE_2, pattern=FRUIT_PATTERN_04},    -- Level 08
{maze=MAZE_2, pattern=FRUIT_PATTERN_06},    -- Level 12

{maze=MAZE_3, pattern=FRUIT_PATTERN_01},    -- Level 03
{maze=MAZE_3, pattern=FRUIT_PATTERN_02},    -- Level 18
{maze=MAZE_3, pattern=FRUIT_PATTERN_11},    -- Level 30

{maze=MAZE_4, pattern=FRUIT_PATTERN_02},    -- Level 04
{maze=MAZE_4, pattern=FRUIT_PATTERN_10},    -- Level 20

{maze=MAZE_5, pattern=FRUIT_PATTERN_05},    -- Level 11
{maze=MAZE_5, pattern=FRUIT_PATTERN_09},    -- Level 17

{maze=MAZE_6, pattern=FRUIT_PATTERN_07},    -- Level 13

{maze=MAZE_7, pattern=FRUIT_PATTERN_01},    -- Level 15

{maze=MAZE_8, pattern=FRUIT_PATTERN_08},    -- Level 16

--]]

local FRUIT_PATTERN_01 = 1
local FRUIT_PATTERN_02 = 2
local FRUIT_PATTERN_03 = 3
local FRUIT_PATTERN_04 = 4
local FRUIT_PATTERN_05 = 5
local FRUIT_PATTERN_06 = 6
local FRUIT_PATTERN_07 = 7
local FRUIT_PATTERN_08 = 8
local FRUIT_PATTERN_09 = 9
local FRUIT_PATTERN_10 = 10
local FRUIT_PATTERN_11 = 11

local MAZE_1 = 1
local MAZE_2 = 2
local MAZE_3 = 3
local MAZE_4 = 4
local MAZE_5 = 5
local MAZE_6 = 6
local MAZE_7 = 7
local MAZE_8 = 8

-- We have to define these, as we have to make a decision about which pattern to use at a time
-- when the game hasn't yet populated them.  I could have waited a couple of frames, but this was easier.
local Levels = {
                    {maze=MAZE_1, pattern=FRUIT_PATTERN_01},    -- Level 01
                    {maze=MAZE_2, pattern=FRUIT_PATTERN_01},    -- Level 02
                    {maze=MAZE_3, pattern=FRUIT_PATTERN_01},    -- Level 03
                    {maze=MAZE_4, pattern=FRUIT_PATTERN_02},    -- Level 04
                    {maze=MAZE_2, pattern=FRUIT_PATTERN_01},    -- Level 05
                    {maze=MAZE_3, pattern=FRUIT_PATTERN_01},    -- Level 06
                    {maze=MAZE_1, pattern=FRUIT_PATTERN_03},    -- Level 07
                    {maze=MAZE_2, pattern=FRUIT_PATTERN_04},    -- Level 08
                    {maze=MAZE_3, pattern=FRUIT_PATTERN_01},    -- Level 09
                    {maze=MAZE_4, pattern=FRUIT_PATTERN_02},    -- Level 10
                    {maze=MAZE_5, pattern=FRUIT_PATTERN_05},    -- Level 11
                    {maze=MAZE_2, pattern=FRUIT_PATTERN_06},    -- Level 12
                    {maze=MAZE_6, pattern=FRUIT_PATTERN_07},    -- Level 13
                    {maze=MAZE_1, pattern=FRUIT_PATTERN_03},    -- Level 14
                    {maze=MAZE_7, pattern=FRUIT_PATTERN_01},    -- Level 15
                    {maze=MAZE_8, pattern=FRUIT_PATTERN_08},    -- Level 16
                    {maze=MAZE_5, pattern=FRUIT_PATTERN_09},    -- Level 17
                    {maze=MAZE_3, pattern=FRUIT_PATTERN_02},    -- Level 18
                    {maze=MAZE_6, pattern=FRUIT_PATTERN_07},    -- Level 19
                    {maze=MAZE_4, pattern=FRUIT_PATTERN_10},    -- Level 20
                    {maze=MAZE_5, pattern=FRUIT_PATTERN_05},    -- Level 21
                    {maze=MAZE_8, pattern=FRUIT_PATTERN_08},    -- Level 22
                    {maze=MAZE_7, pattern=FRUIT_PATTERN_01},    -- Level 23
                    {maze=MAZE_1, pattern=FRUIT_PATTERN_03},    -- Level 24
                    {maze=MAZE_6, pattern=FRUIT_PATTERN_07},    -- Level 25
                    {maze=MAZE_5, pattern=FRUIT_PATTERN_09},    -- Level 26
                    {maze=MAZE_8, pattern=FRUIT_PATTERN_08},    -- Level 27
                    {maze=MAZE_4, pattern=FRUIT_PATTERN_10},    -- Level 28
                    {maze=MAZE_7, pattern=FRUIT_PATTERN_01},    -- Level 29
                    {maze=MAZE_3, pattern=FRUIT_PATTERN_11},    -- Level 30
                    {maze=MAZE_5, pattern=FRUIT_PATTERN_09},    -- Level 31
                    {maze=MAZE_8, pattern=FRUIT_PATTERN_08},    -- Level 32 - AKA Level 00 after "level & 31"
               }

-- These are the "speed ramps" used by the game, and the one that's used is determined by a dipswitch setting
local EasySpeeds = {2, 2, 
					3, 3, 3, 3,
					4, 4, 4, 4,
					5, 5, 5, 5,
					6, 6, 6, 6, 6, 6
}			   

local HardSpeeds = {2, 2, 
					3, 
					4, 4, 
					5, 5, 5, 
					6, 6, 6, 6, 6, 6
}								   

-- These are the files that contain the patterns for the mazes
dofile("Maze1.lua")
dofile("Maze2.lua")
dofile("Maze3.lua")
dofile("Maze4.lua")
dofile("Maze5.lua")
dofile("Maze6.lua")
dofile("Maze7.lua")
dofile("Maze8.lua")

local M = {}

-- Define the hardware interfaces we'll use
local cpu = manager.machine.devices[":maincpu"]
local mem = cpu.spaces["program"]
local ioport = manager.machine.ioport
local in0 = ioport.ports[":IN0"]
local in2 = ioport.ports[":IN2"]
local dsw = ioport.ports[":DSW"]

-- These are the things based on ports.
M.move_up    = { in0 = in0, field = in0.fields["P1 Up"] }
M.move_down  = { in0 = in0, field = in0.fields["P1 Down"] }
M.move_left  = { in0 = in0, field = in0.fields["P1 Left"] }
M.move_right = { in0 = in0, field = in0.fields["P1 Right"] }
M.start1     = { in2 = in2, field = in2.fields["1 Player Start"] }
M.difficulty = { dsw = dsw, field = dsw.fields["Difficulty"] }

-- Set our variables to their initial values
M.wave = 0
M.totalWave = 0
M.step = 1
M.levelDone = true
M.startReady = false
M.isHard = false;

-- This functions like a pointer to the current move set.
local Maze = {}

local _Level
local _Maze
local _Pattern
local _Speed
local _LastScore
local _Billions

function comma_value(amount)
  local formatted = amount
  while true do  
    formatted, k = string.gsub(formatted, "^(-?%d+)(%d%d%d)", '%1,%2')
    if (k==0) then
      break
    end
  end
  return formatted
end

-- This converts the score from BCD to "normal"
function convertScore()
	-- Get the current score from game RAM
	bcd_score = mem:read_u32(0xB2)
	
	-- Convert it to a string of hex digits, BUT, this being BCD, all digits will be 0-9
	score_string = string.format("%X0", bcd_score)
	
	-- So, we can convert it to a DECIMAL like this
	score = tonumber(score_string, 10)
	
	-- Now, if the score has DECREASED, this means it has went back to 0, meaning we're crossed a Billion point threshold
	if score < _LastScore then
		-- So, increment the Billions counter
		_Billions = _Billions + 1
	end
	
	-- Update the Last Score, so that we can compare again next level
	_LastScore = score

	if _Billions > 0 then
		score_string = string.format("%09d", score)
		print("Current Score: " .. tostring(_Billions) .. "," .. comma_value(score_string))
	else	
		-- Just print the current score
		print("Current Score: " .. comma_value(score_string))
	end
end

-- function called every frame (with mem-read support)
function M.updateMem()

    -- If we've progressed to the next level
    if M.wave ~= mem:read_i8(0xBC) then
        -- Sanity check
        if mem:read_i8(0xBC) <= 0 then
            return
        end

        -- Try to correct the weird start-up errors
        if M.startReady == false and mem:read_i8(0xBC) == 1 then
            M.startReady = true
			
			-- Set this based on the difficulty dipswitch setting.
			M.isHard = ((dsw:read() & 4) == 4)
        end

        if M.startReady == false then
            return
        end

        M.lives     = mem:read_u8(0xB0)
        M.wave      = mem:read_i8(0xBC)
        M.totalWave = M.totalWave + 1

        print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
        print("Current Wave:  " .. M.wave)
        print("Current Lives: " .. M.lives)
		convertScore()		
		
        print("\nTotal Waves:   " .. comma_value(tostring(M.totalWave)) .. "\n")

        M.levelDone = false;

        -- Set the Maze to use here
        _Level = (M.wave & 31)

        -- If we got 0, we use 32.
        if _Level == 0 then
            _Level = 32
        end

        _Maze = Levels[_Level]['maze']
        _Pattern = Levels[_Level]['pattern']

		-- These values are based on the dipswitch setting
		if M.isHard == false then
			-- If the game is set to EASY, you get 20 waves before everything is speed 7
			if M.wave > 20 then
				_Speed = 7
			else
				_Speed = EasySpeeds[M.wave]
			end
		else
			-- If it's HARD, then you get only 14 waves before speed 7.
			if M.wave > 14 then
				_Speed = 7
			else
				_Speed = HardSpeeds[M.wave]
			end
		end

		print("=-=-=-=-[ Current Wave Info ]=-=-=-=-")
        print("Level (1-32):       " .. _Level)
        print("Maze (1-8):         " .. _Maze)
        print("Dot Pattern (1-11): " .. _Pattern)
		print("Speed (2-7):        " .. _Speed)

        -- This would be easier if there was a  switch/case
        if _Maze == 1 then
            if _Pattern == 1 then
				Maze = Maze_1_Pattern_1[_Speed]
            elseif _Pattern == 3 then
				Maze = Maze_1_Pattern_3[_Speed]
            else
                print("Unknown Maze 1 pattern " .. _Pattern)
                emu.pause()
            end
        elseif _Maze == 2 then
            if _Pattern == 1 then
				Maze = Maze_2_Pattern_1[_Speed]
            elseif _Pattern == 4 then
				Maze = Maze_2_Pattern_4[_Speed]
            elseif _Pattern == 6 then
                Maze = Maze_2_Pattern_6[_Speed]
            else
                print("Unknown Maze 2 pattern " .. _Pattern)
                emu.pause()
            end
        elseif _Maze == 3 then
            if _Pattern == 1 then
				Maze = Maze_3_Pattern_1[_Speed]
			elseif _Pattern == 2 then
                Maze = Maze_3_Pattern_2[_Speed]
			elseif _Pattern == 11 then			
                Maze = Maze_3_Pattern_11[_Speed]
            else
                print("Unknown Maze 3 pattern " .. _Pattern)
                emu.pause()
            end
        elseif _Maze == 4 then
            if _Pattern == 2 then
                Maze = Maze_4_Pattern_2[_Speed]
            elseif _Pattern == 10 then
				Maze = Maze_4_Pattern_10[_Speed]
            else
                print("Unknown Maze 4 pattern " .. _Pattern)
                emu.pause()
            end
        elseif _Maze == 5 then
            if _Pattern == 5 then
				Maze = Maze_5_Pattern_5[_Speed]
            elseif _Pattern == 9 then
                Maze = Maze_5_Pattern_9[_Speed]
            else
                print("Unknown Maze 5 pattern " .. _Pattern)
                emu.pause()
            end
        elseif _Maze == 6 then
            if _Pattern == 7 then
				Maze = Maze_6_Pattern_7[_Speed]
            else
                print("Unknown Maze 6 pattern " .. _Pattern)
                emu.pause()
            end
        elseif _Maze == 7 then
            if _Pattern == 1 then
                Maze = Maze_7_Pattern_1[_Speed]
            else
                print("Unknown Maze 7 pattern " .. _Pattern)
                emu.pause()
            end
        elseif _Maze == 8 then
            if _Pattern == 8 then
                Maze = Maze_8_Pattern_8[_Speed]
            else
                print("Unknown Maze 8 pattern " .. _Pattern)
                emu.pause()
            end
        else
            print("Unimplemented Maze " .. _Maze)
            emu.pause()
        end
		
		-- If Maze has 0 length, it's empty, aka bad.
		if #Maze == 0 then
			print("No moves for this Maze/Pattern/Speed combo")
			emu.pause()
		end

        -- Say that we're ready to begin
        M.step = 1
		
        -- Grab the 1st item
        M.targetAddress   = Maze[M.step]['address']
        M.targetCharacter = Maze[M.step]['character']
        M.targetAction    = Maze[M.step]['action']
    end

    -- If level isn't active, don't do anything
    if M.levelDone == true then
        return
    end
	
    -- Monitor the target VMEM address
    if mem:read_i8(M.targetAddress) == M.targetCharacter then

        -- Clear up the previous joystick input
		M.move_down.field:set_value(0)
		M.move_up.field:set_value(0)
		M.move_right.field:set_value(0)
		M.move_left.field:set_value(0)

		-- Set the CURRENT joystick input
        if M.targetAction == DOWN then
            M.move_down.field:set_value(1)
        elseif M.targetAction == UP then
            M.move_up.field:set_value(1)
        elseif M.targetAction == RIGHT then
            M.move_right.field:set_value(1)
        elseif M.targetAction == LEFT then
            M.move_left.field:set_value(1)
        end

		-- Increment our pointer into the moves array
		M.step = M.step + 1

		-- Initialize the other variables based on the components of the move
        M.targetAddress   = Maze[M.step]['address']
        M.targetCharacter = Maze[M.step]['character']
        M.targetAction    = Maze[M.step]['action']
	end

	-- This monitors the number of "dots" left.
	-- the "step > 1" makes sure it doesn't trigger before the level has even started.
    if mem:read_i8(0xBA) == 0 and M.step > 1 then
        print("Wave Complete!\n\n\n")
		
        M.levelDone = true
		
        -- Clear up the previous joystick input
		M.move_down.field:set_value(0)
		M.move_up.field:set_value(0)
		M.move_right.field:set_value(0)
		M.move_left.field:set_value(0)
    end
end

-- start game
function M.start()
    M.step = 0
	_Billions = 0
	_LastScore = 0
	
    -- Press 1-player start button
    M.start1.field:set_value(0x80)
	
    -- register update loop callback function
    emu.register_frame_done(M.updateMem, "frame")	
	
	-- This allows the =-=-=- line to be on a clean line.
	print("\n")
end

M.start()

return M
