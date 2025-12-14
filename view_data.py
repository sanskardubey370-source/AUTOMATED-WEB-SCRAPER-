import csv
from models import Session, Product

def export_to_csv(filename="scraped_data.csv"):
    session = Session()
    products = session.query(Product).all()
    
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write Header
        writer.writerow(["ID", "Name", "Price", "URL", "Timestamp"])
        
        # Write Rows
        for p in products:
            writer.writerow([p.id, p.name, p.price, p.source_url, p.timestamp])
            
    print(f"Exported {len(products)} records to {filename}")
    session.close()

if __name__ == "__main__":
    export_to_csv()