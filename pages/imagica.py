import streamlit as st
import cv2
import numpy as np
import zipfile
import io

# Page setup
st.set_page_config(page_title="Imagica", layout="wide")

# Hide Streamlit default styling
hide_st_style = """
<style>
#MainMenu, footer, header {visibility: hidden;}
</style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

# Sidebar for file upload
st.sidebar.title("📂 Upload Your Data")
uploaded_file = st.sidebar.file_uploader("Upload image here", type=['jpg', 'jpeg', 'png'])

# Dictionary to store processed images
transformed_images = {}

if uploaded_file is None:
    st.warning("Please upload an image to begin...")
else:
    img_array = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img_bgr = cv2.imdecode(img_array, 1)

    if img_bgr is None:
        st.error("❌ Unsupported or corrupted image format.")
    else:
        width = 600
        height = int(img_bgr.shape[0] * (600 / img_bgr.shape[1]))  # Maintain aspect ratio
        img_resized = cv2.resize(img_bgr, (width, height))
        st.subheader("🖼️ Original Image Preview (Full Resolution)")
        st.image(cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB), caption="Original Image", use_container_width=False)  # Full resolution
        st.markdown("----")

        # Format options
        format_options = [
            "Grayscale", "Rotate", "Flip Horizontally",
            "Flip Vertically", "Shearing", "Translation", "Cropping"
        ]
        selected_formats = st.sidebar.multiselect("Choose transformations", format_options, default=[])

        st.subheader("🔄 Transformed Outputs")

        for i in range(0, len(selected_formats), 2):
            col_pair = st.columns(2)
            for j in range(2):
                if i + j < len(selected_formats):
                    fmt = selected_formats[i + j]
                    result = None
                    with col_pair[j]:
                        st.markdown(f"**{fmt}**")

                        if fmt == 'Grayscale':
                            result = cv2.cvtColor(img_resized, cv2.COLOR_BGR2GRAY)
                            st.image(result, use_container_width=True, clamp=True)

                        elif fmt == "Rotate":
                            rotation_option = st.sidebar.selectbox(
                                "Select Rotation",
                                ["No Rotation", "90° Clockwise", "180°", "90° Counter-Clockwise"],
                                key="rotate"
                            )
                            rot_map = {
                                "90° Clockwise": cv2.ROTATE_90_CLOCKWISE,
                                "180°": cv2.ROTATE_180,
                                "90° Counter-Clockwise": cv2.ROTATE_90_COUNTERCLOCKWISE
                            }
                            if rotation_option != "No Rotation":
                                img_rgb = cv2.cvtColor(img_resized, cv2.COLOR_BGR2RGB)
                                result = cv2.rotate(img_rgb,rot_map[rotation_option])  
                                st.image(result,use_container_width=True,clamp=True)
                                
                            else:
                                result = cv2.cvtColor(img_resized, cv2.COLOR_BGR2RGB)
                                st.image(result,use_container_width=True,clamp=True)

                        elif fmt == "Flip Horizontally":
                            flip_img = cv2.flip(img_resized,1)
                            result=cv2.cvtColor(flip_img,cv2.COLOR_BGR2RGB)
                            st.image(result,use_container_width=True,clamp=True)
                        

                        elif fmt == "Flip Vertically":
                            flip_img = cv2.flip(img_resized,0)
                            result=cv2.cvtColor(flip_img,cv2.COLOR_BGR2RGB)
                            st.image(result,use_container_width=True,clamp=True)
                        

                        elif fmt == 'Shearing':
                            shear = st.sidebar.slider("Shear Factor", 0.0, 1.0, 0.2, step=0.05)
                            rows, cols = img_resized.shape[:2]
                            shear_matrix = np.float32([[1, shear, 0], [0, 1, 0]])
                            new_width = int(cols + shear * rows)

                            shear_img = cv2.warpAffine(img_resized, shear_matrix, (new_width, rows))

                            # Convert and display
                            result = cv2.cvtColor(shear_img, cv2.COLOR_BGR2RGB)
                            st.image(result, caption=f"Sheared Image (factor: {shear})", use_container_width=True, clamp=True)



                        elif fmt == "Translation":
                            rows, cols = img_resized.shape[:2]
                            col1, col2 = st.sidebar.columns(2)
                            with col1:
                                x_shift = st.number_input("X-shift", -cols, cols, 0, key="tx")
                            with col2:
                                y_shift = st.number_input("Y-shift", -rows, rows, 0, key="ty")
                            m = np.float32([[1, 0, x_shift], [0, 1, y_shift]])


                            tras_img=cv2.warpAffine(img_resized,m,(cols,rows))
                            result=cv2.cvtColor(tras_img,cv2.COLOR_BGR2RGB)
                            st.image(result,use_container_width=True,clamp=True)
            

                        elif fmt == "Cropping":
                            rows, cols = img_resized.shape[:2]
                            st.sidebar.markdown("### 📐 Crop Parameters")
                            x_start = st.sidebar.slider("x_start", 0, cols - 1, 0)
                            x_end = st.sidebar.slider("x_end", x_start + 1, cols, cols)
                            y_start = st.sidebar.slider("y_start", 0, rows - 1, 0)
                            y_end = st.sidebar.slider("y_end", y_start + 1, rows, rows)
                            crop_img = img_resized[y_start:y_end,x_start:x_end]
                            result=cv2.cvtColor(crop_img,cv2.COLOR_BGR2RGB)
                            st.image(result,use_container_width=True,clamp=True)

                        # Save to dictionary in RGB format
                        if result is not None:
                            # Convert to RGB if needed
                            if len(result.shape) == 2:
                                rgb_img = cv2.cvtColor(result, cv2.COLOR_GRAY2RGB)
                            else:
                                rgb_img = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)

                            success, buffer = cv2.imencode('.jpg', rgb_img)
                            if success:
                                transformed_images[f"{fmt.lower().replace(' ', '_')}.jpg"] = buffer.tobytes()

        # ZIP download
        if transformed_images:
            st.markdown("### 📦 Download All Transformed Images")
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED) as zf:
                for filename, image_bytes in transformed_images.items():
                    zf.writestr(filename, image_bytes)
            zip_buffer.seek(0)
            st.download_button(
                label="📥 Download ZIP",
                data=zip_buffer,
                file_name="transformed_images.zip",
                mime="application/zip"
            )
