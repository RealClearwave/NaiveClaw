import mss
from PIL import Image
import base64
import io

def capture_screen_base64() -> str:
    """
    Captures the primary monitor screen, converts it to a JPEG,
    and returns its base64 string representation.
    """
    with mss.mss() as sct:
        monitor = sct.monitors[1]  # primary monitor
        sct_img = sct.grab(monitor)
        
        # Convert to PIL Image
        img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
        
        # Optionally resize or overlay grid here if needed for localization
        
        # Save to memory buffer
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG", quality=70) # Compress to save tokens
        img_bytes = buffer.getvalue()
        
        return base64.b64encode(img_bytes).decode('utf-8')
