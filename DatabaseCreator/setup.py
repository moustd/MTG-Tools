"""Script to set up and initialize the MTG card database."""

from database import create_tables

if __name__ == "__main__":
    print("Initializing MTG Card Database...")
    create_tables()
    print("Database setup complete!")