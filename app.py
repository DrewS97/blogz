from flask import Flask, render_template, request, jsonify
from flask_mysqldb import MySQL
 
app = Flask(__name__)
 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'blogz'
 
mysql = MySQL(app)

#Use database without values
def sql(cmd):
  cur = mysql.connection.cursor()
  query = cur.execute(cmd)
  rv = cur.fetchall()
  mysql.connection.commit()
  cur.close()
  return rv

#Use database with values
def sqlVal(cmd, vals=None):
  cur = mysql.connection.cursor()
  query = cur.execute(cmd, vals)
  rv = cur.fetchall()
  mysql.connection.commit()
  cur.close()
  return rv

#Render Home Page With All Posts Or Individual When Clicked
@app.route('/')
def start_page():
  query = sql('SELECT * FROM blogposts')
  # print(f"\n\n\n {query} \n\n\n")
  return render_template("index.html", query = query)

#Individual Posts
@app.route('/post')
def ind_post():
  id = request.args.get('postID')
  if id != None:
    #Grab values
    title = sqlVal('SELECT Title FROM blogposts WHERE PostID=%s', (id,))
    body = sqlVal('SELECT Body FROM blogposts WHERE PostID=%s', (id,))
    return render_template('individualBlog.html', Title = title[0][0], Body = body[0][0])

#Render Page to add Post
@app.route('/addBlogPost')
def add_blog_post():
  return render_template("addBlogPost.html")

#Render/Re-render post confirmation or page to add post
@app.route('/addBlogPost', methods=["POST"])
def create_post():
  #Input info
  title = str(request.form.get("Post Title"))
  content = str(request.form.get("Post Content"))
  titleLen = len(title)
  contentLen = len(content)

  error = "Please enter a post title under 300 characters and post content under 1000 characters"

  if title != "None" and content != "None":
    if titleLen > 0 and titleLen < 300 and contentLen > 0 and contentLen < 1000:
      #Insert into DB
      sqlVal('INSERT INTO blogposts (UserID, Title, Body) VALUES (%s, %s, %s)', (1, title, content,))
      return render_template("postAdded.html", title = title, content = content)
    else:
      return render_template("addBlogPost.html", error = error)

  return render_template("addBlogPost.html", error = error)


app.run(host='0.0.0.0', port=8080)