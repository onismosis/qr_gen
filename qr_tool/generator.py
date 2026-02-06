import qrcode
from PIL import Image

def generate_qr(data, icon_path=None, fill_color="black", back_color="white"):
    """
    Generates a QR code with an optional icon overlay.
    
    Args:
        data (str): The data to encode in the QR code.
        icon_path (str or file-like object): Path to the icon image or a file-like object.
        fill_color (str): Color of the QR code modules.
        back_color (str): Background color of the QR code.
        
    Returns:
        PIL.Image.Image: The generated QR code image.
    """
    # 1. Generate QR code
    # ERROR_CORRECT_H is critical for icon embedding (30% error correction)
    qr = qrcode.QRCode(
        version=None,  # Auto-size
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    # Convert to RGBA for transparency support
    qr_img = qr.make_image(fill_color=fill_color, back_color=back_color).convert("RGBA")

    # 2. Add Icon if provided
    if icon_path:
        try:
            icon = Image.open(icon_path).convert("RGBA")
            
            # Calculate icon size (approx 20% of QR width)
            qr_w, qr_h = qr_img.size
            factor = 4
            size_w = qr_w // factor
            size_h = qr_h // factor
            
            # Resize icon maintaining aspect ratio
            icon.thumbnail((size_w, size_h), Image.Resampling.LANCZOS)
            
            # Calculate position to center the icon
            icon_w, icon_h = icon.size
            pos = (
                (qr_w - icon_w) // 2,
                (qr_h - icon_h) // 2,
            )
            
            # Paste icon (using itself as mask for transparency)
            qr_img.paste(icon, pos, icon)
            
        except Exception as e:
            print(f"Error loading icon: {e}")
            # Return QR without icon if loading fails (or handle as needed)
            
    return qr_img
