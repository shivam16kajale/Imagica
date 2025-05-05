import streamlit as st

# Set page config
st.set_page_config(page_title="Imagica - Image Transformation Tool", layout="wide")

# Hide Streamlit default styling
hide_st_style = """
<style>
#MainMenu, footer, header {visibility: hidden;}
</style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

# Extra UI cleanup
st.markdown("""
    <style>
    .css-1jc7ptx, .e1ewe7hr3, .viewerBadge_container__1QSob,
    .styles_viewerBadge__1yB5_, .viewerBadge_link__1S137,
    .viewerBadge_text__1JaDK {
        display: none;
    }
    </style>
""", unsafe_allow_html=True)

# Page header
st.markdown("<h1 style='text-align: center;'>Imagica - Image Transformation Tool</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: gray;'>Transform and Visualize Your Images</h3>", unsafe_allow_html=True)
st.markdown("---")

# Introduction part
st.markdown("""
### 🎯 **Project Overview**

Welcome to **Imagica**, an image transformation tool that allows you to manipulate images with ease! This application provides several common image processing techniques that you can apply to any image.

---

### 🚀 **Objectives**

- Allow users to upload images and instantly preview them.
- Provide a variety of transformations, including:
  - Grayscale conversion
  - Rotation (90°, 180°)
  - Flip (horizontal and vertical)
  - Shearing, translation, and cropping
- Enable easy download of transformed images as a **ZIP file** for batch processing.

---

### ⚙️ **Key Features**

1. **Image Upload**: Users can upload images in various formats (JPG, PNG, etc.).
2. **Multiple Transformations**: Apply several transformations like:
   - **Grayscale**: Convert the image to grayscale for better visual analysis.
   - **Rotate**: Rotate the image 90° clockwise, 180°, or counterclockwise.
   - **Flip**: Flip the image horizontally or vertically.
   - **Shearing and Translation**: Apply transformations to adjust the position and angle of the image.
   - **Cropping**: Crop the image by selecting a specific area.
3. **Real-time Preview**: See the results of transformations immediately.
4. **Download Transformed Images**: After applying transformations, download all images as a **ZIP file** for batch processing.

---

### 🧑‍💻 **How to Get Started**
1. **Upload an image**: Click on the sidebar and upload your image.
2. **Select transformations**: Choose the transformations you want to apply (e.g., Grayscale, Rotate).
3. **Apply changes**: Preview and view the results instantly.
4. **Download the results**: Once happy with the transformations, download the modified images in a ZIP file.

---

### 📚 **Technologies Used**
- **Streamlit**: For the interactive user interface.
- **OpenCV**: For image transformation techniques.
- **NumPy**: For efficient numerical computations in image processing.
- **ZipFile**: For packaging and downloading the images.

---

### 🎨 **Author**
This project was created by **Shivam Kajale**.  
You can connect with me on [LinkedIn](https://www.linkedin.com/in/shivamkajale/).  
Feel free to reach out for collaboration or any questions related to this project.

---
""")

