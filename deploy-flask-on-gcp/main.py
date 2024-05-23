from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Dummy data for demonstration
images_data = [
    {'filename': 'image1.jpg', 'title': 'Image 1', 'description': 'Description for Image 1'},
    {'filename': 'image2.jpg', 'title': 'Image 2', 'description': 'Description for Image 2'},
    {'filename': 'image3.jpg', 'title': 'Image 3', 'description': 'Description for Image 3'},
    {'filename': 'image4.jpg', 'title': 'Image 4', 'description': 'Description for Image 4'},
    {'filename': 'image5.jpg', 'title': 'Image 5', 'description': 'Description for Image 5'},
    {'filename': 'image6.jpg', 'title': 'Image 6', 'description': 'Description for Image 6'},
    {'filename': 'image7.jpg', 'title': 'Image 7', 'description': 'Description for Image 7'},
    {'filename': 'image8.jpg', 'title': 'Image 8', 'description': 'Description for Image 8'},
    {'filename': 'image9.jpg', 'title': 'Image 9', 'description': 'Description for Image 9'},
]

articles_data = [
    {'title': 'Article 1', 'date': '2022-03-16', 'summary': 'Summary of Article 1', 'author': 'Author 1'},
    {'title': 'Article 2', 'date': '2022-03-15', 'summary': 'Summary of Article 2', 'author': 'Author 2'},
    {'title': 'Article 3', 'date': '2012-03-14', 'summary': 'Summary of Article 3', 'author': 'Author 3'},
    {'title': 'Article 4', 'date': '2005-05-16', 'summary': 'Summary of Article 4', 'author': 'Author 4'},
    {'title': 'Article 5', 'date': '2006-06-15', 'summary': 'Summary of Article 5', 'author': 'Author 5'},
    {'title': 'Article 6', 'date': '2009-08-14', 'summary': 'Summary of Article 6', 'author': 'Author 6'},
    {'title': 'Article 7', 'date': '2013-04-15', 'summary': 'Summary of Article 7', 'author': 'Author 7'},
    {'title': 'Article 8', 'date': '2020-11-14', 'summary': 'Summary of Article 8', 'author': 'Author 8'},
    {'title': 'Article 9', 'date': '2023-12-15', 'summary': 'Summary of Article 9', 'author': 'Author 9'},
    {'title': 'Article 10', 'date': '2021-05-14', 'summary': 'Summary of Article 10', 'author': 'Author 10'},
]


videos_data = [
    {'filename': 'video1.mp4'},
    {'filename': 'video2.mp4'},
]

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/images')
def images():
    return render_template('images.html', images=images_data)

@app.route('/articles')
def articles():
    return render_template('articles.html', articles=articles_data)

@app.route('/videos')
def videos():
    return render_template('videos.html', videos=videos_data)

@app.route('/feedbacks', methods=['GET', 'POST'])
def feedbacks():
    if request.method == 'POST':
        # Handle form submission
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        # Process the data (e.g., save to database)
        # Redirect to a thank you page or home page
        return redirect(url_for('articles'))
    return render_template('feedbacks.html')

@app.route('/post', methods=['POST'])
def post():
    # Handle form submission
    # Example: data = request.form['data']
    return 'Posted successfully'

if __name__ == '__main__':
    app.run()
