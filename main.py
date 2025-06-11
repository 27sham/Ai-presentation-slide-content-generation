
import streamlit as st
import json
import datetime
import random

# Presentation templates for different topics
TEMPLATES = {
    "business": [
        "Executive Summary",
        "Problem Statement", 
        "Market Analysis",
        "Solution Overview",
        "Business Model",
        "Financial Projections",
        "Implementation Timeline",
        "Team & Resources",
        "Risk Assessment",
        "Call to Action"
    ],
    "technical": [
        "Introduction & Overview",
        "Problem Definition",
        "Technical Requirements",
        "Architecture & Design",
        "Implementation Details",
        "Testing & Validation",
        "Performance Analysis",
        "Security Considerations",
        "Future Enhancements",
        "Conclusion"
    ],
    "educational": [
        "Learning Objectives",
        "Background & Context",
        "Key Concepts",
        "Detailed Explanation",
        "Real-world Examples",
        "Interactive Activity",
        "Assessment & Review",
        "Additional Resources",
        "Q&A Session",
        "Summary & Next Steps"
    ],
    "research": [
        "Research Question",
        "Literature Review",
        "Methodology",
        "Data Collection",
        "Results & Analysis",
        "Discussion",
        "Limitations",
        "Implications",
        "Future Research",
        "Conclusions"
    ]
}

def generate_detailed_content(topic, template_type, num_slides):
    """Generate detailed slide content based on topic and template"""
    template = TEMPLATES.get(template_type, TEMPLATES["business"])
    slides = []
    
    for i in range(min(num_slides, len(template))):
        slide_title = template[i]
        slide_content = generate_slide_details(topic, slide_title, template_type)
        slides.append({
            "title": f"Slide {i+1}: {slide_title}",
            "content": slide_content
        })
    
    return slides

def generate_slide_details(topic, slide_title, template_type):
    """Generate specific content for each slide"""
    content_map = {
        "Executive Summary": f"Brief overview of {topic} and its key benefits for stakeholders",
        "Problem Statement": f"Current challenges and pain points related to {topic}",
        "Market Analysis": f"Market size, trends, and opportunities in the {topic} space",
        "Solution Overview": f"How {topic} addresses the identified problems",
        "Introduction & Overview": f"Welcome to our presentation on {topic} - setting the stage",
        "Problem Definition": f"Technical challenges and requirements for {topic}",
        "Learning Objectives": f"What you will learn about {topic} by the end of this session",
        "Research Question": f"Key research questions driving our study of {topic}",
        "Background & Context": f"Historical background and current state of {topic}",
        "Literature Review": f"Previous research and findings related to {topic}",
    }
    
    return content_map.get(slide_title, f"Detailed information about {slide_title} in the context of {topic}")

def export_to_formats(slides, topic):
    """Export slides to different formats"""
    # JSON format
    json_data = {
        "presentation": {
            "topic": topic,
            "created": datetime.datetime.now().isoformat(),
            "slides": slides
        }
    }
    
    # Text format
    text_content = f"PRESENTATION: {topic.upper()}\n"
    text_content += "=" * 50 + "\n\n"
    
    for slide in slides:
        text_content += f"{slide['title']}\n"
        text_content += "-" * len(slide['title']) + "\n"
        text_content += f"{slide['content']}\n\n"
    
    return json_data, text_content

def main():
    st.set_page_config(
        page_title="AI Presentation Generator",
        page_icon="🎯",
        layout="wide"
    )
    
    st.title("🎯 Advanced AI Presentation Generator")
    st.markdown("Create professional presentation outlines with detailed content")
    
    # Sidebar for controls
    with st.sidebar:
        st.header("Presentation Settings")
        
        topic = st.text_input("Enter your topic:", placeholder="e.g., Machine Learning in Healthcare")
        
        template_type = st.selectbox(
            "Choose presentation type:",
            ["business", "technical", "educational", "research"],
            format_func=lambda x: x.title()
        )
        
        num_slides = st.slider("Number of slides:", 3, 15, 8)
        
        st.header("Customization Options")
        include_speaker_notes = st.checkbox("Include speaker notes", value=True)
        include_timing = st.checkbox("Include timing estimates", value=False)
        
        generate_btn = st.button("🚀 Generate Presentation", type="primary")
    
    # Main content area
    if generate_btn and topic:
        with st.spinner("Generating your presentation..."):
            slides = generate_detailed_content(topic, template_type, num_slides)
            
            st.success(f"✅ Generated {len(slides)} slides for '{topic}'")
            
            # Display slides
            st.header("📊 Your Presentation Outline")
            
            # Tabs for different views
            tab1, tab2, tab3 = st.tabs(["📋 Slide Overview", "📝 Detailed View", "📤 Export"])
            
            with tab1:
                # Overview cards
                cols = st.columns(2)
                for i, slide in enumerate(slides):
                    with cols[i % 2]:
                        with st.container():
                            st.markdown(f"### {slide['title']}")
                            st.write(slide['content'])
                            
                            if include_timing:
                                estimated_time = random.randint(2, 5)
                                st.caption(f"⏱️ Estimated time: {estimated_time} minutes")
                            
                            if include_speaker_notes:
                                with st.expander("💡 Speaker Notes"):
                                    st.write(f"Key points to emphasize: Make sure to engage the audience when discussing {slide['title'].lower()}. Use visual aids where possible.")
            
            with tab2:
                # Detailed view with editing capability
                st.markdown("### 📝 Edit Your Slides")
                for i, slide in enumerate(slides):
                    with st.expander(f"{slide['title']}", expanded=i==0):
                        new_content = st.text_area(
                            f"Content for slide {i+1}:",
                            value=slide['content'],
                            height=100,
                            key=f"slide_{i}"
                        )
                        slides[i]['content'] = new_content
            
            with tab3:
                # Export options
                st.markdown("### 📤 Export Your Presentation")
                
                json_data, text_content = export_to_formats(slides, topic)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.download_button(
                        label="📄 Download as JSON",
                        data=json.dumps(json_data, indent=2),
                        file_name=f"{topic.replace(' ', '_')}_presentation.json",
                        mime="application/json"
                    )
                
                with col2:
                    st.download_button(
                        label="📝 Download as Text",
                        data=text_content,
                        file_name=f"{topic.replace(' ', '_')}_presentation.txt",
                        mime="text/plain"
                    )
                
                # Preview exports
                with st.expander("🔍 Preview JSON Export"):
                    st.json(json_data)
                
                with st.expander("🔍 Preview Text Export"):
                    st.text(text_content)
    
    elif generate_btn and not topic:
        st.error("⚠️ Please enter a topic to generate your presentation!")
    
    # Footer with additional features
    st.markdown("---")
    with st.expander("ℹ️ About This Tool"):
        st.markdown("""
        **Features:**
        - Multiple presentation templates (Business, Technical, Educational, Research)
        - Customizable number of slides
        - Speaker notes and timing estimates
        - Export to JSON and Text formats
        - Interactive slide editing
        
        **Tips for better presentations:**
        - Keep slides concise and focused
        - Use visual elements where possible
        - Practice your timing
        - Engage with your audience
        """)

if __name__ == "__main__":
    main()
