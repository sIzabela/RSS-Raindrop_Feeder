# RSS Raindrop Feeder

This script will allow you to upload your favorite RSS Feeds to Raindrop.io.

## Setup

-   Rename the `.env.example` file to `.env`:

    ```bash
    mv .env.example .env
    ```

-   Rename the `RSS_FEED_LIST.csv.example` file to `RSS_FEED_LIST.csv`:

    ```bash
    mv RSS_FEED_LIST.csv.example RSS_FEED_LIST.csv
    ```

    and add the addresses of your RSS Feeds to this file. Each on a separate line.

-   In the end replace the Xs on the `.env` file with your:
    -   [Raindrop TOKEN](https://developer.raindrop.io/v1/authentication/token).
    -   path to the downloaded RSS-Raindrop_Feeder package on your disk
    -   tags which will be automatically added to uploaded articles

## How to use it?

### Method 1: PowerShell

Standard, manual launch of the script

1. Run PowerShell (not CMD).
2. Download the python path on your computer using the following command:
    ```bash
    python -c "import sys; print(sys.executable)"
    ```
3. Use the following command, replacing C:/path/to/python.exe with the path of the Python interpreter downloaded in the previous step and C:/path/to/RSS-Raindrop_Feeder/main.py with the path to the script
    ```bash
    & "C:/path/to/python.exe" "C:/path/to/RSS-Raindrop_Feeder/main.py"
    ```

### Method 2: Task Scheduler (Windows)

Adding a task in the Task Scheduler according to the instructions below, will ensure that the script will run fairly regularly and automatically (after system startup and when idle), so that the indicated RSS Feeds will be added to Raindrop.io on a regular basis.

1. Open Task Scheduler:
    - Press `Win + R`, type `taskschd.msc`, and press `Enter`.
2. Create a Folder for Your Tasks:
    - In the left pane, right-click on `Task Scheduler Library`.
    - Select `New Folder...`.
    - Name the folder (e.g., `MyTasks`) and click OK.
3. Create a New Task:
    - In the left pane, navigate to the folder you just created (e.g., `MyTasks`).
    - In the right pane, click on `Create Task...`.
4. General Settings:
    - In the `General` tab, name the task (e.g., `RSS-Raindrop_Feeder`).
    - Check the box `Run with highest privileges`.
5. Triggers:
    - Go to the `Triggers` tab and click `New...`.
        - For the first trigger:
            - Set `Begin the task` to `At startup`.
            - Check `Delay task for` and set it to e.g., 1 minute.
            - Click `OK`.
        - For the second trigger:
            - Click `New...` again.
            - Set `Begin the task` to `On idle`.
            - Click `OK`.
6. Actions:
    - Go to the `Actions` tab and click `New...`.
        - Set `Action` to `Start a program`.
        - In the `Program/script` field, enter your `C:/path/to/python.exe`.
        - In the `Add arguments (optional)` field, enter your `C:/path/to/RSS-Raindrop_Feeder/main.py`.
        - Click `OK`.
7. Conditions:
    - Go to the `Conditions` tab.
        - Check `Start the task only if the computer is idle for` and set the desired time.
        - Check `Wait for idle for` and set the desired time (optional).
        - Click `OK`.
8. Finish:
    - Click `OK` to save and finish creating the task.

## Using AI

This project used Microsoft Copilot to generate some of the code.

## Licence

MIT
