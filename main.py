import pymysql
from app import app
from db_config import mysql
from flask import jsonify
from flask import flash, request
from werkzeug.security import generate_password_hash, check_password_hash

@app.route('/')
def root():
	return "Welcome"

@app.route('/addUser', methods=['POST'])
def add_user():
	cursor = None
	conn = None
	try:
		_json = request.json
		_name = _json['name']
		_email = _json['email']
		_password = _json['pwd']

		if _name and _email and _password and request.method == 'POST':

			_hashed_password = generate_password_hash(_password)

			sql = "INSERT INTO tbl_user(user_name, user_email, user_password) VALUES(%s, %s, %s)"
			data = (_name, _email, _hashed_password,)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql, data)
			conn.commit()
			resp = jsonify('User added successfully!')
			resp.status_code = 200
			return resp
		else:
			print("Por favor ingrese todos los datos")
			return not_found()
	except Exception as e:
		print(e)
	finally:
		if cursor:
			cursor.close()
		if conn:
			conn.close()
		
@app.route('/users')
def users():
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM tbl_user")
		rows = cursor.fetchall()
		resp = jsonify(rows)
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
		
@app.route('/user/<int:id>')
def user(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM tbl_user WHERE user_id=%s", id)
		row = cursor.fetchone()
		resp = jsonify(row)
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
		
@app.route('/update', methods=['PUT'])
def update_user():
    conn = None
    cursor = None
    try:
        _json = request.json
        _id = _json.get('id')
        _name = _json.get('name')
        _email = _json.get('email')
        _password = _json.get('pwd')

        if not (_id and _name and _email and _password):
            return jsonify({'error': 'Faltan datos requeridos'}), 400

        conn = mysql.connect()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM tbl_user WHERE user_id = %s", (_id,))
        user = cursor.fetchone()

        if not user:
            return jsonify({'error': f'Usuario con ID {_id} no encontrado'}), 404

        _hashed_password = generate_password_hash(_password)
        sql = """UPDATE tbl_user 
                SET user_name=%s, user_email=%s, user_password=%s 
                WHERE user_id=%s"""
        data = (_name, _email, _hashed_password, _id)
        cursor.execute(sql, data)
        conn.commit()

        return jsonify({'message': 'Usuario actualizado correctamente'}), 200

    except Exception as e:
        print("ERROR:", e)
        return jsonify({'error': str(e)}), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

		
@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_user(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("DELETE FROM tbl_user WHERE user_id=%s", (id,))
		conn.commit()
		resp = jsonify('User deleted successfully!')
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
		
@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp

@app.route('/reset-autoincrement', methods=['POST'])
def reset_autoincrement():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("ALTER TABLE tbl_user AUTO_INCREMENT = 1")
        conn.commit()
        return jsonify({'message': 'AUTO_INCREMENT reiniciado a 1'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

		
if __name__ == "__main__":
    app.run()