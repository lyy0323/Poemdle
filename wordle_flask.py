from flask import Flask, render_template, request, session
from wordle_utils import Wordle


app = Flask(__name__)
app.secret_key = 'sjtuguoxue123'


@app.route('/', methods=['POST', 'GET'])
def main_page():
    if request.method == 'GET':
        w: Wordle = Wordle()
        session['w'] = w.to_json()
    if request.method == 'POST':
        guessResult = dict(request.form)['guess']
        w: Wordle = Wordle.from_dict(session.get('w'))
        w.set_current(guessResult)
        match_list = w.match()
        match_result = render_template('little.html', w=w, solu=match_list, selected_colors={-1: '#CCBB33', 0: '#999999', 1: '#339933'})
        w.historic.append(match_result)
        session['w'] = w.to_json()
    lent = len(w.historic)
    return render_template('index.html', w=w, lent=lent)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5080, debug=True)
