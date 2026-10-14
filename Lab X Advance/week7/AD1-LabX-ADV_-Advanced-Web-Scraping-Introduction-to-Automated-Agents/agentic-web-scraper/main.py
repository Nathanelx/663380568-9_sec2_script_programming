# agentic-web-scraper/main.py
import os
from src.config_parser import ConfigParser
from src.scraper_agent import ScraperAgent
from src.utils import save_data_to_json, save_data_to_csv


def main():
    config_path = os.path.join("configs", "example_site_config.json")
    json_output = os.path.join("data", "scraped_products.json")
    csv_output = os.path.join("data", "scraped_products.csv")

    # 1. Load and parse config
    parser = ConfigParser(config_path)
    config = parser.load_config()

    # 2. Initialize and run scraper agent
    # ปรับ headless=False หากต้องการเปิดเบราว์เซอร์ดูการทำงานจริง
    agent = ScraperAgent(config=config, browser="chrome", headless=True)
    results = agent.run()

    # 3. Save results
    save_data_to_json(results, json_output)
    save_data_to_csv(results, csv_output)
    print(f"Successfully scraped {len(results)} items and saved to {json_output} and {csv_output}")


if __name__ == "__main__":
    main()
