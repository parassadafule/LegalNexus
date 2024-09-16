from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")  

@app.route("/chat", methods=['POST'])
def user_query():
    data = request.get_json()
    query = data.get('query')

    type = processQuery(query)
    if type == 0:
        result= division()
    elif type == 1:
        result= judgesAppointed(query)
    elif type == 2:
        result= judgesVacancy()
    elif type == 3:
        result= casePendency(query)
    elif type == 4:
        result = liveStream(query)
    elif type == 5:
        result = welcomeIntent()
    else:
        return jsonify({"result": "Invalid query type"})
    
    query = ""

    return ({"result": result})

def processQuery(query):
    from modules import trainedModel
    tempModel=trainedModel.model
    tempVec = trainedModel.v
    return trainedModel.threshold(query, tempModel, tempVec, threshold=0.5)

def division():
    from modules import divisions
    return divisions.division_info

def casePendency(courtType):
    from modules import case_pendency
    return case_pendency.case(courtType)

def liveStream(courtType):
    from modules import live_streaming
    return live_streaming.live(courtType)

def judgesAppointed(courtType):
    from modules import judges_appointed
    return judges_appointed.judge(courtType)

def judgesVacancy():
    from modules import judges_vacancy
    return judges_vacancy.get_vacancy()

def welcomeIntent():
    return 'hi'

if __name__ == "__main__":
    app.run(debug=True)
