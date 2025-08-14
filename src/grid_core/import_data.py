import pandas as pd
from grid_opt.db import get_engine, create_tables, get_session, GridState

def import_csv_to_db(csv_path):
    engine = get_engine()
    create_tables(engine)
    session = get_session(engine)
    df = pd.read_csv(csv_path)
    for _, row in df.iterrows():
        state = GridState(
            region=row['region'],
            demand=row['demand'],
            supply=row['supply'],
            timestamp=pd.to_datetime(row['timestamp'])
        )
        session.add(state)
    session.commit()
    session.close()

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python grid_ops/import_data.py ./gridstate.csv")
    else:
        import_csv_to_db(sys.argv[1])
        print("Import complete.")