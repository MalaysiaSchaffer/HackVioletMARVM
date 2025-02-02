from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

DATABASE = 'astroannotate.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/labels', methods=['GET'])
def get_labels():
    conn = get_db_connection()
    labels = conn.execute('SELECT * FROM image_labels').fetchall()
    conn.close()
    return jsonify([dict(ix) for ix in labels])

@app.route('/api/labels', methods=['POST'])
def add_label():
    new_label = request.get_json()
    conn = get_db_connection()
    conn.execute('INSERT INTO image_labels (image_url, ai_label, human_1_score, human_2_score, human_3_score, human_1_comment, human_2_comment, human_3_comment, ai_accuracy) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                 (new_label['image_url'], new_label['ai_label'], new_label['human_1_score'], new_label['human_2_score'], new_label['human_3_score'], new_label['human_1_comment'], new_label['human_2_comment'], new_label['human_3_comment'], new_label['ai_accuracy']))
    conn.commit()
    conn.close()
    return jsonify(new_label), 201

@app.route('/api/labels/<int:id>', methods=['PUT'])
def update_label(id):
    updated_label = request.get_json()
    conn = get_db_connection()
    conn.execute('UPDATE image_labels SET image_url = ?, ai_label = ?, human_1_score = ?, human_2_score = ?, human_3_score = ?, human_1_comment = ?, human_2_comment = ?, human_3_comment = ?, ai_accuracy = ? WHERE image_id = ?',
                 (updated_label['image_url'], updated_label['ai_label'], updated_label['human_1_score'], updated_label['human_2_score'], updated_label['human_3_score'], updated_label['human_1_comment'], updated_label['human_2_comment'], updated_label['human_3_comment'], updated_label['ai_accuracy'], id))
    conn.commit()
    conn.close()
    return jsonify(updated_label)

@app.route('/api/labels/<int:id>', methods=['DELETE'])
def delete_label(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM image_labels WHERE image_id = ?', (id,))
    conn.commit()
    conn.close()
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
