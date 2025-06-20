import re
from typing import Optional

class PriceExtractor:
    def __init__(self):
        self.price_patterns = [
            r'\$?(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',  # $1,234.56 or 1234.56
            r'(\d+\.\d{2})',  # 12.34
            r'(\d+)',  # 123
        ]
    
    def extract_price(self, text: str) -> float:
        """Extract price from text"""
        if not text:
            return 0.0
        
        # Clean the text
        cleaned_text = text.replace(',', '').replace('$', '').strip()
        
        for pattern in self.price_patterns:
            match = re.search(pattern, cleaned_text)
            if match:
                try:
                    return float(match.group(1))
                except ValueError:
                    continue
        
        return 0.0
    
    def extract_threshold(self, goal: str) -> float:
        """Extract monetary threshold from goal text"""
        patterns = [
            r'\$(\d+(?:\.\d{2})?)',
            r'(\d+(?:\.\d{2})?) dollars?',
            r'(\d+(?:\.\d{2})?) USD'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, goal, re.IGNORECASE)
            if match:
                return float(match.group(1))
        
        return 100.0  # Default threshold