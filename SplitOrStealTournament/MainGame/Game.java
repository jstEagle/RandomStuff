package MainGame;

import java.util.List;
import java.util.ArrayList;
import java.util.Map;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Arrays;
import java.util.Comparator;

public class Game {

    private static List<GameBot> bots = new ArrayList<>();
    
    private static Map<GameBot, Integer> BotScores = new HashMap<>();
    
    public static void main(String[] args) {
        GameBot MenaceBot = new MenaceBot();  
        GameBot RandomBot = new RandomBot();
        GameBot ExtremelyPoliteBot = new ExtremelyPoliteBot();

        bots.add(MenaceBot);
        bots.add(RandomBot);
        bots.add(ExtremelyPoliteBot);

        for(GameBot bot : bots) {
            BotScores.put(bot, 0);
        }

        // Implement the tournament
        Iterator<GameBot> iterator = bots.iterator();
        while(iterator.hasNext()) {
            GameBot bot1 = iterator.next();
            for(GameBot bot2 : bots) {
                if(!(bot1.Name().equals(bot2.Name()))) {
                    PlayRound(bot1, bot2);
                }
            }
            iterator.remove();  // Safely remove the current bot from the list
        }
        System.out.println();

        // Evaluation
        Integer[] scores = new Integer[BotScores.size()];

        int index = 0;
        for (Map.Entry<GameBot, Integer> entry : BotScores.entrySet()) {
            scores[index] = entry.getValue();
            index++;
        }

        Arrays.sort(scores, Comparator.reverseOrder());

        int n = 0;
        while (n < index) {
            for (Map.Entry<GameBot, Integer> entry : BotScores.entrySet()) {
                Integer value = entry.getValue();
                if (value.equals(scores[n])) {
                    System.out.println((n + 1) + ") " + entry.getKey().Name() + ": " + value);
                    n++;
                    break;
                }
            }
        }
        
    }

    public static void PlayRound(GameBot bot1, GameBot bot2) {
        String ANSI_RESET = "\u001B[0m";
        String ANSI_RED = "\u001B[31m";
        String ANSI_BLUE = "\u001B[34m";
        String ANSI_GREEN = "\u001B[32m";
        
        int gameLength = 10;
        int[][] game = new int[2][gameLength];
        //[0, 1, 0, 1, 0, 1, 1, 1, ...] Player 1
        //[0, 1, 1, 0, 1, 1, 1, 0, ...] Player 2
        int bot1Score = 0;
        int bot2Score = 0;

        // Initialize the game array to -1
        for(int i = 0; i < game.length; i++) {
            for(int j = 0; j < game[0].length; j++) {
                game[i][j] = -1;
            }
        }

        System.out.println();
        System.out.println();

        String title = bot1.Name() + " vs " + bot2.Name();
        System.out.println(title);

        System.out.println("-".repeat(title.length()));
        
        for(int i = 0; i < gameLength; i++) {
            int bot1Move = bot1.makeMove(game, 0);
            int bot2Move = bot2.makeMove(game, 1);

            game[0][i] = bot1Move;
            game[1][i] = bot2Move;

            if(bot1Move == 1) {
                if(bot2Move == 1) {
                    bot1Score++;
                    bot2Score++;
                    System.out.print(ANSI_RED + "Steal" + ANSI_RESET + " | " + ANSI_RED + "Steal" + ANSI_RESET);
                } else {
                    bot1Score += 5;
                    System.out.print(ANSI_RED + "Steal" + ANSI_RESET + " | " + ANSI_BLUE + "Split" + ANSI_RESET);
                }
            } else {
                if(bot2Move == 1) {
                    bot2Score += 5;
                    System.out.print(ANSI_BLUE + "Split" + ANSI_RESET + " | " + ANSI_RED + "Steal" + ANSI_RESET);
                } else {
                    bot1Score += 3;
                    bot2Score += 3;
                    System.out.print(ANSI_BLUE + "Split" + ANSI_RESET + " | " + ANSI_BLUE + "Split" + ANSI_RESET);
                }
            }
            System.out.println();
        }
        System.out.println();

        if(bot1Score > bot2Score) {
            System.out.println(ANSI_GREEN + bot1.Name() + " Score: " + bot1Score + ANSI_RESET);
            System.out.println(ANSI_RED + bot2.Name() + " Score: " + bot2Score + ANSI_RESET);
        } else {
            System.out.println(ANSI_GREEN + bot2.Name() + " Score: " + bot2Score + ANSI_RESET);
            System.out.println(ANSI_RED + bot1.Name() + " Score: " + bot1Score + ANSI_RESET);
        }
        

        updateScore(bot1Score, bot1);
        updateScore(bot2Score, bot2);
    }

    private static void updateScore(Integer score, GameBot bot) {
        Integer prev = BotScores.get(bot);
        BotScores.put(bot, prev + score); // Adds the new score onto the previous score
    }

    interface GameBot {
        int makeMove(int[][] game, int player);
        String Name();
    }
}