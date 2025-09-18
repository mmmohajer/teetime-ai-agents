import scrapy
import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_BASE_URL = os.getenv("API_BASE_URL")

class TeetimeSpider(scrapy.Spider):
    name = "teetime"
    allowed_domains = ["teetimegolfpass.com"]
    start_urls = [
        "https://teetimegolfpass.com/",
        "https://teetimegolfpass.com/golf-pass/super-pass/",
        "https://teetimegolfpass.com/golf-pass/mid-atlantic/",
        "https://teetimegolfpass.com/golf-pass/midwest/",
        "https://teetimegolfpass.com/golf-pass/lower-midwest/",
        "https://teetimegolfpass.com/golf-pass/upper-midwest/",
        "https://teetimegolfpass.com/golf-pass/northeast/",
        "https://teetimegolfpass.com/about-us/",
        "https://teetimegolfpass.com/money-back-guarantee/",
        "https://teetimegolfpass.com/difference/",
        "https://teetimegolfpass.com/course-operators/",
        "https://teetimegolfpass.com/golf-gifts/",
        "https://teetimegolfpass.com/golf-pass/gift-card/",
        "https://teetimegolfpass.com/reviews/",
        "https://teetimegolfpass.com/golf-trips/",
        "https://teetimegolfpass.com/golf-deals-app/",
        "https://teetimegolfpass.com/golf-pass/",
        "https://help.teetimegolfpass.com/portal/en/home",
        "https://teetimegolfpass.com/contact-us/",
        "https://teetimegolfpass.com/privacy-policy/",
        "https://teetimegolfpass.com/terms-conditions/"
    ]

    def parse(self, response):
        try:
            body_text = " ".join(response.css("body :not(script):not(style)::text").getall()).strip()
            url = response.url
            if url:
                API_ENDPOINT = f"{API_BASE_URL}/api/knowledge-base/"
                headers = {"Content-Type": "application/json"}
                payload = {"description": body_text, "url": url}
                res = requests.post(API_ENDPOINT, json=payload, headers=headers)
                if res.status_code == 200:
                    print(f"✅ Successfully processed {url}")
                else:
                    print(f"❌ Failed to process {url}: {res.status_code} - {res.text}")
            else:
                print(f"❌ No URL found for response: {response}")
        except Exception as e:
            print(f"Request failed for {url}: {str(e)}")


