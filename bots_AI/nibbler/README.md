# NibblerBot
LUA code to play Nibbler inside MAME

This was the FIRST thing I'd ever written in LUA, so I learned as I went, so there could be some bits that are brute-force when there
was a much more elegant way to do it.  Sorry if this offends you, I just wanted to get the LUA bits done.

And now, the FAQ:

#1 - What IS this?
It’s a LUA script running inside of MAME playing Nibbler version 9.

#2 - So, it’s a TAS?
Short answer: No, this is very different!
Long answer: No, most TASbot runs base EVERYTHING off of the frame #.  All moves are input based on the frame number, and the script that inputs the moves is mostly dumb. You’ll often hear TAS runners speak of their scripts becoming unsynced.  That doesn’t happen with my bot.  THIS script monitors video memory for the nose of the snake.  When the nose arrives at the location we’re interested in, we input the joystick movement, and go to the next item in the array of moves. In that sense, it plays the same way that a human player would.  You watch for the snake to get to a specific point, and then move the joystick.  It can also detect the dipswitch being set to EASY or HARD, and adjusts accordingly, it queries memory locations inside the game to provide the current wave, score, and several other metrics you see in the command prompt-like window.

#3 - What are you trying to do?
Short answer: Spur people to write their OWN bots that play other classic arcade games in MAME.
Long answer: Ever since MAME arrived on the scene, I’ve had an interest in writing a bot (or bots!) to play arcade games.  This wasn’t really possible until recently, when the LUA interpreter and bindings were added to MAME.  I’d LOVE to see more bots appear!

#4 - You realize no one will consider your “World Record” legitimate, right?
Answer: OF COURSE!  I have no desire to have the record.  I just wanted people to notice this, and maybe write their own bots!

#5 - Wait, why are some of your levels finishing before you eat the last “dot”?
Short answer: There’s a “bug/feature” in the game.
Long answer:  When the snake moves, the only things that really move are the head, and the tail.  The head moves a chunk, and the space it used to occupy is filled in with snake body.  Then, the tail moves a chunk, and the space it used to occupy is redraw as the maze.  So, the tail has to be able to follow the head.  This means that every time the head changes directions, that “corner” must be noted.  The game maintains an internal “list” of these corners via a circular buffer.  This buffer contains 32 16-bit values.  When the number of corners exceeds this, the game throws in the towel, and just finishes the level instead of overwriting the location pointed to by the tail pointer.  If you pause the video on any level that ends early, you can count 31 “bends” or “corners”, and the head, and tail.  This is enough to overflow the buffer.

#6 - Can you PROVE this?
Answer: Yes, see actual 6502 assembly code from the game disassembled below.

#7 - How did you discover this?
Answer: When I decided I wanted to write a bot to play nibbler, I realized that I had a problem.  I was TERRIBLE at the game, had no patterns of my own, and as such, couldn’t contribute any intelligence to the bot.  So, (skip ahead 9 months!) I wrote an app that “plays” nibbler.  (No graphics, and I wrote it in C/C++, not 6502 assembly).  This app spawns a (CPU-Thread count) number of threads, reads in the maze data from files that I captured from the video RAM of the game, and tries to find a solution.  AKA a pattern, that works, with the fewest moves.  This app took WAY too long to write, and get debugged, but once it did, it started to spit out patterns.  Once the patterns got to a low enough count of moves to not seem tedious, I ran them through my python script to convert the solution files into lists of moves that the LUA script would consume.  Once I put some of these in, I watched it play, and saw Waves 10 & 11 end “prematurely”.  I thought this was odd, but let it go.  Once I had almost a full set, I made a video and showed it to some friends, who also asked the same question.  “Why is it ending like that?”.  So, I had to find out why.  I concatenated the ROM files in the correct order, and loaded them into IDA Pro.  Using the MAME debugger, a lifetime of assembly debugging skills, and some good old fashioned luck, I found where this was happening in the code, and then set about commenting it, and trying to understand it.  After a couple of hours, I understood what was going on.

#8 - Can *I* make the levels end earlier while playing?
Answer: YES, I invite you to copy any of my patterns, and try them yourself.  You should get the exact same results.  As I mentioned above, Wave 10 was the first one that I saw it happen on.  The waves with no walls (wave 3 for example) are the easiest to do it on.  (But, you can’t do it ON Wave 3, as your snake doesn’t grow long enough to cover 32 corners).

