# Afloat and Alive : Might be a fancy task manager for all I know.

## Base features:

    1. Activity Tracker 
    2. Task Tracker
    3. Resource Tracker
    4. Mood and Health Tracker

### Activity Tracker sub features:

    1. Mental Health activities.
        - eg: sunlight everyday, walks, 2 to 3 meals a day or controlling eating
    2. Daily essentials activities:
        - work or study or etc
    3. Weekly:
        - Wash your sheets etc
    4. Monthly:
        - pay bills etc
    5. Custom tasks that repeat.

#### SQL:
    CREATE TABLE activities(
        id INT,
        timestamp TIME,
        category ENUM IN ('mental_health', 'daily_essentials', 'weekly_activities', 'monthly', 'custom');
        description TEXT,
        impact ENUM IN ('negative' , 'positive')
    );
        
### Task Tracker:

    1. Special out of loop tasks
    2. Custom one occurence tasks

#### SQL:
    CREATE TABLE task(
        id INT,
        timestamp,
        desc,
        deadline
    )

### Resource Tracker:

    1. Money
    2. Groceries
    3. Misc.

### Mood and Health:

    1. Through chats
        - keep track of words, time and patterns