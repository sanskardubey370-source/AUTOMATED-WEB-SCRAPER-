from celery import Celery
from celery.schedules import crontab
from models import Session, Product, init_db
from scraper import get_dynamic_data

# Ensure DB is ready when worker starts
init_db()

# Initialize Celery
# Broker: Redis (default port 6379)
# Backend: Redis (to store task results if needed)
app = Celery('web_scraper', broker='redis://localhost:6379/0')

# --- CONFIGURATION ---
app.conf.beat_schedule = {
    'scrape-every-morning': {
        'task': 'tasks.run_scraper',
        # Schedule: Every day at 8:00 AM
        'schedule': crontab(hour=8, minute=0),
        # FOR TESTING: Uncomment line below to run every 30 seconds
        # 'schedule': 30.0, 
    },
}
app.conf.timezone = 'UTC'

@app.task
def run_scraper():
    """
    This is the task that Celery workers will execute.
    """
    session = Session()
    # Replace with the actual URL you want to scrape
    target_url = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
    
    print(f"Starting scrape for {target_url}...")
    
    data = get_dynamic_data(target_url)
    
    if data:
        # Save to SQLite
        try:
            new_entry = Product(
                name=data['name'], 
                price=data['price'], 
                source_url=data['url']
            )
            session.add(new_entry)
            session.commit()
            print(f"SUCCESS: Saved {data['name']} (${data['price']}) to DB.")
        except Exception as e:
            session.rollback()
            print(f"DATABASE ERROR: {e}")
        finally:
            session.close()
    else:
        print("FAILED: No data retrieved.")