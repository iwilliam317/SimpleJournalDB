import json
import time
from pathlib import Path
from datetime import datetime

class SimpleDB:
    def __init__(self, db_file="database.json", log_file="transactions.log"):
        self.db_file = Path(db_file)
        self.log_file = Path(log_file)
        
        # Initialize database if it doesn't exist
        if not self.db_file.exists():
            self._write_db({'users': {}})
            
    def _write_db(self, data):
        """Write data to database file"""
        with open(self.db_file, 'w') as f:
            json.dump(data, f, indent=2)
            
    def _read_db(self):
        """Read data from database file"""
        with open(self.db_file, 'r') as f:
            return json.load(f)
            
    def _log_transaction(self, operation, data):
        """Log a transaction before executing it"""
        transaction = {
            'timestamp': datetime.now().isoformat(),
            'operation': operation,
            'data': data
        }
        with open(self.log_file, 'a') as f:
            json.dump(transaction, f)
            f.write('\n')

    def add_user(self, user_id, name, email):
        """Add a new user to the database"""
        # First log the transaction
        self._log_transaction('ADD_USER', {
            'user_id': user_id,
            'name': name,
            'email': email
        })
        
        # Then perform the operation
        db_data = self._read_db()
        db_data['users'][user_id] = {
            'name': name,
            'email': email
        }
        self._write_db(db_data)

    def recover_from_logs(self):
        """Recover database by replaying transaction logs"""
        print("Starting recovery...")
        
        # Reset database to initial state
        self._write_db({'users': {}})
        
        # Replay all transactions from log
        with open(self.log_file, 'r') as f:
            for line in f:
                transaction = json.loads(line)
                print(f"Replaying: {transaction['operation']}")
                
                if transaction['operation'] == 'ADD_USER':
                    data = transaction['data']
                    db_data = self._read_db()
                    db_data['users'][data['user_id']] = {
                        'name': data['name'],
                        'email': data['email']
                    }
                    self._write_db(db_data)

        print("Recovery complete!")

def corrupt_database():
    """Simulate database corruption"""
    with open('database.json', 'w') as f:
        f.write('{"users": CORRUPTED_DATA}')
    print("Database corrupted!")

def main():
    # Initialize database
    db = SimpleDB()
    
    print("\n1. Adding users (each operation will be logged)...")
    db.add_user("1", "John Doe", "john@example.com")
    db.add_user("2", "Jane Smith", "jane@example.com")
    
    print("\n2. Current database state:")
    print(json.dumps(db._read_db(), indent=2))
    
    print("\n3. Transaction log contents:")
    with open('transactions.log', 'r') as f:
        print(f.read())
    
    print("\n4. Simulating database corruption...")
    corrupt_database()
    
    print("\n5. Trying to read corrupted database...")
    try:
        db._read_db()
    except json.JSONDecodeError:
        print("Database is corrupted!")
    
    print("\n6. Recovering from transaction logs...")
    db.recover_from_logs()
    
    print("\n7. Recovered database state:")
    print(json.dumps(db._read_db(), indent=2))

if __name__ == "__main__":
    main()
