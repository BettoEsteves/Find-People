"""
FaceAge Identity Analyzer - Main Streamlit Application

This application performs face aging simulation and identity verification.
"""
import streamlit as st
import cv2
import numpy as np
from pathlib import Path
from datetime import date
import sys
from loguru import logger

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from config.settings import settings
from src.core import (
    FaceDetector,
    FaceAligner,
    FaceAging,
    FaceEmbeddings,
    FaceComparator
)
from src.utils import ImageUtils, DateUtils, Visualization

# Configure logging
logger.remove()
logger.add(
    settings.get_path('logs') / "app.log",
    rotation="10 MB",
    retention="30 days",
    level=settings.get('logging.level', 'INFO')
)
logger.add(sys.stderr, level="INFO")


# Page configuration
st.set_page_config(
    page_title="FaceAge Identity Analyzer",
    page_icon="👤",
    layout="wide",
    initial_sidebar_state="expanded"
)


def initialize_models():
    """Initialize all models with caching."""
    if 'models_initialized' not in st.session_state:
        with st.spinner("Initializing AI models... This may take a moment."):
            try:
                # Initialize models
                st.session_state.face_detector = FaceDetector(
                    backend=settings.get('models.face_detection.backend', 'opencv'),
                    confidence_threshold=settings.get('models.face_detection.confidence_threshold', 0.9)
                )

                st.session_state.face_aligner = FaceAligner(
                    target_size=tuple(settings.get('models.face_alignment.target_size', [256, 256]))
                )

                st.session_state.face_aging = FaceAging(
                    method=settings.get('models.face_aging.method', 'style_transfer')
                )

                # Initialize embeddings (might take longer)
                try:
                    st.session_state.face_embeddings = FaceEmbeddings(
                        backend=settings.get('models.face_recognition.backend', 'insightface'),
                        model_name=settings.get('models.face_recognition.model_name', 'buffalo_l'),
                        device='cuda' if settings.enable_gpu else 'cpu'
                    )
                except Exception as e:
                    logger.warning(f"Failed to initialize InsightFace, trying FaceNet: {e}")
                    st.session_state.face_embeddings = FaceEmbeddings(
                        backend='facenet',
                        device='cpu'
                    )

                st.session_state.face_comparator = FaceComparator(
                    similarity_threshold=settings.get('models.face_recognition.similarity_threshold', 0.4)
                )

                st.session_state.models_initialized = True
                logger.info("All models initialized successfully")

            except Exception as e:
                st.error(f"Failed to initialize models: {e}")
                logger.error(f"Model initialization error: {e}")
                st.stop()


def display_disclaimer():
    """Display ethics and usage disclaimer."""
    if settings.get('ethics.display_disclaimer', True):
        with st.expander("⚠️ IMPORTANT DISCLAIMER - Please Read", expanded=False):
            st.warning(settings.disclaimer_text)


