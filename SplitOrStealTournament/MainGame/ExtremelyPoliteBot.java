package MainGame;

import MainGame.Game.GameBot;

public class ExtremelyPoliteBot implements GameBot {
    public static String BotName = "Extremely Nice Bot";

    public int makeMove(int[][] game, int player) {
        return 0;
    }

    public String Name() {
        return BotName;
    }
}