import time

def get_response_stream(prompt):
    text = """ 
    This is some text
    <img src="/src/backend/images/plot.png" alt="Untitled-design" border="0" style="width: 600px; border-radius: 10%; overflow: hidden;">
    """
    # yield letter by letter
    for char in text:
        # wait for 1 second before yielding next character
        time.sleep(0.01)
        yield char