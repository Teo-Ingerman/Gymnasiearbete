using System;
using System.Text.Json;
using System.Text.Json.Serialization;

class Minesweeper
{
    static void Main()
    {
        // Get user input for the height and length of the Minesweeper grid
        int rows = GetUserInput("Enter the height of the Minesweeper grid: ");
        int cols = GetUserInput("Enter the length of the Minesweeper grid: ");

        // Create the Minesweeper grid
        int[,] minesweeper_grid = new int[rows, cols];

        // Initialize the grid with empty cells
        InitializeGrid(minesweeper_grid);

        // Place mines in approximately 15% of the grid squares
        PlaceMines(minesweeper_grid, 0.15);

        // Calculate the numbers for each cell
        CalculateNumbers(minesweeper_grid);

        // Display the initial state of the Minesweeper grid
        DisplayGrid(minesweeper_grid);

        // Save the Minesweeper grid to a JSON file
        SaveGridToJson(minesweeper_grid, "minesweeper_grid.json");

        // Your Minesweeper game logic goes here...

        Console.ReadLine();
    }

    // Function to create a copy of the grid with all squares set to 9
    static int[,] CreateGameGrid(int rows, int cols)
    {
        int[,] game_grid = new int[rows, cols];

        for (int i = 0; i < game_grid.GetLength(0); i++)
        {
            for (int j = 0; j < game_grid.GetLength(1); j++)
            {
                game_grid[i, j] = 9;
            }
        }

        return game_grid;
    }

    // Function to place mines in approximately a given percentage of the grid squares
    static void PlaceMines(int[,] grid, double percentage)
    {
        Random random = new Random();

        int totalSquares = grid.GetLength(0) * grid.GetLength(1);
        int numMines = (int)(totalSquares * percentage);

        for (int i = 0; i < numMines; i++)
        {
            int index = random.Next(0, totalSquares);

            int row = index / grid.GetLength(1);
            int col = index % grid.GetLength(1);

            // Check if the cell already contains a mine
            while (grid[row, col] == -1)
            {
                index = random.Next(0, totalSquares);
                row = index / grid.GetLength(1);
                col = index % grid.GetLength(1);
            }

            // Place a mine in the selected cell
            grid[row, col] = -1;
        }
    }

    // Function to calculate the numbers for each cell
    static void CalculateNumbers(int[,] grid)
    {
        for (int i = 0; i < grid.GetLength(0); i++)
        {
            for (int j = 0; j < grid.GetLength(1); j++)
            {
                if (grid[i, j] != -1)
                {
                    int count = CountAdjacentMines(grid, i, j);
                    grid[i, j] = count;
                }
            }
        }
    }

    // Function to count the number of mines adjacent to a cell
    static int CountAdjacentMines(int[,] grid, int row, int col)
    {
        int count = 0;

        for (int i = -1; i <= 1; i++)
        {
            for (int j = -1; j <= 1; j++)
            {
                int newRow = row + i;
                int newCol = col + j;

                if (newRow >= 0 && newRow < grid.GetLength(0) && newCol >= 0 && newCol < grid.GetLength(1))
                {
                    if (grid[newRow, newCol] == -1)
                    {
                        count++;
                    }
                }
            }
        }

        return count;
    }

    // Function to initialize the Minesweeper grid with empty cells
    static void InitializeGrid(int[,] grid)
    {
        for (int i = 0; i < grid.GetLength(0); i++)
        {
            for (int j = 0; j < grid.GetLength(1); j++)
            {
                grid[i, j] = 0;
            }
        }
    }

    // Function to display the Minesweeper grid with colored numbers
    static void DisplayGrid(int[,] grid)
    {
        for (int i = 0; i < grid.GetLength(0); i++)
        {
            for (int j = 0; j < grid.GetLength(1); j++)
            {
                if (grid[i, j] == -1)
                {
                    Console.Write("X ");
                }
                else
                {
                    Console.Write(GetColoredNumber(grid[i, j]) + " ");
                }
            }
            Console.WriteLine();
        }
        Console.WriteLine();
    }

    // Function to get colored representation of numbers
    static string GetColoredNumber(int number)
    {
        string coloredNumber;

        switch (number)
        {
            case 0:
                coloredNumber = "\u001b[37m0\u001b[0m"; // White
                break;
            case 1:
                coloredNumber = "\u001b[34m1\u001b[0m"; // Blue
                break;
            case 2:
                coloredNumber = "\u001b[32m2\u001b[0m"; // Green
                break;
            case 3:
                coloredNumber = "\u001b[31m3\u001b[0m"; // Red
                break;
            case 4:
                coloredNumber = "\u001b[35m4\u001b[0m"; // Purple
                break;
            case 5:
                coloredNumber = "\u001b[36m5\u001b[0m"; // Cyan
                break;
            case 6:
                coloredNumber = "\u001b[33m6\u001b[0m"; // Yellow
                break;
            case 7:
                coloredNumber = "\u001b[37m7\u001b[0m"; // White
                break;
            case 8:
                coloredNumber = "\u001b[30m8\u001b[0m"; // Black
                break;
            default:
                coloredNumber = "\u001b[32m" + number + "\u001b[0m"; // Green for 9
                break;
        }

        return coloredNumber;
    }

    // Function to get user input for the height and length of the grid
    static int GetUserInput(string prompt)
    {
        Console.Write(prompt);
        return int.Parse(Console.ReadLine());
    }

    // Function to save the Minesweeper grid to a JSON file using System.Text.Json
    static void SaveGridToJson(int[,] grid, string fileName)
    {
        int[][] jaggedArray = ConvertToJaggedArray(grid);
        string json = JsonSerializer.Serialize(jaggedArray, new JsonSerializerOptions { WriteIndented = true });
        System.IO.File.WriteAllText(fileName, json);
        Console.WriteLine($"Grid saved to {fileName}");
    }

    // Function to convert a 2D array to a jagged array
    static int[][] ConvertToJaggedArray(int[,] array)
    {
        int rows = array.GetLength(0);
        int cols = array.GetLength(1);

        int[][] jaggedArray = new int[rows][];

        for (int i = 0; i < rows; i++)
        {
            jaggedArray[i] = new int[cols];
            for (int j = 0; j < cols; j++)
            {
                jaggedArray[i][j] = array[i, j];
            }
        }

        return jaggedArray;
    }
}
