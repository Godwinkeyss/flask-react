from flask import request, jsonify
from config import app, db
from models import Contact

@app.route('/contact', methods=['GET'])
def index():
    contacts = Contact.query.all()
    result = list(map(lambda x: x.to_json(), contacts))
    return jsonify({"contacts": result})

@app.route('/create', methods=['GET','POST'])
def create_contact():
    first_name = request.json.get('firstName')
    last_name =  request.json.get('lastName')
    email =  request.json.get('email')

    if not first_name or not last_name or not email:
        return (jsonify({'Message':'Please enter all field'}), 400)
    new_contact = Contact(first_name=first_name, last_name=last_name, email=email)
    try:
        db.session.add(new_contact)
        db.session.commit()
    except Exception as e:
        return (jsonify({'message': str(e)}), 400)
    
    return (jsonify({'message':'Contact created successfully'}), 200)
    
@app.route('/contact/<int:user_id>', methods=['GET'])
def get_single_contact(user_id):
    contact = Contact.query.get(user_id)
    if not contact:
        return (jsonify({'message':'user not found'}), 404)
    return jsonify(contact.to_json())
@app.route('/update/<int:user_id>', methods=['PATCH'])
def update(user_id):
    check_contact = Contact.query.get(user_id)
    if not check_contact:
        return (jsonify({'message':'user not found'}), 404)
    data = request.json
    check_contact.first_name = data.get('firstName', check_contact.first_name)
    check_contact.last_name = data.get('lastName', check_contact.last_name)
    check_contact.email = data.get('email', check_contact.email)

    db.session.add(check_contact)
    db.session.commit()

    return jsonify({"message":"Contact updated successfully"}),201

@app.route('/delete/<int:user_id>',methods=['DELETE'])
def delete(user_id):
    contact = Contact.query.get(user_id)
    if not contact:
        return (jsonify({"message":" User not found"})), 404
    db.session.delete(contact)
    db.session.commit()
    return (jsonify({"message":"user deleted successfully"}), 200)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)