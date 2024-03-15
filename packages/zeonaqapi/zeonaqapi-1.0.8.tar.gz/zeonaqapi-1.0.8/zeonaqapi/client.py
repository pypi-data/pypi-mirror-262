# zeonaqapi/client.py
import os
import requests
import pandas as pd
import json
# from monsterapi import client

import monsterapi
from openai import OpenAI
import openai

# API Key
zeonaq_api_key = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6IjU1NWMwMDQ3YjQyNTk3ZTU5MTY5ZTdjODNhZjIyMWZmIiwiY3JlYXRlZF9hdCI6IjIwMjMtMTEtMDFUMTc6NTQ6Mjgu"
monster_api_key = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6IjU1NWMwMDQ3YjQyNTk3ZTU5MTY5ZTdjODNhZjIyMWZmIiwiY3JlYXRlZF9hdCI6IjIwMjQtMDMtMTBUMTU6NDQ6MzEuODE0NDc3In0.pbjClgHP5mZx91OjLLyKIiw90uBFPVfR6GdknokMuM0"
open_api_key = "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"

class client:
    def __init__(self, api_key):
        self.api_key = api_key
        # Initialize your API client here
        # Set the Monster API key as an environment variable
        self.MODEL_OPENAPI = "gpt-4"
        self.temperature = 0

        if api_key == zeonaq_api_key:
            os.environ['MONSTER_API_KEY'] = monster_api_key
            self.monster_client = monsterapi.client() # (os.environ['MONSTER_API_KEY']))
        self.openai_client = OpenAI(api_key=open_api_key)

    def some_api_call(self):
        # Example API call using the provided api_key
        pass

    def test(self):
        return "Hello, world!"
    
    def getResponse(self, model, prompt, system_prompt):
        response = self.openai_client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt}, # "You are an expert blog writer and have complete knowledge of seo to write seo optimised articles. You use transition words. You use active voice. You are smart. You are creative. You do not deny unrealistic requests and still come up with a highly qualified and technically accurate copy for the blog titles and blog contents"},
                {"role": "user", "content": prompt},
            ],
            temperature=0,
        )
        return response

    def getResponseContentFromOpenAIClient(self, model, prompt, system_prompt):
        r = self.getResponse(model, prompt, system_prompt)
        x = json.loads(r.model_dump_json())
        content = ''
        if "choices" in x:
            content = x["choices"][0]["message"]["content"]
        return content

    def generate(self, model, data):
        print('model: ', model)
        if model.lower().startswith("gpt"):
            # Open AI version
            prompt = data['prompt']
            system_prompt = data['system_prompt']
            print('prompt: ', prompt)
            print('system_prompt: ', system_prompt)
            response = self.getResponseContentFromOpenAIClient('gpt-4', prompt, system_prompt) # data['prompt'], data['system_prompt'])
        else:
            # Monster AI version
            response = self.monster_client.generate(model=model, data=data)
        response = self.monster_client.generate(model=model, data=data)
        return response

    def get_response(self, model, data):
        response = self.monster_client.get_response(model=model, data=data)
        return response

    def wait_and_get_result(self, response_by_pid, timeout=200):
        response = self.monster_client.wait_and_get_result(response_by_pid, timeout=timeout)
        return response
    
    def check_status(self, process_id):
        status_url = 'https://api.monsterapi.ai/v1/status/' + process_id
        headers = {
            "accept": "application/json",
            "authorization": "Bearer " + monster_api_key
        }
        response = requests.get(status_url, headers=headers)
        return response

