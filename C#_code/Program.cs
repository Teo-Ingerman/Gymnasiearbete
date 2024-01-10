using System;
using System.Collections.Generic;
using System.IO;
using System.Text.Json;
using System.Linq;

class Minesweeper
{
    // Define a class to represent a move (opened square)
    class Move
    {
        public int Row { get; set; }
        public int Col { get; set; }

        public Move(int row, int col)
        {
            Row = row;
            Col = col;
        }
    }
    // Custom equality comparer for List<int>
    public class ListComparer : IEqualityComparer<List<int>?>
    {
        public bool Equals(List<int>? x, List<int>? y)
        {
            return x?.SequenceEqual(y ?? Enumerable.Empty<int>()) ?? (y == null);
        }

        public int GetHashCode(List<int>? obj)
        {
            if (obj == null)
            {
                return 0;
            }

            int hash = 17;
            foreach (int item in obj)
            {
                hash = hash * 31 + item.GetHashCode();
            }
            return hash;
        }
    }
    static void Main()
    {


        // // Get user input for the height and length of the Minesweeper grid
        // int rows = GetUserInput("Enter the height of the Minesweeper grid: ");
        // int cols = GetUserInput("Enter the length of the Minesweeper grid: ");

        // // Create the Minesweeper grid
        // int[,] minesweeper_grid = new int[rows, cols];

        // // Initialize the grid with empty cells
        // InitializeGrid(minesweeper_grid);

        // // Place mines in approximately 15% of the grid squares
        // PlaceMines(minesweeper_grid, 0.15);

        // // Calculate the numbers for each cell
        // CalculateNumbers(minesweeper_grid);

        // // Display the initial state of the Minesweeper grid
        // DisplayGrid(minesweeper_grid);

        // Save the Minesweeper grid to a JSON file
        // SaveGridsToJson(minesweeper_grid, "minesweeper_grid.json");

        // Load the Minesweeper grid from the JSON file
        List<int[,]> loadedGrids = LoadGridsFromJson("../generated_grids.json");

        // Display the loaded state of the Minesweeper grids
        Console.WriteLine("Loaded Minesweeper Grids:");
        foreach (var grid in loadedGrids)
        {
            DisplayGrid(grid);
        }

        // Solve and update each grid
        List<object[]> solvedGridsAndMoves = new List<object[]>();

        foreach (var grid in loadedGrids)
        {
            List<List<int>> moves = GridSolver(grid);

            // Create an array with the grid and its moves
            object[] gridAndMoves = new object[] { ConvertToJaggedArray(grid), moves };

            // Add the array to the list
            solvedGridsAndMoves.Add(gridAndMoves);

            // Update the grid (replace with your actual solver logic)
            int[,] solvedGrid = UpdateGrid(grid, moves);

            // solvedGrids.Add(solvedGrid);
        }

        // Save the updated grids and move sequences to a new JSON file
        SaveGridsAndMovesToJson(solvedGridsAndMoves, "../finished_grids.json");
    }

    // Function to remove duplicate positions from a list of moves
    static List<List<int>> RemoveDuplicatePositions(List<List<int>> moves)
    {
        return moves.Distinct(new ListComparer()).ToList();
    }

    // Function to save a list of Minesweeper grids and their move sequences to a JSON file using System.Text.Json
    static void SaveGridsAndMovesToJson(List<object[]> gridsAndMoves, string fileName)
    {
        string json = JsonSerializer.Serialize(gridsAndMoves, new JsonSerializerOptions { WriteIndented = true });
        File.WriteAllText(fileName, json);
        Console.WriteLine($"Grids and moves saved to {fileName}");
    }

    // Function to solve the Minesweeper grid and return a list of moves (row and col positions)
    static List<List<int>> GridSolver(int[,] grid)
    {
        List<List<int>> moves = new List<List<int>>();

        for (int i = 0; i < grid.GetLength(0); i++)
        {
            for (int j = 0; j < grid.GetLength(1); j++)
            {
                if (grid[i, j] != -1 && grid[i, j] != 9)
                {
                    // Add the position (row and col) to the list of moves
                    moves.Add(new List<int> { i, j });
                    
                    if (grid[i, j] == 0)
                    {
                        // If the square is empty, include surrounding squares in the moves list
                        List<List<int>> surroundingSquares = GetSurroundingSquares(grid, i, j)
                            .Select(tuple => new List<int> { tuple.Item1, tuple.Item2 })
                            .ToList();
                        moves.AddRange(surroundingSquares);
                        

                    }
                }



                
            }
        }


        List<List<int>> uniqueMoves = RemoveDuplicatePositions(moves);

        return uniqueMoves;


    }

