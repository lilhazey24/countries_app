from flask import Flask, render_template, request
app = Flask(__name__)

def load_data(filename):
    data = {} #dict for data 
    with open(filename,"r") as f: #open file 
        lines = f.readlines()

    city = '' 
    for line in lines: 
        line = line.strip() #removes extra space
        if not line: 
            continue #if line is empty, next one
        if line.endswith(":") and ' ' not in line: #if line ends with :, new city 
            city = line[:-1] #removes colon
            data[city] = {"language":'',"currency": ""}
        elif line.startswith("Language:"):
            data[city]["language"]=line.replace("Language:",'').strip()
        elif line.startswith("Currency:"):
            data[city]["currency"]=line.replace("Currency:",'').strip()
    return data  #return full dict
 
@app.route('/',methods=["GET","POST"])
def index(): 
    all_data = load_data("countries.txt")
    results = {}
    if request.method == "POST": 
        query = request.form.get('query','').strip().lower()
        if query:
            for city, info in all_data.items():
                if (query in city.lower() or query in info["language"].lower() or query in info["currency"].lower()):
                    results[city]=info 
    return render_template("index.html", data=results)
if __name__ == "__main__":
    app.run(debug=True)