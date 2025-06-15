# FPL Data Project

This project fetches Fantasy Premier League (FPL) data from the Fantasy Nutmeg API and stores it in a PostgreSQL database. The data can be stored either in a local PostgreSQL database or in Supabase.

## Features

- Fetches FPL data from Fantasy Nutmeg API
- Stores data in PostgreSQL database
- Supports both local PostgreSQL and Supabase connections
- Creates and manages three main tables:
  - `player_matrix`: Player performance data
  - `team_history`: Team historical data
  - `player`: Player information

## Prerequisites

- Python 3.7+
- PostgreSQL (for local database)
- Supabase account (optional, for cloud database)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Configure the database connection settings

## Configuration

### Local PostgreSQL Setup
Set the following in your `.env` file:
```
CONNECT_SUPABASE=false
DB_USER=your_local_user
DB_PASSWORD=your_local_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=fpl_data
```

### Supabase Setup
Set the following in your `.env` file:
```
CONNECT_SUPABASE=true
DIRECT_URL=your_supabase_direct_url
```

## Usage

1. Create database tables:
```bash
python create_tables.py
```

2. Test database connection:
```bash
python test_connection.py
```

3. Populate data:
```bash
python populate_fpl_data.py
```

## Project Structure

- `create_tables.py`: Creates database tables
- `populate_fpl_data.py`: Fetches and populates data
- `test_connection.py`: Tests database connection
- `requirements.txt`: Project dependencies
- `.env`: Environment variables (not tracked in git)
- `.env.example`: Example environment variables

## Database Schema

### Player Matrix Table
- Primary key: `id`
- Contains player performance data
- Links to player and team history

### Team History Table
- Primary key: `id`
- Contains team historical data
- Links to player matrix

### Player Table
- Primary key: `id`
- Contains player information
- Links to player matrix
