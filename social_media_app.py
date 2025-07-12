import streamlit as st
from openai import OpenAI
from typing import Dict, List
import json

# Configure the page
st.set_page_config(
    page_title="Social Media Post Generator",
    page_icon="📱",
    layout="wide"
)

# Title and description
st.title("📱 Social Media Post Generator")
st.markdown("Transform any event into engaging social media posts for LinkedIn, Twitter, and WhatsApp!")

# Sidebar for API key
st.sidebar.header("🔑 Configuration")
api_key = st.sidebar.text_input("Enter your OpenAI API Key:", type="password")

# Initialize OpenAI client
client = None
if api_key:
    client = OpenAI(api_key=api_key)

# Main input section
st.header("📝 Event Details")
event_description = st.text_area(
    "Describe your event:",
    placeholder="e.g., Launched a new AI-powered mobile app that helps users track their fitness goals...",
    height=100
)

# Tone selection
st.header("🎭 Choose Your Tone")
tone_options = {
    "Professional": "Professional and business-focused",
    "Casual": "Friendly and conversational",
    "Excited": "Enthusiastic and energetic",
    "Sarcastic": "Witty and slightly sarcastic",
    "Inspiring": "Motivational and uplifting",
    "Humorous": "Light-hearted and funny"
}

selected_tone = st.selectbox(
    "Select the tone for your posts:",
    list(tone_options.keys())
)

# Additional customization
st.header("⚙️ Customization")
col1, col2 = st.columns(2)

with col1:
    include_hashtags = st.checkbox("Include hashtags", value=True)
    include_call_to_action = st.checkbox("Include call-to-action", value=True)

with col2:
    target_audience = st.selectbox(
        "Target audience:",
        ["General", "Tech professionals", "Business owners", "Students", "Entrepreneurs"]
    )

def generate_social_media_posts(client: OpenAI, event: str, tone: str, platform: str, hashtags: bool, cta: bool, audience: str) -> str:
    """Generate social media post using OpenAI API"""
    
    # Platform-specific guidelines
    platform_guidelines = {
        "LinkedIn": {
            "character_limit": "1300 characters (recommended: 150-300)",
            "style": "Professional networking focus, industry insights, career-related content",
            "format": "Can include line breaks, bullet points, and longer explanations"
        },
        "Twitter": {
            "character_limit": "280 characters maximum",
            "style": "Concise, punchy, trending topics, conversational",
            "format": "Short and sweet, thread-style if needed"
        },
        "WhatsApp": {
            "character_limit": "No strict limit but keep it readable",
            "style": "Personal, direct, emoji-friendly, casual conversation",
            "format": "Like a message to friends/family, can be informal"
        }
    }
    
    guidelines = platform_guidelines[platform]
    
    # Build the prompt
    prompt = f"""
    Create a {tone.lower()} {platform} post about the following event:
    
    Event: {event}
    
    Platform Guidelines:
    - Character limit: {guidelines['character_limit']}
    - Style: {guidelines['style']}
    - Format: {guidelines['format']}
    
    Target Audience: {audience}
    
    Requirements:
    - Match the {tone.lower()} tone perfectly
    - Follow {platform}'s best practices
    - Make it engaging and relevant to {audience.lower()}
    {"- Include relevant hashtags" if hashtags else "- Do not include hashtags"}
    {"- Include a call-to-action" if cta else "- Do not include call-to-action"}
    
    Generate only the post content, nothing else.
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert social media content creator who understands platform-specific best practices and audience engagement."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        return f"Error generating post: {str(e)}"

# Generate posts button
if st.button("🚀 Generate Social Media Posts", type="primary"):
    if not client:
        st.error("Please enter your OpenAI API key in the sidebar.")
    elif not event_description:
        st.error("Please describe your event.")
    else:
        with st.spinner("Generating your social media posts..."):
            
            # Generate posts for each platform
            platforms = ["LinkedIn", "Twitter", "WhatsApp"]
            posts = {}
            
            for platform in platforms:
                posts[platform] = generate_social_media_posts(
                    client,
                    event_description, 
                    selected_tone, 
                    platform, 
                    include_hashtags, 
                    include_call_to_action,
                    target_audience
                )
            
            # Display results
            st.success("✅ Posts generated successfully!")
            
            # Create tabs for each platform
            tab1, tab2, tab3 = st.tabs(["LinkedIn", "Twitter", "WhatsApp"])
            
            with tab1:
                st.subheader("💼 LinkedIn Post")
                st.write(posts["LinkedIn"])
                st.download_button(
                    label="📥 Download LinkedIn Post",
                    data=posts["LinkedIn"],
                    file_name="linkedin_post.txt",
                    mime="text/plain"
                )
            
            with tab2:
                st.subheader("🐦 Twitter Post")
                st.write(posts["Twitter"])
                
                # Character count for Twitter
                char_count = len(posts["Twitter"])
                if char_count > 280:
                    st.warning(f"⚠️ Post is {char_count} characters (exceeds 280 limit)")
                else:
                    st.info(f"✅ {char_count}/280 characters")
                
                st.download_button(
                    label="📥 Download Twitter Post",
                    data=posts["Twitter"],
                    file_name="twitter_post.txt",
                    mime="text/plain"
                )
            
            with tab3:
                st.subheader("💬 WhatsApp Post")
                st.write(posts["WhatsApp"])
                st.download_button(
                    label="📥 Download WhatsApp Post",
                    data=posts["WhatsApp"],
                    file_name="whatsapp_post.txt",
                    mime="text/plain"
                )
            
            # Download all posts
            st.markdown("---")
            all_posts = f"""LINKEDIN POST:
{posts["LinkedIn"]}

TWITTER POST:
{posts["Twitter"]}

WHATSAPP POST:
{posts["WhatsApp"]}
"""
            st.download_button(
                label="📥 Download All Posts",
                data=all_posts,
                file_name="all_social_media_posts.txt",
                mime="text/plain"
            )

# Footer with instructions
st.markdown("---")
st.markdown("""
### 🔧 How to use this app:

1. **Get OpenAI API Key**: Go to [OpenAI's website](https://platform.openai.com/api-keys) and create an API key
2. **Enter API Key**: Paste your API key in the sidebar
3. **Describe Event**: Write a detailed description of your event
4. **Choose Settings**: Select tone, audience, and customization options
5. **Generate**: Click the button to create posts for all platforms
6. **Download**: Save individual posts or download all at once

**💡 Tips for better results:**
- Be specific about your event details
- Include context like achievements, numbers, or outcomes
- Mention your target audience if different from the selected option
- Try different tones to see what works best for your brand
""")

st.markdown("---")
st.markdown("*Built with Streamlit and OpenAI API* 🚀")