def main():
    """Main application."""
    # Title and header
    st.title("👤 FaceAge Identity Analyzer")
    st.markdown("### Face Aging Simulation & Identity Verification")

    # Display disclaimer
    display_disclaimer()

    # Initialize models
    initialize_models()

    # Sidebar for inputs
    st.sidebar.header("📋 Input Information")

    # File upload
    uploaded_file = st.sidebar.file_uploader(
        "Upload Person's Photo",
        type=settings.get('ui.supported_formats', ['jpg', 'jpeg', 'png']),
        help="Upload a clear frontal face photo"
    )

    # Personal information
    st.sidebar.subheader("Personal Information")
    person_name = st.sidebar.text_input("Name", placeholder="Enter person's name")

    birth_date = st.sidebar.date_input(
        "Date of Birth",
        value=date(1990, 1, 1),
        min_value=date(1900, 1, 1),
        max_value=date.today()
    )

    age_in_photo = st.sidebar.number_input(
        "Approximate Age in Photo",
        min_value=0,
        max_value=120,
        value=25,
        help="Estimated age when photo was taken"
    )

    # Process button
    process_button = st.sidebar.button("🚀 Analyze", type="primary", use_container_width=True)

    # Main content area
    if uploaded_file is None:
        st.info("👆 Please upload a photo to begin analysis")

        # Show example/instructions
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("#### 1️⃣ Upload Photo")
            st.write("Upload a clear frontal face photo")

        with col2:
            st.markdown("#### 2️⃣ Enter Details")
            st.write("Provide name, birth date, and age in photo")

        with col3:
            st.markdown("#### 3️⃣ Analyze")
            st.write("Click Analyze to simulate aging and compare")

    elif process_button:
        # Validate inputs
        if not person_name:
            st.error("Please enter the person's name")
            return

        # Validate birth date
        is_valid, error_msg = DateUtils.validate_birth_date(birth_date)
        if not is_valid:
            st.error(f"Invalid birth date: {error_msg}")
            return

        # Save uploaded file
        upload_path = settings.get_path('uploads') / uploaded_file.name
        with open(upload_path, 'wb') as f:
            f.write(uploaded_file.getbuffer())

        # Load image
        image = ImageUtils.load_image(str(upload_path))
        if image is None:
            st.error("Failed to load image")
            return

        # Progress tracking
        progress_bar = st.progress(0)
        status_text = st.empty()

        try:
            # Step 1: Face Detection
            status_text.text("🔍 Detecting face...")
            progress_bar.progress(10)

            detections = st.session_state.face_detector.detect(image)
            if not detections:
                st.error("No face detected in the image. Please upload a clear frontal face photo.")
                return

            largest_face = st.session_state.face_detector.get_largest_face(detections)
            bbox = largest_face['bbox']
            landmarks = largest_face.get('landmarks', {})

            # Crop face
            face_cropped = st.session_state.face_detector.crop_face(
                image,
                bbox,
                padding=settings.get('models.face_alignment.padding', 0.3)
            )

            progress_bar.progress(20)

            # Step 2: Face Alignment
            status_text.text("📐 Aligning face...")

            if landmarks:
                face_aligned = st.session_state.face_aligner.align(face_cropped, landmarks)
            else:
                face_aligned = st.session_state.face_aligner.align_bbox(face_cropped, [0, 0, face_cropped.shape[1], face_cropped.shape[0]])

            progress_bar.progress(30)

            # Step 3: Calculate ages
            status_text.text("📅 Calculating ages...")

            current_age = DateUtils.calculate_age(birth_date)

            progress_bar.progress(35)

            # Step 4: Age Progression
            status_text.text("⏳ Simulating aging...")

            aged_face = st.session_state.face_aging.age_progression(
                face_aligned,
                current_age=age_in_photo,
                target_age=current_age
            )

            aging_confidence = st.session_state.face_aging.get_confidence_score(
                current_age - age_in_photo
            )

            progress_bar.progress(60)

            # Step 5: Extract Embeddings
            status_text.text("🧬 Extracting facial features...")

            embedding_original = st.session_state.face_embeddings.extract(face_aligned)
            if embedding_original is None:
                st.error("Failed to extract features from original face")
                return

            embedding_aged = st.session_state.face_embeddings.extract(aged_face)
            if embedding_aged is None:
                st.error("Failed to extract features from aged face")
                return

            progress_bar.progress(80)

            # Step 6: Compare Faces
            status_text.text("🔬 Comparing faces...")

            comparison_result = st.session_state.face_comparator.compare(
                embedding_original,
                embedding_aged,
                method='cosine'
            )

            similarity_score = comparison_result['similarity']
            match_confidence = comparison_result['confidence']

            progress_bar.progress(100)
            status_text.text("✅ Analysis complete!")

            # Display Results
            st.success(f"Analysis completed for {person_name}")

            # Summary metrics
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("Age in Photo", f"{age_in_photo} years")

            with col2:
                st.metric("Current Age", f"{current_age} years")

            with col3:
                st.metric(
                    "Similarity Score",
                    f"{similarity_score * 100:.1f}%",
                    delta=st.session_state.face_comparator.get_match_label(similarity_score)
                )

            with col4:
                st.metric(
                    "Confidence",
                    f"{match_confidence * 100:.1f}%",
                    delta=st.session_state.face_comparator.get_confidence_level(match_confidence)
                )

            # Image comparison
            st.markdown("---")
            st.subheader("📸 Visual Comparison")

            col_img1, col_img2 = st.columns(2)

            with col_img1:
                st.markdown(f"**Original Photo (Age: {age_in_photo})**")
                st.image(cv2.cvtColor(face_aligned, cv2.COLOR_BGR2RGB), use_container_width=True)

            with col_img2:
                st.markdown(f"**Aged Simulation (Age: {current_age})**")
                st.image(cv2.cvtColor(aged_face, cv2.COLOR_BGR2RGB), use_container_width=True)

            # Similarity visualization
            st.markdown("---")
            st.subheader("📊 Similarity Analysis")

            # Similarity bar
            similarity_bar = Visualization.create_similarity_bar(similarity_score, width=800, height=60)
            st.image(cv2.cvtColor(similarity_bar, cv2.COLOR_BGR2RGB), use_container_width=True)

            # Detailed metrics
            col_m1, col_m2 = st.columns(2)

            with col_m1:
                st.markdown("**Similarity Metrics**")
                st.write(f"- Cosine Similarity: {similarity_score:.4f}")
                st.write(f"- Distance: {comparison_result['distance']:.4f}")
                st.write(f"- Match Status: {'✅ Match' if comparison_result['match'] else '❌ No Match'}")

            with col_m2:
                st.markdown("**Confidence Analysis**")
                st.write(f"- Aging Confidence: {aging_confidence * 100:.1f}%")
                st.write(f"- Match Confidence: {match_confidence * 100:.1f}%")
                st.write(f"- Age Delta: {current_age - age_in_photo} years")

            # Important notes
            st.markdown("---")
            st.info(
                "**📌 Important Notes:**\n\n"
                f"- Similarity score of **{similarity_score * 100:.1f}%** indicates the likelihood "
                "that both images represent the same person.\n"
                "- This is a **probabilistic estimate**, not a definitive identification.\n"
                "- Accuracy depends on image quality, lighting, pose, and age difference.\n"
                "- Results should **NOT** be used for legal or forensic purposes."
            )

            # Save results
            result_path = settings.get_path('results') / f"{person_name}_{date.today()}.jpg"
            comparison_grid = Visualization.create_comparison_grid(
                face_aligned,
                aged_face,
                similarity_score,
                age_in_photo,
                current_age,
                match_confidence
            )

            if settings.get('ethics.watermark_results', True):
                comparison_grid = ImageUtils.add_watermark(comparison_grid)

            ImageUtils.save_image(comparison_grid, str(result_path))
            st.success(f"Results saved to: {result_path}")

        except Exception as e:
            st.error(f"An error occurred during analysis: {e}")
            logger.error(f"Analysis error: {e}", exc_info=True)

        finally:
            progress_bar.empty()
            status_text.empty()

    # Sidebar info
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"**Version:** {settings.app_version}")
    st.sidebar.markdown("**Powered by:** Deep Learning & Computer Vision")


if __name__ == "__main__":
    main()
