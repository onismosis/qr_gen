import streamlit as st
import os
from generator import generate_qr
from PIL import Image
import io

# Page Config
st.set_page_config(
    page_title="QR Code Generator",
    page_icon="🧊",
    layout="centered"
)

st.title("🧊 QR Generator")
st.markdown("Generate custom QR codes with high error correction and embedded logos.")

# Sidebar Controls
with st.sidebar:
    st.header("Settings")
    
    # 1. Data Input
    qr_data = st.text_input("QR Content (URL or Text)", "https://example.com")
    
    # 2. Colors
    col1, col2 = st.columns(2)
    with col1:
        fill_color = st.color_picker("Fill Color", "#000000")
    with col2:
        back_color = st.color_picker("Background", "#FFFFFF")
        
    # 3. Icon Selection
    st.subheader("Icon Overlay")
    
    uploaded_icon = st.file_uploader("Upload Custom Icon (PNG/JPG)", type=["png", "jpg", "jpeg"])

# Logic to determine which icon to use
icon_source = None
if uploaded_icon:
    icon_source = uploaded_icon

# Generate Button & Preview
if qr_data:
    try:
        # Generate the QR Code
        img = generate_qr(
            data=qr_data,
            icon_path=icon_source,
            fill_color=fill_color,
            back_color=back_color
        )
        
        # Convert to bytes for download
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        byte_im = buf.getvalue()

        # Display
        st.image(img, caption="Generated QR Code", width=350)
        
        # Download Button
        st.download_button(
            label="Download QR Code",
            data=byte_im,
            file_name="custom_qr.png",
            mime="image/png",
        )
        
    except Exception as e:
        st.error(f"Error generating QR code: {e}")
else:
    st.warning("Please enter text or a URL to generate a QR code.")