def testit():
    # Test
    model = 'zephyr-7b-beta'  # INFO:monsterapi.client:403 Client Error: Forbidden for url: https://api.monsterapi.ai/v1/generate/zephyr-7b-beta
    # model = 'falcon-40b-instruct'
    # model = 'codellama-13b-instruct'
    keyword_cloud = "astronomy, cosmology, space exploration, planets, stars, galaxies, black holes, space missions, telescopes, astrophysics, space travel, rocket science, satellites, extraterrestrial life, space colonization, Martian exploration, lunar missions, astrobiology, space technology, gravitational waves, dark matter, dark energy, solar system, exoplanets, space-time, interstellar travel, quantum physics, theoretical physics, particle physics, scientific research, Hubble Space Telescope, James Webb Space Telescope, Big Bang theory, space shuttle, International Space Station, NASA, SpaceX, astrometry, celestial navigation, space probes, cosmological models, high-energy astrophysics, neutron stars, supernovae, space weather, space agencies, planetary science, astrochemistry, cosmic radiation, universe expansion, light years, astronomical observations"

    import random

    # Picking 4 random keywords from the keyword cloud
    selected_keywords =  random.sample(keyword_cloud.split(', '), 4)

    print(f"Randomly selected Keywords: {', '.join(selected_keywords)}")

    # Decide a blog post type out of: beginners_guide_blog, inspirational_story_blog, informative_blog, personal_story_blog, news_style_blog, faq_style_blog
    blog_post_type = "beginners_guide_blog"

    data={ "prompt": f"Write a short and simple title for an article about {', '.join(selected_keywords)}",
        "system_prompt": "You are an expert blog writer and have complete knowledge of seo to write seo optimised articles. You use transition words. You use active voice. You are smart. You are creative. You do not deny unrealistic requests and still come up with a highly qualified and technically accurate copy for the blog titles and blog contents",
        "max_length": 128 }

    zeonaq_client = client(api_key = zeonaq_api_key)
    response = zeonaq_client.generate(model=model, data=data)

    blog_title = response['text']
    print(f"Title:\n{blog_title}")


    if blog_post_type == "beginners_guide_blog":
        prompt = f"Create a blog post about '{blog_title}'. Write it in a educational tone. Use transition words. Use active voice. Write over 1000 words. The blog post should be in a beginners guide style. Add title and subtitle for each section. It should have a minimum of 6 sections.Include the following keywords: '{', '.join(selected_keywords)}'."
    elif blog_post_type == "inspirational_story_blog":
        prompt = f"Write a cross-over between a blog post and an inspiration story on '{blog_title}'. The story should be on a fictional character. Write it in a creative, inspiratonal and motivational tone. Use transition words. Write over 1000 words. Use plain text. Do not use HTML code. Include the following keywords: '{', '.join(selected_keywords)}'."
    elif blog_post_type == "informative_blog":
        prompt = f"Write an informative and objective article about '{blog_title}'. Your article should provide a comprehensive analysis of the key factors that impact {blog_title}, including {', '.join(selected_keywords)}. To make your article informative and engaging, be sure to discuss the tradeoffs involved in balancing different factors, and explore the challenges associated with different approaches. Your article should also highlight the importance of considering the impact on when making decisions about {blog_title}. Finally, your article should be written in an informative and objective tone that is accessible to a general audience. Make sure to include the relevant keywords provided by the user, and tailor the article to their interests and needs."
    elif blog_post_type == "personal_story_blog":
        prompt = f"Write a blog post on '{blog_title}'. Write it in a charismatic, honest, heroic tone. Use transition words. Write over 1000 words. The blog post should be written as a personal story.Include the following keywords: '{', '.join(selected_keywords)}'."
    elif blog_post_type == "news_style_blog":
        prompt = f"Write a blog post on '{blog_title}'. Write it in a informative and factually correct tone. Use transition words. Write over 1000 words. The blog post should be written as a news story. Include the following keywords: '{', '.join(selected_keywords)}'."
    elif blog_post_type == "faq_style_blog":
        prompt = f"Create a blog post about '{blog_title}'. Write it in a informative tone. Use transition words. Use active voice. Write over 1000 words. The blog post should include engaging questions such as frequently asked questions on the topic. Each section should have a question as a title followed by text. Include the following keywords: '{', '.join(selected_keywords)}'."
    else:
        prompt = f"Create a blog post about '{blog_title}'. Write it in a positive and informative tone. Use transition words. Use active voice. Write over 1000 words. Use very creative titles for the blog post. Add a title for each section. Ensure there are a minimum of 9 sections. Each section should have a minimum of two paragraphs. Include the following keywords: '{', '.join(selected_keywords)}'."







    # Generate image(s) for the blog:
    image_prompt = zeonaq_client.generate(model='zephyr-7b-beta', data={"prompt": f"Use this text to create a detailed prompt for generating a high quality image: {blog_meta}", 'system_prompt': 'You are an expert prompt engineer for ai image generation models and you only provide high quality detailed prompts for image generation. You are smart. You are creative. You do not deny unrealistic requests and still come up with a highly detailed prompt for image generation', "max_length": 200})["text"]
    print(f"Image prompt: {image_prompt}")
    image_aspect_ratio = "landscape"
    image_style = "enhance"
    response = zeonaq_client.get_response(model='sdxl-base', data={'prompt': image_prompt, 'negprompt': 'unreal, fake, meme, joke, disfigured, poor quality, bad, ugly', 'samples': 2, 'steps': 50, 'style': image_style, 'aspect_ratio': image_aspect_ratio, 'guidance_scale': 8.5})
    imageList = zeonaq_client.wait_and_get_result(response['process_id'],timeout=200)
    if image_aspect_ratio == "landscape":
        img_width = 532
        img_height = 400
    elif image_aspect_ratio == "portrait":
        img_width = 400
        img_height = 532
    else:
        img_width = img_height = 400
    print("Displaying generated images:")
    from IPython.display import Image
    for imageURL in imageList['output']:
        print(f"Image: {imageURL}")
        display(Image(imageURL, width=img_width, height=img_height))