import csv, sqlite3, random
from pathlib import Path
BASE = Path(__file__).parent
SQL = """SELECT vendor, COUNT(*) AS shipments,
ROUND(100.0 * AVG(CASE WHEN actual_days <= promised_days THEN 1 ELSE 0 END),2) AS on_time_pct,
ROUND(AVG(cost),2) AS avg_cost FROM shipments GROUP BY vendor ORDER BY on_time_pct DESC"""
def generate():
    rng=random.Random(42)
    with (BASE/'shipments.csv').open('w',newline='') as f:
        w=csv.writer(f); w.writerow(['shipment_id','vendor','promised_days','actual_days','cost'])
        for i in range(1,301):
            vendor=rng.choice(['Atlas','Harbor','Summit']); promised=rng.randint(2,7)
            w.writerow([i,vendor,promised,max(1,promised+rng.randint(-2,4)),rng.randint(150,1450)])
def analyze():
    if not (BASE/'shipments.csv').exists(): generate()
    with sqlite3.connect(':memory:') as db:
        db.execute('CREATE TABLE shipments(id INTEGER PRIMARY KEY, vendor TEXT, promised_days INTEGER, actual_days INTEGER, cost REAL)')
        with (BASE/'shipments.csv').open() as f:
            db.executemany('INSERT INTO shipments VALUES(?,?,?,?,?)', list(csv.reader(f))[1:])
        rows = db.execute(SQL).fetchall()
    with (BASE/'vendor_report.csv').open('w', newline='') as f:
        w=csv.writer(f); w.writerow(['vendor','shipments','on_time_pct','avg_cost']); w.writerows(rows)
    return rows
if __name__ == '__main__':
    for row in analyze(): print(*row, sep=' | ')
