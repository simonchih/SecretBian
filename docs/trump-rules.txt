Secret Trump is the game similar with board game Secret Hitler.

==Environment==
Python 3 and Pygame

Game Rule:
10 players join this game. Only one is human player, others are computer.
Three players are the member of Republican Party. Six players are the member
of Democratic Party. The last one is D.T. The member of Republican Party and 
D.T. belong to Republican Party.

The player name of human is "Tina". The image near "Tina" is the role of player.
The roles include Donkey (Democratic Party), Elephant (Republican Party) and D.T.
The member of Republican Party (NOT include D.T.) can know Republican Party
members each other. Other roles only know the role yourself at the beginning.

At the game start, random to pick up one player as president candidate.
President candidate can select a chancellor candidate. A chancellor candidate
can't be the last president, chancellor or dead player. A president candidate 
and chancellor candidate will win an election if accepted tickets more than
deny tickets. Otherwise, to increase negotiation broke down 1 times. To enact law 
if negotiation broke down 3 times. The laws include Donkey and Elephant only.
The possibility between the law for Donkey and Elephant is 10:19.

If president and chancellor candidate win the election, they can enact law.
To enact law by president, remove one law from three laws. Then the remainder
two laws can remove one law by chancellor. Finally, the last one law is enacted.
If 5 donkey laws are enacted, then Democratic party win the game. If 6 elephant 
laws are enacted then Republican party win the game.

President can kill the other live player while 3 elephant or 5 elephant laws are
enacted. Before the player is killed, it will ask the person "Are you D.T. ?".
Then the player will dead. If D.T. is dead, Democratic party win the game.
Otherwise, the player is dead but the game continues to run.

President can investigate the party of player while 4 elephant laws are enacted.
After investigation, it will show elephant for D.T. and Republican party members.
Otherwise, it will show donkey for Democratic party. The only player to know the
investigation result is the president issue the power. Other players won't know
the investigation result.

After 4 elephant laws are enacted, any president candidate select chancellor
candidate will ask the chancellor candidate, "Are you D.T. ?". The Republican
party win the game if the answer is "Yes". Otherwise, the game continues to run.

Under 4 conditions below, the next president candidate will be the clockwise of 
last live president (candidate): 
1. To lose the election, the negotiation broke down.
2. To enact laws and NO any power action should be executed. (kill or investigation power)
3. After president issue power action. (kill or investigation)
4. The game is restart.
