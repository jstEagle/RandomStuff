The main part of your bot will consist of a makeMove() function. This function will take in a 2d integer array and an integer. The array is the game board so to speak and the integer is the player. The player number labeled "player" indicates which row of the 2d array your bot plays in. So if the player number is 0, your bot is playing in the first row. If it is 1 then your bot is playing in the second row. (Note: the bot does not have to take this value into consideration when deciding a move. This is only so that incase you wish to look at your previous moves or more importantly your opponents previous moves you can do so).

Rules:
- Each turn a bot may either split (0) or steal (1)
- If both bots split then each get +3 points
- If bot A chooses to steal while bot B chooses to split then bot A receives +5 points and bot B receives none
- If both bots choose to steal then each bot receives +1 point
- Each bot must make a move each turn
- The bots program may not interfere with the main game program or other bots programs
- Each bot will play against all the other bots once
- The bot with the most points overall is the winner!

Here is an example of what a random bot might look like. 
```java
package MainGame; //Must import the package

import java.util.Random;
import MainGame.Game.GameBot; //Must import Game class

public class RandomBot implements GameBot {
	public static String BotName = "Random Bot"; 

	public int makeMove(int[][] game, int player) { //Must implement makeMove
		Random rand = new Random();
		return rand.nextInt(2); //Chooses either 0 or 1
	}

	public String Name() { //Must implement Name() class
		return BotName;
	}
}
```
This bot (when makeMove() is called) will pick a random integer between 0 and 1. This means that it is a 50 - 50 chance of split or steal. (not a very good approach).

The standard boilerplate needed for the code to be accepted is as follows:
```java
package MainGame;

import MainGame.Game.GameBot;

public class Bot implements GameBot {
	public int makeMove(int[][] game, int player) {
		//Decide to either split (0) or steal (1)
		return Move;
	}

	public String Name() {
		String name = "Example Name";
		return name;
	}
}
```

I have also provided code to find the index of the last move played by any opponent to use in your calculation.
To find the index of the last played move by a player:
```java
int indexOfLastMove = Game.findGameIndex(int[][] game, int player);
```
