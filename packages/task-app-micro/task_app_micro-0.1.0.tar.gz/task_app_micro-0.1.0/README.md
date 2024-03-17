# Task-App-Micro

# Usage

```python
from task_app_micro import TaskApp
ta = TaskApp()
```

# Features

# TODO

-   Add tasks
    -   Name
    -   Description
    -   Time - start+end
    -   Date - start+end
    -   Frequency
        -   Periodicity
        -   Discrete
-   Update tasks
-   Visualise
    -   Table
    -   Look ahead
        -   To date
        -   Set period
            -   Weekly
            -   Monthly
    -   Timeline
-   Delete
-   Complete Tasks
-   Fail Tasks
    -   Re-create new Task? How to inform the application
-   Output
    -   HTML Table
    -   JSON
    -   Pickle
    -   Open Standards?
    -   Common apps?

# Backup and Restore

# Build

```bash
python -m build
python -m twine upload dist/*
```
