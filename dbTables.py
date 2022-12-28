# This variable holds the Person table
personTable = """
CREATE TABLE IF NOT EXISTS 
  Person (
  pID          INTEGER PRIMARY KEY AUTOINCREMENT,
  pFirstName   TEXT    NOT NULL,
  pLastName    TEXT    NOT NULL,
  pBodyType    TEXT    NOT NULL,
  pWeight      TEXT    NOT NULL
  );
"""

# This variable holds the Exercise table
exerciseTable = """
CREATE TABLE IF NOT EXISTS
  ExerciseTable (
  exID         INTEGER PRIMARY KEY AUTOINCREMENT,
  exName       TEXT    NOT NULL,
  muscleGroup  TEXT    NOT NULL,
  overallInten INTEGER NOT NULL,
  exType       TEXT    NOT NULL,
);
"""


# This variable holds the Workout Data table
workoutData = """
CREATE TABLE IF NOT EXISTS
  WorkoutDataTable (
  dateID       DATE    PRIMARY KEY AUTOINCREMENT,
  pID          INTEGER PRIMARY KEY,
  exName       TEXT NOT NULL,
  repCount     INTEGER NOT NULL,
  timeBtwnReps INTEGER,
  overallInten INTEGER NOT NULL,
    
  CONSTRAINT  
  FOREIGN KEY (pID)
  REFERENCES Person (pID),
  
  CONSTRAINT  
  FOREIGN KEY (mID)
  REFERENCES Morning (mID)
);
"""


# This variable holds the Workout Data table
workoutFeedBack = """
CREATE TABLE IF NOT EXISTS
  WorkoutFeedbackTable (
  dateID       DATE    PRIMARY KEY AUTOINCREMENT,
  pID          INTEGER PRIMARY KEY,
  exName       TEXT    NOT NULL,
  predInten    INTEGER NOT NULL,
  actualInten  INTEGER NOT NULL,
  raing        INTEGER NOT NULL,
    
  CONSTRAINT  
  FOREIGN KEY (pID)
  REFERENCES Person (pID)
);
"""

dataBase = [
    personTable,
    exerciseTable,
    workoutData,
    workoutFeedBack
]
