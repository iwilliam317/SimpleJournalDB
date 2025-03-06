# Database Journal Demo

A simple demonstration of database journaling/transaction logging mechanism using Python. This project simulates a basic database system that maintains a transaction log for recovery purposes.

## Overview

Transaction logging (journaling) is a mechanism that:
- Records all changes before they are made to the database
- Enables recovery from crashes or corruptions
- Provides an audit trail of operations

## What This Project Does

1. Simulates a simple JSON-based database storing user data
2. Maintains a transaction log of all operations
3. Demonstrates database corruption scenario
4. Shows how to recover the database using transaction logs

## Project Structure
```
SimpleJournalDB/
│
├── simple_journal_db.py      # Main implementation
├── database.json            # Generated when running
├── transactions.log         # Generated when running
├── .gitignore
└── README.md
```
    

## How to Run
```bash
# Run the demo
python simple_journal_db.py
```

# Test recovery (delete database and run again)
```
rm database.json
python simple_journal_db.py
```