    // Function to get the 8 surrounding squares of a given position on the grid
    static List<(int, int)> GetSurroundingSquares(int[,] grid, int row, int col)
    {
        List<(int, int)> surroundingSquares = new List<(int, int)>();

        for (int i = -1; i <= 1; i++)
        {
            for (int j = -1; j <= 1; j++)
            {
                int newRow = row + i;
                int newCol = col + j;

                // Ensure the surrounding square is within the grid bounds
                if (newRow >= 0 && newRow < grid.GetLength(0) &&
                    newCol >= 0 && newCol < grid.GetLength(1))
                {
                    // Exclude the center square itself
                    if (!(i == 0 && j == 0))
                    {
                        surroundingSquares.Add((newRow, newCol));
                    }
                }
            }
        }

        return surroundingSquares;
    }
    // Function to iteratively open adjacent safe squares and update the move sequence
    static void OpenAdjacentSquaresIterative(int[,] grid, List<List<int>> moves, int startRow, int startCol)
    {
        int rows = grid.GetLength(0);
        int cols = grid.GetLength(1);

        Queue<(int, int)> queue = new Queue<(int, int)>();
        queue.Enqueue((startRow, startCol));

        while (queue.Count > 0)
        {
            var (row, col) = queue.Dequeue();

            for (int i = -1; i <= 1; i++)
            {
                for (int j = -1; j <= 1; j++)
                {
                    int newRow = row + i;
                    int newCol = col + j;

                    if (newRow >= 0 && newRow < rows && newCol >= 0 && newCol < cols &&
                        grid[newRow, newCol] != -1 && grid[newRow, newCol] != 9)
                    {
                        // Add the position (row and col) to the list of moves
                        moves.Add(new List<int> { newRow, newCol });

                        if (grid[newRow, newCol] == 0)
                        {
                            // If the square is empty, enqueue it for further exploration
                            queue.Enqueue((newRow, newCol));

                            // Mark the square as opened
                            grid[newRow, newCol] = 9;
                        }
                        else
                        {
                            // Mark the square as opened
                            grid[newRow, newCol] = 9;
                        }
                    }
                }
            }
        }
    }



     // Function to update the Minesweeper grid based on the list of moves
    static int[,] UpdateGrid(int[,] grid, List<List<int>> moves)
    {
        // Implement your update logic here
        // For demonstration purposes, this function doesn't modify the grid
        return grid;
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
    return int.Parse(Console.ReadLine()!);
}

    // Function to save a list of Minesweeper grids to a JSON file using System.Text.Json
    // Function to save a list of Minesweeper grids to a JSON file using System.Text.Json
    static void SaveGridsToJson(List<int[,]> grids, string fileName)
    {
        List<int[][]> listOfJaggedArrays = new List<int[][]>();

        foreach (var grid in grids)
        {
            int[][] jaggedArray = ConvertToJaggedArray(grid);
            listOfJaggedArrays.Add(jaggedArray);
        }

        string json = JsonSerializer.Serialize(listOfJaggedArrays, new JsonSerializerOptions { WriteIndented = true });
        File.WriteAllText(fileName, json);
        Console.WriteLine($"Grids saved to {fileName}");
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

    // Function to load Minesweeper grids from a JSON file using System.Text.Json
    static List<int[,]> LoadGridsFromJson(string fileName)
    {
        if (File.Exists(fileName))
        {
            string json = File.ReadAllText(fileName);
            List<int[][]> listOfJaggedArrays = JsonSerializer.Deserialize<List<int[][]>>(json)!;

            List<int[,]> listOfGrids = new List<int[,]>();

            foreach (var jaggedArray in listOfJaggedArrays!)
            {
                int rows = jaggedArray.Length;
                int cols = jaggedArray[0].Length;

                int[,] grid = new int[rows, cols];

                for (int i = 0; i < rows; i++)
                {
                    for (int j = 0; j < cols; j++)
                    {
                        grid[i, j] = jaggedArray[i][j];
                    }
                }

                listOfGrids.Add(grid);
            }

            Console.WriteLine($"Grids loaded from {fileName}");
            return listOfGrids;
        }
        else
        {
            Console.WriteLine($"File '{fileName}' not found. Creating an empty list.");
            return new List<int[,]>();
        }
    }
}
