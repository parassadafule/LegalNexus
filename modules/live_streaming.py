from modules.court_code import live_links

def live_stream_high(court_type):
    for key in live_links:
        if key in court_type:
            url = live_links[key]
            return url
    return "No live stream found for court"    

def live_stream_supreme():
    url = "https://www.youtube.com/@supremecourtofindia5950/streams"
    return url

def live(court_type):
    if 'high' in court_type:
        live_stream = live_stream_high(court_type)
    elif 'supreme' in court_type:
        live_stream = live_stream_supreme()
    else:
        live_stream = {"error": "Invalid court type"}
    
    return live_stream