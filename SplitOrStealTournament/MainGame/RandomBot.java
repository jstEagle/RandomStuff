package MainGame;

import java.util.Random;

import MainGame.Game.GameBot;

public class RandomBot implements GameBot {
    public static String BotName = "Random Bot";

    public int makeMove(int[][] game, int player) {
        Random rand = new Random();

        return rand.nextInt(2);
    }
    
    public String Name() {
        return BotName;
    }
}