#9 - Are you cheating?
Answer: Nope, not at all.  The ROMs are completely unmodified, and my LUA code only READS memory from the game, it NEVER writes.  The only things my LUA script “inputs” are the start button to start the game, and the joystick movements to move the snake.

#10 - No, I meant, are some of your patterns designed to get to 32 moves, and end the level as quickly as possible?
Answer: No, as I said above, I’m a TERRIBLE Nibbler player, and used my app to find patterns, and IT doesn’t care about the number of “corners”, it only cares about the number of “dots” left.  So, nope!

#11 - Why are some of your patterns so SPASTIC?
Answer: Because they’re computer generated based on random numbers.  “Choose a random number, is that direction OPEN?  If yes, GO that way.  If no, pick a new random number, and try again.”  It seems to have a thing for “UP” and “LEFT”, and I’m not really sure why.

#12 - WHY did you do this again?
Answer: As the late Larry Walters of Los Angeles said after he tied weather balloons to his lawn chair and floated up to 10,000 feet said “A man can’t just sit around!”.  

#13 - What did it take to do this?
Answer: 9 months, and the following technologies:  6502 assembly, C, C++, Python, LUA, and even some DOS batch in the early days to run my pattern finder over and over for the different mazes.

#14 - Where’s that assembly listing you spoke about in #6?
Answer: Here!  (Of course, all names come from me).
```
ROM:3BE6 loc_3BE6:
ROM:3BE6                 LDA     Head_X_value
ROM:3BE8                 LDY     headPtr
ROM:3BEA                 STA     (moveSlotPtr),Y
ROM:3BEC                 INY
ROM:3BED                 LDA     Head_Y_value
ROM:3BEF                 STA     (moveSlotPtr),Y
ROM:3BF1                 INY
ROM:3BF2                 STY     headPtr
ROM:3BF4                 LDA     #$3F
ROM:3BF6                 AND     headPtr
ROM:3BF8                 STA     headPtr
; If headPtr == tailPtr, BAD JUJU!
ROM:3BFA                 CMP     tailPtr
ROM:3BFC                 BNE     circularBufferOK
; Just end the level to prevent circular buffer overflow
ROM:3BFE                 LDA     #0              
ROM:3C00                 STA     FruitsLeft
ROM:3C02                 LDA     #9
ROM:3C04                 JSR     saveDebugValues
ROM:3C07                 JMP     functionExit
ROM:3C0A ; ---------------------------------------------------------------------------
ROM:3C0A
ROM:3C0A circularBufferOK:
ROM:3C0A                 LDA     #$F
ROM:3C0C                 STA     byte_5E
ROM:3C0E                 STA     soundRelated
ROM:3C10                 LDA     SnakeRow
ROM:3C12                 STA     moveToRow
ROM:4FDB functionExit:
ROM:4FDB                 JSR     draw_fruits
ROM:4FDE                 LDA     #$10
ROM:4FE0                 AND     byte_F0
ROM:4FE2                 BEQ     loc_4FE9
ROM:4FE4                 LDA     #5
ROM:4FE6                 JMP     loc_4FEB
```

