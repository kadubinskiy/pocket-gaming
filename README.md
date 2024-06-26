# Game Manager App

Welcome to the Game Manager App! This open-source command line-based game manager allows users to provide the manager with game files (currently supporting `.py` files) and corresponding configuration files. The manager detects the presence of these files, adds options to set the game up, and allows users to manipulate game metrics directly in the terminal. 

A significant part of this project is the collection of original games developed from scratch, including:

- **Snake:** A classic game where the player controls a snake to eat food and grow longer without running into itself.
- **Tic-Tac-Toe:** The traditional two-player game where players take turns marking spaces in a 3x3 grid to get three in a row.
- **Minesweeper:** A single-player puzzle game where the objective is to clear a rectangular board containing hidden "mines" without detonating any of them.
- **Pong:** One of the earliest arcade video games, simulating table tennis where the player controls paddles to hit the ball back and forth.

These games were built from scratch, utilizing only the `pynput` library for keyboard input.

## Features

- **Game Detection:** Automatically detects game and configuration files.
- **Metric Manipulation:** Allows users to read and modify predefined game metrics from the configuration file.
- **Game Launch:** Runs a bash script to launch the game and display its output.
- **Initial Games Included:** Comes with several built-in games like Snake, Tic-Tac-Toe, Minesweeper, and Pong.
- **Modding Capability:** Supports easy modding for other programmers to test their own games.
- **Future Plans:** Aiming to grow into a comprehensive library of open-source games with account options, game downloads from servers, and a GUI.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/gamemanager.git
    cd gamemanager
    ```

2. Ensure you have Python and Bash installed on your system.

3. Install required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. **Add Your Game:**
   - Place your game file (`.py` extension) and its configuration file in the designated directory.
   - The manager will detect these files and list the game as an option.

2. **Manipulate Metrics:**
   - The game manager reads the manipulatable metrics from the configuration file and displays them in a bullet-point format.
   - Modify the values as needed and save the changes.

3. **Launch the Game:**
   - Use the game manager to start the game, which will run a bash script to launch the `.py` file and display the game output.

## Future Plans

- **Expanded Game Library:** We plan to grow the library with more open-source games.
- **Accounts and Downloads:** Implement user accounts and options to download new games from servers.
- **GUI Development:** Develop a graphical user interface for a more user-friendly experience.

## Contact

For any questions or suggestions, feel free to open an issue or contact me at kirill.kadubinskiy@gmail.com. 

---