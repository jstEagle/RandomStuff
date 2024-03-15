package MainGame;

import MainGame.Game.GameBot;

public class MenaceBot implements GameBot{
    public static String BotName = "Menace Bot";

    public int makeMove(int[][] game, int player) {
        return 1;
    }

    public String Name() {
        return BotName;
    }
}
