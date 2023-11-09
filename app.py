from flask import Flask, render_template, request, session  # from module import Class.
import os 

import hfpy_utils
import swim_utils


app = Flask(__name__)
app.secret_key = ":)"

@app.get("/")
@app.get("/getswimmers")
def get_swimmers_names():
    files = os.listdir(swim_utils.FOLDER)
    files.remove(".DS_Store")
    names = set()
    for swimmer in files:
        names.add(swim_utils.get_swimmers_data(swimmer)[0])
    return render_template(
        "select.html",
        title="Select a swimmer to chart",
        data=sorted(names),
    )


@app.post("/displayevents")
def get_swimmer_events():
    chosenName = request.form["swimmer"]
    session["chosenName"] = chosenName
    session.modified = True
    files = os.listdir(swim_utils.FOLDER)
    files.remove(".DS_Store")
    events = list()
    for event in files:
        if(swim_utils.get_swimmers_data(event)[0] == chosenName):
            events.append(
                swim_utils.get_swimmers_data(event)[1] + "-" +
                swim_utils.get_swimmers_data(event)[2] + "-" +
                swim_utils.get_swimmers_data(event)[3]
                )
    return render_template(
        "selectEvent.html",
        title="Select an event for " + chosenName + " to chart",
        data=sorted(events) 
    )

@app.post("/charts")
def display_chart():
    chosenName = session["chosenName"]
    chosenEvent = request.form["event"]
    (
        name,
        age,
        distance,
        stroke,
        the_times,
        converts,
        the_average,
    ) = swim_utils.get_swimmers_data(chosenName + "-" + chosenEvent + ".txt")

    the_title = f"{name} (Under {age}) {distance} {stroke}"
    from_max = max(converts) + 50
    the_converts = [ hfpy_utils.convert2range(n, 0, from_max, 0, 350) for n in converts ]

    the_data = zip(the_converts, the_times)

    return render_template(
        "chart.html",
        title=the_title,
        average=the_average,
        data=the_data,
    )

if __name__ == "__main__":
    app.run(debug=True)  # Starts a local (test) webserver, and waits... forever.
