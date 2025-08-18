 

from django.shortcuts import render
import google.generativeai as genai
import re
import markdown
import google.auth
from googleapiclient.discovery import build

# Configure the API key for Google Generative AI
genai.configure(api_key="AIzaSyAhLnCtHdpNsfU06LJljQfWY78Z4lQSLTA")

# Configure the API key for YouTube Data API
YOUTUBE_API_KEY = "AIzaSyAXn4LhH2lHOPnFok8I04vcP8-FZVBk_Qo" 


def get_youtube_videos(query):
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    search_response = youtube.search().list(
        q=query,
        part='snippet',
        maxResults=5,
        type='video',
        order='relevance'
    ).execute()

    videos = []
    for item in search_response.get('items', []):
        video_data = {
            'title': item['snippet']['title'],
            'description': item['snippet']['description'],
            'url': f"https://www.youtube.com/watch?v={item['id']['videoId']}"
        }
        videos.append(video_data)
    
    return videos

def extract_title(response_text, prompt):
    # Use regex to find the title in the response text
    match = re.search(r'\*\*Title:\*\*\s*(.+)', response_text)
    if match:                               
        return match.group(1).strip()
    return f"{prompt} course"

def home(request):
    response_data = {}
    youtube_videos = []
    if request.method == 'POST': 
        prompt = request.POST.get('prompt')
        if prompt:
            model = genai.GenerativeModel('gemini-2.5-flash')
            new_prompt2 =f"Explain {prompt} to me . start from the content and explain the concept of each content with examples"
            #new_prompt = f"I want to learn {prompt}. Find me the best {prompt} tutorial video on YouTube that covers from basic to advanced."
            response = model.generate_content(new_prompt2)
            response_text = response.text.strip()
            print("response text =>>>", response_text)
            
            html_response = markdown.markdown(response_text)
            # Extract the title from the response text
            title = extract_title(response_text, prompt)
            
            youtube_videos = get_youtube_videos(title)

            response_data = html_response

    context = {
        'response': response_data,
        'youtube_videos': youtube_videos
    }
    return render(request, 'index.html', context=context)


def about(request):

    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')