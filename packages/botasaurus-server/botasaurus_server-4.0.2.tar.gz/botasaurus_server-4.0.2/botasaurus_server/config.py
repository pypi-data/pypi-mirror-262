from .utils.create_config import create_config
from .header_title import header_title

config = create_config(
    title="Google Maps Scraper",
    header_title=header_title(),
    description="Find thousands of new customers personal phone, email and grow your business exponentially.",
    right_header={
        "text": "Love It? Star It! ★",
        "link": "https://github.com/omkarcloud/google-maps-scraper",
    },
)
