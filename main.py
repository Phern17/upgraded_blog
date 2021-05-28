from flask import Flask, render_template, request
import requests
import os
import smtplib

app = Flask(__name__)
url_endpoint = 'https://api.npoint.io/0067e63917ca7a5034d9'

json_data = requests.get(url_endpoint).json()
email = os.environ.get("EMAIL")
pwd = os.environ.get("EMAIL_PWD")


@app.route('/')
def home():
    return render_template('index.html', articles=json_data)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/blog/<int:index>')
def get_blog_post(index):
    requested_post = None
    for post in json_data:
        if post['id'] == index:
            requested_post = post
    return render_template('post.html', post=requested_post)


@app.route('/form-entry', methods=["POST"])
def receive_data():
    name = request.form['inputName']
    e_address = request.form['inputEmail']
    phone = request.form['inputPhone']
    msg = request.form['inputMessage']

    structured_msg = f"Subject:From My Blog\n\nName: {name}\nEmail: {e_address}\nPhone: {phone}\nMessage: {msg}"

    connection = smtplib.SMTP("smtp.gmail.com")
    connection.starttls()
    connection.login(user=email, password=pwd)
    connection.sendmail(from_addr=email, to_addrs="mphern17@gmail.com", msg=structured_msg)

    return f'<h1>Successfully submitted your message.</h1>'


if __name__ == "__main__":
    app.run(debug=True)