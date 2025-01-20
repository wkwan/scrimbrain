# Prompting with video docs: https://ai.google.dev/gemini-api/docs/vision?_gl=1*wu85lt*_up*MQ..*_ga*MTczNTEyODE5Ni4xNzM3NDA1MTM2*_ga_P1DBVKWT6V*MTczNzQwNTEzNS4xLjAuMTczNzQwNTEzNS4wLjAuNzA1NTEwNDky&lang=python#prompting-video

import google.generativeai as genai # pip install -q -U google-generativeai
import time

genai.configure(api_key="YOUR_API_KEY")
model = genai.GenerativeModel("gemini-2.0-flash-exp")

# Upload the video and print a confirmation.
video_file_name = "test-data-viz.mp4"

print(f"Uploading file...")
video_file = genai.upload_file(path=video_file_name)
print(f"Completed upload: {video_file.uri}")

# Check whether the file is ready to be used.
while video_file.state.name == "PROCESSING":
    print('.', end='')
    time.sleep(10)
    video_file = genai.get_file(video_file.name)

if video_file.state.name == "FAILED":
  raise ValueError(video_file.state.name)

# Create the prompt.
prompt = "You output Python code and nothing else. Generate a Python script that uses Manim to render an animated data visualization video like this, but with green bars instead of blue. Make the bars horizontal, starting from the left side of the screen at exactly the y-axis of the graph. Change the font to Comic Sans MS."

# Make the LLM request.
print("Making LLM inference request...")
response = model.generate_content([video_file, prompt],
                                  request_options={"timeout": 600})

# Save the response to a file (usually need to fix bugs in the code)
with open('gemini_out_manim.py', 'w') as f:
    f.write(response.text)