#15 - So, having worked on this thing for 9 months, I bet you know a lot about it.  What can you tell us about the game?
Answer: LOTS.  
There are only 8 mazes.  
But, there are a total of 11 different patterns for the “dots”.  (Not 11 per maze, 11 total).  No maze has more than 3 different patterns for itself, and most of them have less.  
The 1st 3 levels use the same dot pattern!  If you put your finger on a dot during Wave 1, you’ll see that there’s also a dot there for Waves 2, and 3.
There are 6 speeds, (2 - 7).  The speeds are represented by the distance the head moves per frame.  The distance COULD match the speed level, I haven’t gotten that deeply into it.  On my simulator, I assumed it did, and it seemed to work.  
There are 2 dipswitch settings, Easy, and Hard.  The difference between them is how soon you get to speed 7.  On Easy, wave 21 is the 1st speed 7 level. On HARD, it’s wave 15.  Once you reach speed 7, it never goes back.  It’s that speed until the end of your game. The waves go from Wave 1 at the start, to Wave 99, and then it repeats waves 80-99 forever.  
There are really only 32 individual levels, which repeat forever.  (I track that in the metrics).
If you’re playing the EASY difficulty, There are 34 distinct levels.  (When you consider speeds, mazes, and dot patterns).  Whereas HARD difficulty only has 29.  If you want to be able to handle either, the number is 42.  MANY of the levels are shared between them both.
The “Extra lives” bug that you hear about.  This ROM set seems to have fixed it, or at least lessened its impact.  The way the game is, you get an extra live for every 4 waves you complete.  The field that stores the lives is an 8-bit byte, which means values from 0-255.  I’ve watched the lives go from 254, to 255, to 0.  Which means that despite the fact that you’ve played so well that you have 256 lives in reserve, if you die in that 4 level window where it’s 0, you’ll get a game over.  Fortunately, my bot never dies.  :-)  
If you’ve not noticed, the last digits of the score, and the time never change.  They’re always 0.  That’s because the time is represented by 1 BCD byte, and the score is represented by 4.  So, there’s no ROOM to support those bytes, so the code just prints a “0” there.
The game has the ability to have each wave have a different amount of time at the start.  But they’re all set to “99”.  So, this could have been a MUCH harder game.
Using my bot, it takes 9,993 waves to reach a billion points starting from 0.  But, since the earlier levels are fewer points, the 2nd, and all subsequent billions should take a few less.
As we know from watching “Man vs. Snake” it took Tim McVey 48 hours to reach 1 billion points.  On my PC, I can turn off the throttle, and achieve it in 102 minutes.
And MUCH more, if there’s something you want to know specifically, ASK!

#16 - Why Nibbler?
Answer - Man vs. Snake reminded me that it existed.  I remembered playing it once or twice at an arcade in the 80’s, and most importantly:  There are no enemies, so there’s no RNG!  It’s simply a test of your ability to repeat a pattern.  Something that a bot would be GREAT at.  

#17 - What now?
Answer:  Now that I have my first bot under my belt, I plan to do OTHERS.  As my skills grow, I plan to do harder games, as that’s really my objective.  Get “revenge” on the games that I was mediocre, or just plain BAD at in the arcades.  I’ve also been talking to a friend involved with video games, and we’ve discussed doing a “computer vision” tied to a set of actuators version of this that plays an actual arcade machine.  Yeah, we’re nerds.  :-)  

#18 - Did it REALLY take 9 months to do this?
Short Answer: MOSTLY.  I also changed jobs, moved, and took some time off  in the middle. 
LONG Answer: The VAST majority of the time was spent on “snake mover” which was my simulator that allowed me to find these freaky patterns.  The issue was that the game runs until the snake bites itself, or runs out of time.  I wasn’t going to deal with time, as I figured if I ground the patterns down to a very few moves, they’d always be fast enough.  The problem isn’t moving the snake forward, it’s moving it BACKWARDS when it bites itself.  You have to rewind it to the last intersection, and find a direction that you haven’t already been.  If all the directions have been tried, you have to rewind back to the previous junction before THAT one.  And maybe move back, and back, and back.  As it’s possible that one of the very early moves was wrong, and you have to rewind ALL the way back to that.  There are LOTS of corner cases!

#19 - What do you think of Tim McVey’s score now?
Answer: It’s nothing short of incredible!  This game gets FAST, and to be able to make the movements reliably time after time for 48 hours is just insane.  Not to mention having the mental wherewithal to be able to recover for a death to find a pattern that clears the board.  (Something I don’t have to deal with here).

#20 - Looking at the Maze*.lua files, what's with the format?
Answer: They're arranged by physical maze (there are 8 of them), and then by dot pattern (up to 4 per maze), and then by speed.  The content of a single line is like this: {address = 0x045d, character = 0x35, action = UP}.  This says to monitor video memory address 0x045D, and watch for the value 0x35 to arrive there.  Once it does, move the joystick UP.  The reason that the "character" field exists, is that the character for the nose of the snake is different for vertical, and horizontal snakes.  (They're rotated after all).

#21 - Where can I see it in action?
Answer:  HERE!  https://youtu.be/60gVbJTOUOo
