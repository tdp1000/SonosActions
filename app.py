import sqlite3
import requests
from flask import Flask, session, render_template, request, g, jsonify

app = Flask(__name__)
app.secret_key = "jfkodashfdashklj121"


@app.route("/", methods=["POST", "GET"])
def index():
    session["all_items"] = get_db()
    return render_template("index.html", all_items=session["all_items"])


@app.route("/add_items", methods=["post"])
def add_items():
    session["all_items"].append(request.form["select_items"])
    session.modified = True
    return render_template("index.html", all_items=session["all_items"])


@app.route("/card_actions", methods=["POST", "GET"])
def card_actions():
    checked_boxes = request.form.getlist("check")
    list_item = [item for item in session["all_items"] if item[0] in checked_boxes]
    for item in list_item:
        if item in session["all_items"]:
            idx = session["all_items"].index(item)
            session["all_items"].pop(idx)
            session.modified = True
    return render_template("index.html", all_items=session["all_items"])


@app.route("/process_url", methods=["POST"])
def process_url():
    url_data = request.get_json()
    update_db(url_data)
    results = {'processed': 'true'}
    return jsonify(results)


@app.route("/scan_nfc", methods=["GET"])
def scan_nfc():
    results = None
    card = request.args.get('card')
    room = request.args.get('room')
    # print(room)
    session["all_items"] = get_db()
    cards = session["all_items"]
    cards = [(x[0], (x[1], x[3], x[2], x[4])) for x in cards]
    cards = dict(cards)
    # print(cards)
    if card in cards.keys():
        if cards[card] is None:
            pass
            results = dict(processed='true', data='no action')
        else:
            # print(card + str(cards[card]))
            results = dict(processed='true', data='action', action=str(cards[card]))
            action_card(cards[card], room)
    else:
        add_card(card)
    if results is None:
        results = {'processed': 'true', 'data': 'nothing'}
    return jsonify(results)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('card_list.db')
    cursor = db.cursor()
    cursor.execute("select identity, name, service, type, action from cards")
    all_data = cursor.fetchall()
    return all_data


def update_db(data):
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('card_list.db')
    cursor = db.cursor()
    value = str(data[0]["Value"])
    name = data[1]["Name"]
    if data[2]["name"] == "sat":
        field = "type"
    elif data[2]["name"] == "name":
        field = "name"
    elif data[2]["name"] == "serv":
        field = "service"
    else:
        field = "action"
        # playlist = (value.split('playlist/')[1].split('?')[0])
        # playlist = "http://192.168.68.103:5005/playroom/spotify/now/spotify:user:spotify:playlist:" + playlist
        # print(playlist)
    sql = "update cards set " + field + " = '" + value + "' where identity = '" + name + "'"
    print(sql)
    cursor.execute(sql)
    db.commit()
    db.close()


def add_card(card):
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('card_list.db')
    cursor = db.cursor()
    cursor.execute("insert into cards (identity, name) values (?,?)", (card, card))
    db.commit()
    db.close()


def action_card(card_action, room):
    service = card_action[1]
    action_type = card_action[2]
    action = card_action[3]
    if service == "spotify":
        service_action = spotify_action(action_type, action, room)
    elif service == "tunein":
        prefix = "/" + room + "/tunein/play/" + action.split('station:')[1]
        service_action = "http://192.168.68.130:5005" + prefix
    elif service == "sonos":
        prefix = "/" + room + "/" + action.split('command:')[1]
        service_action = "http://192.168.68.130:5005" + prefix
    else:
        print("unknown service")
    get_url = service_action
    get_response = requests.get(get_url).json()
    print(get_url)
    print(get_response['status'])
    print(type(get_response))


def spotify_action(action_type, action, room):
    if action_type == "playlist":
        prefix = "/" + room + "/spotify/now/spotify:user:spotify:playlist:"
        playlist = (action.split('playlist/')[1].split('?')[0])
        action = "http://192.168.68.130:5005" + prefix + playlist
    elif action_type == "album":
        prefix = "/" + room + "/spotify/now/spotify:album:"
        album = (action.split('album/')[1].split('?')[0])
        action = "http://192.168.68.130:5005" + prefix + album
    elif action_type == "track":
        prefix = "/" + room + "/spotify/now/spotify:user:spotify:playlist:"
    else:
        prefix = "/" + room + "/spotify/now/spotify:user:spotify:playlist:"
    return action


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5200)
