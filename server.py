from __future__ import print_function
import base64
import os
from flask import Flask, flash, request, redirect, url_for, send_from_directory, current_app
from werkzeug.utils import secure_filename
from pymongo import MongoClient
import random
import datetime
from flask import Flask, session
from flask_session import Session
import time
import cloudmersive_convert_api_client
from cloudmersive_convert_api_client.rest import ApiException
from pprint import pprint
import webbrowser
from collections import OrderedDict
from duckduckgo_search import ddg
import ssl
import typesense
from datetime import datetime

client = typesense.Client({
  'nodes': [{
    'host': '', # For Typesense Cloud use xxx.a1.typesense.net
    'port': '',      # For Typesense Cloud use 443
    'protocol': ''   # For Typesense Cloud use https
  }],
  'api_key': '',
  'connection_timeout_seconds': 2
})




context = ssl.SSLContext()
context.load_cert_chain('', '')

clientdb = MongoClient('')
db=clientdb.Searchcord

UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__, static_url_path='/static/')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config["DEBUG"] = True

app.secret_key = ''
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_COOKIE_NAME'] = ""
app.config['SECRET_KEY'] = os.urandom(24)


def countupcont():
    #statistiken über die totale anzahl der aufrufe
    likes = db.statis
    likesbyuser = likes.find_one({"counter": "counter"})
    if not likesbyuser == None:
        count = likesbyuser['contextviews']
        count = int(count) + 1
        likes.update_one(
            {"counter": "counter"},
            { "$set": { "contextviews": count } }
            )

def countup():
    #statistiken über die totale anzahl der aufrufe
    likes = db.statis
    likesbyuser = likes.find_one({"counter": "counter"})
    if not likesbyuser == None:
        count = likesbyuser['aufrufe']
        count = int(count) + 1
        likes.update_one(
            {"counter": "counter"},
            { "$set": { "aufrufe": count } }
            )

def searchcountup():
    #statistiken über die anzahl der suchen
    likes = db.statis
    likesbyuser = likes.find_one({"counter": "counter"})
    if not likesbyuser == None:
        count = likesbyuser['suchen']
        count = int(count) + 1
        likes.update_one(
            {"counter": "counter"},
            { "$set": { "suchen": count } }
            )
            
@app.route('/uploads/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    countup()
    print(filename)
    # Appending app path to upload folder path within app root folder
    uploads = os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER'])
    # Returning file from appended path
    path = f'{uploads}{filename}'
    
    
    return send_from_directory(directory=uploads, filename=filename, path = path)


@app.route('/', methods=['GET'])
def startpage():
    countup()
    #searchcountup()
    return """

    


       <!DOCTYPE html>
       <html>
       <head>
         <style>
           a.fill-div {
           display: block;
           height: 100%;
           width: 100%;
           text-decoration: none;
       }
       * {
         margin: 0;
         padding: 0;
         box-sizing: border-box;
         /*border: 1px solid red;*/
       }

       .suchpart {
         display: flex;
         flex-direction: column;
         align-items: center;
         background-color: #f9f9fb;
         padding: 30px;
         font-family: Segoe UI, sans-serif;
       }

       .logo-and-brand {
         display: flex;
         align-items: center;
         justify-content: center;
         gap: 10px;
         width: 80%;
         margin: 40px 0;
       }

       .firefox-logo {
         width: 80px;
         height: auto;
       }

       .brand {
         font-size: 46px;
       }

       .search-wrapper {
         background-color: rgba(249, 249, 249, 0.95);
         width: 100%;
         height: 100px;
         padding: 25px 0;
         margin-bottom: 50px;
         position: sticky;
         top: 0;
         z-index: 1;
       }

       form {
         width: 720px;
         position: relative;
         margin: auto;
       }

       .ddg-logo {
         width: 25px;
         position: absolute;
         top: 11px;
         left: 15px;
       }

       .search-bar {
         width: 100%;
         padding: 15px;
         padding-left: 50px;
         height: 50px;


         border-radius:  8px 0 0 8px  ;
         box-shadow: 0 2px 6px rgba(58, 57, 68, 0.2);
         border: none;
         font-size: 15px;
       }


       .search-bar::placeholder {
         color: #000;
         opacity: 0.5;
       }

       .search-bar:focus {
         outline: 1px solid #ffffff;
       }

       .section-wrapper {
         width: 966px;
         padding: 10px;
       }

       .pocket-heading {
         display: inline;
         font-size: 17px;
         margin-right: 10px;
       }

       .link {
         text-decoration: none;
         color: #0060DF;
         font-size: 13px;
       }

       .link:hover {
         text-decoration: underline;
       }

       .card-wrapper {
         margin: 20px 0;
         display: grid;
         grid-template-columns: repeat(3, 1fr);
         grid-template-rows: repeat(4, 350px);
         grid-gap: 24px;
       }

       .search-result {
         max-width: 900px;

         background-color: #FFF;
         border-radius: 8px;
         box-shadow: 0 2px 6px rgba(58, 57, 68, 0.2);
         position: relative;
         border: none;
           padding: 15px 20px 20px 20px;

           width: 100%;
         padding: 15px;
         padding-left: 50px;
         width:80vh;
         border-radius: 8px;
         box-shadow: 0 2px 6px rgba(58, 57, 68, 0.2);
         border: none;
         font-size: 15px;

       }

       span {
         position: absolute;
         top: 0;
         left: 0;
         width: 100%;
         height: 100%;
       }



       body{
           display: flex;
         flex-direction: column;
         align-items: center;
         background-color: #f9f9fb;
         padding: 30px;
         font-family: Segoe UI, sans-serif;
       }
       .ibox-content {

           color: inherit;
           padding: 15px 20px 20px 20px;
           border-color: #E7EAEC;
           border-image: none;
           border-style: solid solid none;
           border-width: 1px 0px;
       }

       .search-form {
           margin-top: 10px;
           box-shadow: 0 2px 6px rgba(58, 57, 68, 0.2);

       }

       .search-result h3 {
           margin-bottom: 0;
           color: #1E0FBE;
       }

       .search-result .search-link {
           color: #006621;
       }

       .search-result p {
           font-size: 12px;
           margin-top: 5px;
       }

       .hr-line-dashed {
           border-top: 1px dashed #E7EAEC;
           color: #ffffff;
           background-color: #ffffff;
           height: 1px;
           margin: 20px 0;
       }

       h2 {
           font-size: 24px;
           font-weight: 100;
       }

   .button {
       position: fixed;
     right: 1rem;
     bottom: 1rem;
     min-width: 300px;
     min-height: 60px;
     font-family: 'Nunito', sans-serif;
     font-size: 22px;
     text-transform: uppercase;
     letter-spacing: 1.3px;
     font-weight: 700;
     color: #313133;
     background: #4FD1C5;
   background: linear-gradient(90deg, rgba(129,230,217,1) 0%, rgba(79,209,197,1) 100%);
     border: none;
     border-radius: 1000px;
     box-shadow: 12px 12px 24px rgba(79,209,197,.64);
     transition: all 0.3s ease-in-out 0s;
     cursor: pointer;
     outline: none;

     padding: 10px;
     }

   button::before {
   content: '';
     border-radius: 1000px;
     min-width: calc(300px + 12px);
     min-height: calc(60px + 12px);
     border: 6px solid #00FFCB;
     box-shadow: 0 0 60px rgba(0,255,203,.64);
     position: absolute;
     top: 50%;
     left: 50%;
     transform: translate(-50%, -50%);
     opacity: 0;
     transition: all .3s ease-in-out 0s;
   }

   .button:hover, .button:focus {
     color: #313133;
     transform: translateY(-6px);
   }

   button:hover::before, button:focus::before {
     opacity: 1;
   }

   button::after {
     content: '';
     width: 30px; height: 30px;
     border-radius: 100%;
     border: 6px solid #00FFCB;
     position: absolute;
     z-index: -1;
     top: 50%;
     left: 50%;
     transform: translate(-50%, -50%);
     animation: ring 1.5s infinite;
   }

   button:hover::after, button:focus::after {
     animation: none;
     display: none;
   }

   @keyframes ring {
     0% {
       width: 30px;
       height: 30px;
       opacity: 1;
     }
     100% {
       width: 300px;
       height: 300px;
       opacity: 0;
     }
   }

   select {
      -webkit-appearance:none;
      -moz-appearance:none;
      -ms-appearance:none;
      appearance:none;
      outline:0;
      box-shadow:none;
      border:0!important;
      border-radius:  0 8px 8px 0   ;
      background: #ffffff;
      background-image: none;
      flex: 1;
      padding: 0 .5em;
      color:rgb(0, 0, 0);
      cursor:pointer;
      font-size: 1em;
      font-family: 'Open Sans', sans-serif;

   }
   select::-ms-expand {
      display: none;
   }
   .select {
      position: relative;
      display: flex;
      width: 10em;

      height: 50px;
      line-height: 3;
      background: #ffffff;
      overflow: hidden;

      border-radius:  0 8px 8px 0   ;
      box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
   }
   .select::after {
      content: '▼';
      position: absolute;
      top: 0;
      right: 0;
      padding: 0 1em;
      background:  #ffffff;
      cursor:pointer;
      pointer-events:none;
      transition:.25s all ease;
      border-bottom-left-radius:-1px;
      height: 50px;
   }
   .select:hover::after {
      color: #23b499;
   }




   .float-child2 {
       width: 10%;
       float: left;
       padding: 0px;

   }
   .float-child {
       width: 75%;
       float: left;
       padding: 0px;

   }

       a.fill-div {
       display: block;
       height: 100%;
       width: 100%;
       text-decoration: none;
   }
   * {
     margin: 0;
     padding: 0;
     box-sizing: border-box;
     /*border: 1px solid red;*/
   }

   .section-wrapper {
     width: 966px;
     padding: 10px;
   }

   .pocket-heading {
     display: inline;
     font-size: 17px;
     margin-right: 10px;
   }

   .link {
     text-decoration: none;
     color: #0060DF;
     font-size: 13px;
   }

   .link:hover {
     text-decoration: underline;
   }

   .card-wrapper {
     margin: 20px 0;
     display: grid;
     grid-template-columns: repeat(3, 1fr);
     grid-template-rows: repeat(4, 350px);
     grid-gap: 24px;
   }

   .card {
     max-width: 300px;
     background-color: #FFF;
     border-radius: 8px;
     box-shadow: 0 2px 6px rgba(58, 57, 68, 0.2);
     position: relative;
   }

   span {
     position: absolute;
     top: 0;
     left: 0;
     width: 100%;
     height: 100%;
   }

   .card-image {
     width: 100%;
     border-radius: 8px 8px 0 0;
   }

   .card-description {
     padding: 15px;
   }

   .card-site {
     font-size: 16px;
     color: #777;
     font-weight: normal;
     margin-bottom: 10px;
   }

   .card-link {
     text-decoration: none;
     color: #000;
     font-weight: bold;
   }

   .card-link:hover {
     color: #0060DF;
   }

   .card-text {
     font-size: 14px;
     margin-top: 5px;
   }

   footer {
     display: flex;
     justify-content: space-between;
   }

   footer ul {
     display: flex;
     flex-wrap: wrap;
     list-style: none;
     gap: 10px;
     font-size: 14px;
   }

   @media (max-width: 1100px) {
     form {
       width: 600px;
     }

     .section-wrapper {
       width: 726px;
     }

     footer ul,
     footer .link {
       font-size: 10px;
     }
   }

   @media (max-width: 900px) {
     form {
       width: 360px;
     }

     .section-wrapper {
       width: 490px;
     }

     .card-wrapper {
       grid-template-columns: repeat(2, 1fr);
     }
   }

   @media (max-width: 600px) {
     form {
       width: 200px;
     }

     .section-wrapper {
       width: 246px;
     }

     .card-wrapper {
       grid-template-columns: 1fr;
     }
   }
   body {
     display: flex;
     flex-direction: column;
     align-items: center;
     background-color: #f9f9fb;
     padding: 30px;
     font-family: Segoe UI, sans-serif;
   }

   .logo-and-brand {
     display: flex;
     align-items: center;
     justify-content: center;
     gap: 10px;
     width: 80%;
     margin: 40px 0;
   }

   .firefox-logo {
     width: 80px;
     height: auto;
   }

   .brand {
     font-size: 46px;
   }

         </style>
         <meta charset="utf-8">
         <meta name="viewport" content="width=device-width, initial-scale=1">
         <title>Search-Cord</title>

       </head>
       <body>

       <section class="suchpart">
         <section class="logo-and-brand">
           <img
             class="firefox-logo"
             src="https://search-cord.com/uploads/3543843868965spaffel_sad_transpa22.png"
             alt="Cloud-logo">
           <a href="/" style="text-decoration: none; color: black;"><h1 class="brand">Search-Cord</h1></a>
         </section>
         <section class="search-wrapper">
           <form action="/search" method=post enctype=multipart/form-data class="float-container">
             <img
               class="ddg-logo"
               src="https://search-cord.com/uploads/329190864793search_icon_152764.png"
               alt="ddg-logo">
           <section class="float-container2">
               <div class="float-child">
             <input
               class="search-bar"
               type="text"

               name = "Suche"
               placeholder="Search in archived messages....">
               </div>
                   <div class="float-child2">
                       <div class="select">

                           <select id="fach" name="Fach" onchange="this.form.submit()">
                               <option value="false">User Content</option>
                               <option value="true">Bot Content</option>
                               
                           </select>
                       </div>
               </div>
           </section>
           </form>
         </section>
       </section>
     <section class="section-wrapper">
       <h2 class="pocket-heading">Recommended docs:</h2>
       <a class="link" href=#>Learn more</a>
       <div class="card-wrapper">
         <div class="card">
           <img class="card-image" src="" alt="">
           <div class="card-description">
             <h3 class="card-site">spaffel.de</h3>
             <a class="card-link" href="http://spaffel.de/list">Alle Datein<span></span></a>
             <p class="card-text">Hier findest du eine Liste mit allen Datein (Die Schulcloud)</p>

           </div>
         </div>

         <div class="card">
           <img class="card-image" src="" alt="">
           <div class="card-description">
             <h3 class="card-site">spaffel.de</h3>
             <a class="card-link" href="http://spaffel.de/privatlist">Privater Ordner<span></span></a>
             <p class="card-text">Hier findest du Datein, die nur du sehen kannst.</p>
           </div>
         </div>

         <div class="card">
           <img class="card-image" src="" alt="">
           <div class="card-description">
             <h3 class="card-site">spaffel.de</h3>
             <a class="card-link" href=http://spaffel.de/upload>Datei-Upload<span></span></a>
             <p class="card-text">Hier kannst du Datein hochladen.</p>
           </div>
         </div>


       </div>
     </section>


<center>A Project started by Bjarne D. and Calvin Erfmann. Thanks to all the People that Support Search-Cord <3</center> 
   </body>
   </html>


       




    """

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS




@app.route('/search', methods=['GET', 'POST'])
def newliste():
    countup()
    if request.method == 'POST':
        
        preselect1 = """
        <script>
        
  var selId = document.getElementById("fach");
       selId.value = '"""
        preselect2 = request.form["Fach"]
        preselect3 ="';   </script>"
        preselect = f'{preselect1}{preselect2}{preselect3}'
        seite = '''
                
       <!DOCTYPE html>
       <html>
       <head>
         <style>
           a.fill-div {
           display: block;
           height: 100%;
           width: 100%;
           text-decoration: none;
       }
       * {
         margin: 0;
         padding: 0;
         box-sizing: border-box;
         /*border: 1px solid red;*/
       }

       .suchpart {
         display: flex;
         flex-direction: column;
         align-items: center;
         background-color: #f9f9fb;
         padding: 30px;
         font-family: Segoe UI, sans-serif;
       }

       .logo-and-brand {
         display: flex;
         align-items: center;
         justify-content: center;
         gap: 10px;
         width: 80%;
         margin: 40px 0;
       }

       .firefox-logo {
         width: 80px;
         height: auto;
       }

       .brand {
         font-size: 46px;
       }

       .search-wrapper {
         background-color: rgba(249, 249, 249, 0.95);
         width: 100%;
         height: 100px;
         padding: 25px 0;
         margin-bottom: 50px;
         position: sticky;
         top: 0;
         z-index: 1;
       }

       form {
         width: 720px;
         position: relative;
         margin: auto;
       }

       .ddg-logo {
         width: 25px;
         position: absolute;
         top: 11px;
         left: 15px;
       }

       .search-bar {
         width: 100%;
         padding: 15px;
         padding-left: 50px;
         height: 50px;


         border-radius:  8px 0 0 8px  ;
         box-shadow: 0 2px 6px rgba(58, 57, 68, 0.2);
         border: none;
         font-size: 15px;
       }


       .search-bar::placeholder {
         color: #000;
         opacity: 0.5;
       }

       .search-bar:focus {
         outline: 1px solid #ffffff;
       }

       .section-wrapper {
         width: 966px;
         padding: 10px;
       }

       .pocket-heading {
         display: inline;
         font-size: 17px;
         margin-right: 10px;
       }

       .link {
         text-decoration: none;
         color: #0060DF;
         font-size: 13px;
       }

       .link:hover {
         text-decoration: underline;
       }

       .card-wrapper {
         margin: 20px 0;
         display: grid;
         grid-template-columns: repeat(3, 1fr);
         grid-template-rows: repeat(4, 350px);
         grid-gap: 24px;
       }

       .search-result {
         max-width: 900px;

         background-color: #FFF;
         border-radius: 8px;
         box-shadow: 0 2px 6px rgba(58, 57, 68, 0.2);
         position: relative;
         border: none;
           padding: 15px 20px 20px 20px;

           width: 100%;
         padding: 15px;
         padding-left: 50px;
         width:80vh;
         border-radius: 8px;
         box-shadow: 0 2px 6px rgba(58, 57, 68, 0.2);
         border: none;
         font-size: 15px;

       }

       span {
         position: absolute;
         top: 0;
         left: 0;
         width: 100%;
         height: 100%;
       }



       body{
           display: flex;
         flex-direction: column;
         align-items: center;
         background-color: #f9f9fb;
         padding: 30px;
         font-family: Segoe UI, sans-serif;
       }
       .ibox-content {

           color: inherit;
           padding: 15px 20px 20px 20px;
           border-color: #E7EAEC;
           border-image: none;
           border-style: solid solid none;
           border-width: 1px 0px;
       }

       .search-form {
           margin-top: 10px;
           box-shadow: 0 2px 6px rgba(58, 57, 68, 0.2);

       }

       .search-result h3 {
           margin-bottom: 0;
           color: #1E0FBE;
       }

       .search-result .search-link {
           color: #006621;
       }

       .search-result p {
           font-size: 12px;
           margin-top: 5px;
       }

       .hr-line-dashed {
           border-top: 1px dashed #E7EAEC;
           color: #ffffff;
           background-color: #ffffff;
           height: 1px;
           margin: 20px 0;
       }

       h2 {
           font-size: 24px;
           font-weight: 100;
       }

   .button {
       position: fixed;
     right: 1rem;
     bottom: 1rem;
     min-width: 300px;
     min-height: 60px;
     font-family: 'Nunito', sans-serif;
     font-size: 22px;
     text-transform: uppercase;
     letter-spacing: 1.3px;
     font-weight: 700;
     color: #313133;
     background: #4FD1C5;
   background: linear-gradient(90deg, rgba(129,230,217,1) 0%, rgba(79,209,197,1) 100%);
     border: none;
     border-radius: 1000px;
     box-shadow: 12px 12px 24px rgba(79,209,197,.64);
     transition: all 0.3s ease-in-out 0s;
     cursor: pointer;
     outline: none;

     padding: 10px;
     }

   button::before {
   content: '';
     border-radius: 1000px;
     min-width: calc(300px + 12px);
     min-height: calc(60px + 12px);
     border: 6px solid #00FFCB;
     box-shadow: 0 0 60px rgba(0,255,203,.64);
     position: absolute;
     top: 50%;
     left: 50%;
     transform: translate(-50%, -50%);
     opacity: 0;
     transition: all .3s ease-in-out 0s;
   }

   .button:hover, .button:focus {
     color: #313133;
     transform: translateY(-6px);
   }

   button:hover::before, button:focus::before {
     opacity: 1;
   }

   button::after {
     content: '';
     width: 30px; height: 30px;
     border-radius: 100%;
     border: 6px solid #00FFCB;
     position: absolute;
     z-index: -1;
     top: 50%;
     left: 50%;
     transform: translate(-50%, -50%);
     animation: ring 1.5s infinite;
   }

   button:hover::after, button:focus::after {
     animation: none;
     display: none;
   }

   @keyframes ring {
     0% {
       width: 30px;
       height: 30px;
       opacity: 1;
     }
     100% {
       width: 300px;
       height: 300px;
       opacity: 0;
     }
   }

   select {
      -webkit-appearance:none;
      -moz-appearance:none;
      -ms-appearance:none;
      appearance:none;
      outline:0;
      box-shadow:none;
      border:0!important;
      border-radius:  0 8px 8px 0   ;
      background: #ffffff;
      background-image: none;
      flex: 1;
      padding: 0 .5em;
      color:rgb(0, 0, 0);
      cursor:pointer;
      font-size: 1em;
      font-family: 'Open Sans', sans-serif;

   }
   select::-ms-expand {
      display: none;
   }
   .select {
      position: relative;
      display: flex;
      width: 10em;

      height: 50px;
      line-height: 3;
      background: #ffffff;
      overflow: hidden;

      border-radius:  0 8px 8px 0   ;
      box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
   }
   .select::after {
      content: '▼';
      position: absolute;
      top: 0;
      right: 0;
      padding: 0 1em;
      background:  #ffffff;
      cursor:pointer;
      pointer-events:none;
      transition:.25s all ease;
      border-bottom-left-radius:-1px;
      height: 50px;
   }
   .select:hover::after {
      color: #23b499;
   }




   .float-child2 {
       width: 10%;
       float: left;
       padding: 0px;

   }
   .float-child {
       width: 75%;
       float: left;
       padding: 0px;

   }

       a.fill-div {
       display: block;
       height: 100%;
       width: 100%;
       text-decoration: none;
   }
   * {
     margin: 0;
     padding: 0;
     box-sizing: border-box;
     /*border: 1px solid red;*/
   }

   .section-wrapper {
     width: 966px;
     padding: 10px;
   }

   .pocket-heading {
     display: inline;
     font-size: 17px;
     margin-right: 10px;
   }

   .link {
     text-decoration: none;
     color: #0060DF;
     font-size: 13px;
   }

   .link:hover {
     text-decoration: underline;
   }

   .card-wrapper {
     margin: 20px 0;
     display: grid;
     grid-template-columns: repeat(3, 1fr);
     grid-template-rows: repeat(4, 350px);
     grid-gap: 24px;
   }

   .card {
     max-width: 300px;
     background-color: #FFF;
     border-radius: 8px;
     box-shadow: 0 2px 6px rgba(58, 57, 68, 0.2);
     position: relative;
   }

   span {
     position: absolute;
     top: 0;
     left: 0;
     width: 100%;
     height: 100%;
   }

   .card-image {
     width: 100%;
     border-radius: 8px 8px 0 0;
   }

   .card-description {
     padding: 15px;
   }

   .card-site {
     font-size: 16px;
     color: #777;
     font-weight: normal;
     margin-bottom: 10px;
   }

   .card-link {
     text-decoration: none;
     color: #000;
     font-weight: bold;
   }

   .card-link:hover {
     color: #0060DF;
   }

   .card-text {
     font-size: 14px;
     margin-top: 5px;
   }

   footer {
     display: flex;
     justify-content: space-between;
   }

   footer ul {
     display: flex;
     flex-wrap: wrap;
     list-style: none;
     gap: 10px;
     font-size: 14px;
   }

   @media (max-width: 1100px) {
     form {
       width: 600px;
     }

     .section-wrapper {
       width: 726px;
     }

     footer ul,
     footer .link {
       font-size: 10px;
     }
   }

   @media (max-width: 900px) {
     form {
       width: 360px;
     }

     .section-wrapper {
       width: 490px;
     }

     .card-wrapper {
       grid-template-columns: repeat(2, 1fr);
     }
   }

   @media (max-width: 600px) {
     form {
       width: 200px;
     }

     .section-wrapper {
       width: 246px;
     }

     .card-wrapper {
       grid-template-columns: 1fr;
     }
   }
   body {
     display: flex;
     flex-direction: column;
     align-items: center;
     background-color: #f9f9fb;
     padding: 30px;
     font-family: Segoe UI, sans-serif;
   }

   .logo-and-brand {
     display: flex;
     align-items: center;
     justify-content: center;
     gap: 10px;
     width: 80%;
     margin: 40px 0;
   }

   .firefox-logo {
     width: 80px;
     height: auto;
   }

   .brand {
     font-size: 46px;
   }

         </style>
         <meta charset="utf-8">
         <meta name="viewport" content="width=device-width, initial-scale=1">
         <title>Search-Cord</title>

       </head>
       <body>

       <section class="suchpart">
         <section class="logo-and-brand">
           <img
             class="firefox-logo"
             src="https://search-cord.com/uploads/3543843868965spaffel_sad_transpa22.png"
             alt="Cloud-logo">
           <a href="/" style="text-decoration: none; color: black;"><h1 class="brand">Search-Cord</h1></a>
         </section>
         <section class="search-wrapper">
           <form action="/search" method=post enctype=multipart/form-data class="float-container">
             <img
               class="ddg-logo"
               src="https://search-cord.com/uploads/329190864793search_icon_152764.png"
               alt="ddg-logo">
           <section class="float-container2">
               <div class="float-child">
             <input
               class="search-bar"
               type="text"

               name = "Suche"
               placeholder="Search in archived messages....">
               </div>
                   <div class="float-child2">
                       <div class="select">

                           <select id="fach" name="Fach" onchange="this.form.submit()">
                               <option value="false">User Content</option>
                               <option value="true">Bot Content</option>
                               
                           </select>
                       </div>
               </div>
           </section>
           </form>
         </section>
       </section>
    <div class="ergebnispart"></div>

 

      <div class="container bootstrap snippets bootdey">
        <div class="row">
            <div class="col-lg-12">
                <div class="ibox float-e-margins">
                    <div class="ibox-content">
    
            '''

    suche = request.form["Suche"]

    searchcountup()
    d


    search_parameters = {
  'q'         : suche,
  'query_by'  : 'message',
  'sort_by'   : '_text_match(buckets: 10):desc,timestamp:desc',
  'per_page': 100,
  'page': 1
}

    cursor =client.collections['messages'].documents.search(search_parameters)
    print(cursor['search_time_ms'])

    #filesdb = db.messages
    #cursor = list(filesdb.find())
    #cursor.reverse()
    
    #suche = suche.replace("+", " ")
    #print(suche)
    #cloudergs = 0
    print(request.form)
    seite+= f'Search Time: {cursor["search_time_ms"]}ms'
    for item in cursor["hits"]:
      
      #print(item["document"]["message"])
       # append = "no"

      print(item)
      if str(request.form["Fach"]).lower() == str(item["document"]["bot"]).lower():
        
        
        
        
            
         
        seite+= '<div class="hr-line-dashed"></div> <div class="search-result">'
        seite+=f'<h3><a target="_blank" href="https://search-cord.com/getcontext/{item["document"]["messageid"]}">{item["document"]["username"]}</a></h3>'
        ts = item["document"]["timestamp"]
        ts /= 1000
        zeito = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        seite+=f'<a target="_blank" href="https://search-cord.com/getcontext/{item["document"]["messageid"]}">|  | {zeito} </a>'
        seite+=f'<p>{item["document"]["message"]}</p>'
        seite+= '</div>'
        #cloudergs+= 1


        
      #print(item)


    
    seite+= preselect
    seite+= '''
            
            
                                </div>

                    

                    
                    
                </div>
            </div>
        </div>
    </div>
</div>
                    
<center>A Project started by Bjarne D. and Calvin Erfmann. Thanks to all the People that Support Search-Cord <3</center> 

</body>
</html>
            
            '''
    return f'{seite} '
    #return cursor





@app.route('/getcontext/<messageid>', methods=['GET', 'POST'])
def getcontext(messageid):
  countup()
  countupcont()





 
  seite = '''
                
       <!DOCTYPE html>
       <html>
       <head>
         <style>
           a.fill-div {
           display: block;
           height: 100%;
           width: 100%;
           text-decoration: none;
       }
       * {
         margin: 0;
         padding: 0;
         box-sizing: border-box;
         /*border: 1px solid red;*/
       }

       .suchpart {
         display: flex;
         flex-direction: column;
         align-items: center;
         background-color: #f9f9fb;
         padding: 30px;
         font-family: Segoe UI, sans-serif;
       }

       .logo-and-brand {
         display: flex;
         align-items: center;
         justify-content: center;
         gap: 10px;
         width: 80%;
         margin: 40px 0;
       }

       .firefox-logo {
         width: 80px;
         height: auto;
       }

       .brand {
         font-size: 46px;
       }

       .search-wrapper {
         background-color: rgba(249, 249, 249, 0.95);
         width: 100%;
         height: 100px;
         padding: 25px 0;
         margin-bottom: 50px;
         position: sticky;
         top: 0;
         z-index: 1;
       }

       form {
         width: 720px;
         position: relative;
         margin: auto;
       }

       .ddg-logo {
         width: 25px;
         position: absolute;
         top: 11px;
         left: 15px;
       }

       .search-bar {
         width: 100%;
         padding: 15px;
         padding-left: 50px;
         height: 50px;


         border-radius:  8px 0 0 8px  ;
         box-shadow: 0 2px 6px rgba(58, 57, 68, 0.2);
         border: none;
         font-size: 15px;
       }


       .search-bar::placeholder {
         color: #000;
         opacity: 0.5;
       }

       .search-bar:focus {
         outline: 1px solid #ffffff;
       }

       .section-wrapper {
         width: 966px;
         padding: 10px;
       }

       .pocket-heading {
         display: inline;
         font-size: 17px;
         margin-right: 10px;
       }

       .link {
         text-decoration: none;
         color: #0060DF;
         font-size: 13px;
       }

       .link:hover {
         text-decoration: underline;
       }

       .card-wrapper {
         margin: 20px 0;
         display: grid;
         grid-template-columns: repeat(3, 1fr);
         grid-template-rows: repeat(4, 350px);
         grid-gap: 24px;
       }

       .search-result {
         max-width: 900px;

         background-color: #FFF;
         border-radius: 8px;
         box-shadow: 0 2px 6px rgba(58, 57, 68, 0.2);
         position: relative;
         border: none;
           padding: 15px 20px 20px 20px;

           width: 100%;
         padding: 15px;
         padding-left: 50px;
         width:80vh;
         border-radius: 8px;
         box-shadow: 0 2px 6px rgba(58, 57, 68, 0.2);
         border: none;
         font-size: 15px;

       }

       span {
         position: absolute;
         top: 0;
         left: 0;
         width: 100%;
         height: 100%;
       }



       body{
           display: flex;
         flex-direction: column;
         align-items: center;
         background-color: #f9f9fb;
         padding: 30px;
         font-family: Segoe UI, sans-serif;
       }
       .ibox-content {

           color: inherit;
           padding: 15px 20px 20px 20px;
           border-color: #E7EAEC;
           border-image: none;
           border-style: solid solid none;
           border-width: 1px 0px;
       }

       .search-form {
           margin-top: 10px;
           box-shadow: 0 2px 6px rgba(58, 57, 68, 0.2);

       }

       .search-result h3 {
           margin-bottom: 0;
           color: #1E0FBE;
       }

       .search-result .search-link {
           color: #006621;
       }

       .search-result p {
           font-size: 12px;
           margin-top: 5px;
       }

       .hr-line-dashed {
           border-top: 1px dashed #E7EAEC;
           color: #ffffff;
           background-color: #ffffff;
           height: 1px;
           margin: 20px 0;
       }

       h2 {
           font-size: 24px;
           font-weight: 100;
       }

   .button {
       position: fixed;
     right: 1rem;
     bottom: 1rem;
     min-width: 300px;
     min-height: 60px;
     font-family: 'Nunito', sans-serif;
     font-size: 22px;
     text-transform: uppercase;
     letter-spacing: 1.3px;
     font-weight: 700;
     color: #313133;
     background: #4FD1C5;
   background: linear-gradient(90deg, rgba(129,230,217,1) 0%, rgba(79,209,197,1) 100%);
     border: none;
     border-radius: 1000px;
     box-shadow: 12px 12px 24px rgba(79,209,197,.64);
     transition: all 0.3s ease-in-out 0s;
     cursor: pointer;
     outline: none;

     padding: 10px;
     }

   button::before {
   content: '';
     border-radius: 1000px;
     min-width: calc(300px + 12px);
     min-height: calc(60px + 12px);
     border: 6px solid #00FFCB;
     box-shadow: 0 0 60px rgba(0,255,203,.64);
     position: absolute;
     top: 50%;
     left: 50%;
     transform: translate(-50%, -50%);
     opacity: 0;
     transition: all .3s ease-in-out 0s;
   }

   .button:hover, .button:focus {
     color: #313133;
     transform: translateY(-6px);
   }

   button:hover::before, button:focus::before {
     opacity: 1;
   }

   button::after {
     content: '';
     width: 30px; height: 30px;
     border-radius: 100%;
     border: 6px solid #00FFCB;
     position: absolute;
     z-index: -1;
     top: 50%;
     left: 50%;
     transform: translate(-50%, -50%);
     animation: ring 1.5s infinite;
   }

   button:hover::after, button:focus::after {
     animation: none;
     display: none;
   }

   @keyframes ring {
     0% {
       width: 30px;
       height: 30px;
       opacity: 1;
     }
     100% {
       width: 300px;
       height: 300px;
       opacity: 0;
     }
   }

   select {
      -webkit-appearance:none;
      -moz-appearance:none;
      -ms-appearance:none;
      appearance:none;
      outline:0;
      box-shadow:none;
      border:0!important;
      border-radius:  0 8px 8px 0   ;
      background: #ffffff;
      background-image: none;
      flex: 1;
      padding: 0 .5em;
      color:rgb(0, 0, 0);
      cursor:pointer;
      font-size: 1em;
      font-family: 'Open Sans', sans-serif;

   }
   select::-ms-expand {
      display: none;
   }
   .select {
      position: relative;
      display: flex;
      width: 10em;

      height: 50px;
      line-height: 3;
      background: #ffffff;
      overflow: hidden;

      border-radius:  0 8px 8px 0   ;
      box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
   }
   .select::after {
      content: '▼';
      position: absolute;
      top: 0;
      right: 0;
      padding: 0 1em;
      background:  #ffffff;
      cursor:pointer;
      pointer-events:none;
      transition:.25s all ease;
      border-bottom-left-radius:-1px;
      height: 50px;
   }
   .select:hover::after {
      color: #23b499;
   }




   .float-child2 {
       width: 10%;
       float: left;
       padding: 0px;

   }
   .float-child {
       width: 75%;
       float: left;
       padding: 0px;

   }

       a.fill-div {
       display: block;
       height: 100%;
       width: 100%;
       text-decoration: none;
   }
   * {
     margin: 0;
     padding: 0;
     box-sizing: border-box;
     /*border: 1px solid red;*/
   }

   .section-wrapper {
     width: 966px;
     padding: 10px;
   }

   .pocket-heading {
     display: inline;
     font-size: 17px;
     margin-right: 10px;
   }

   .link {
     text-decoration: none;
     color: #0060DF;
     font-size: 13px;
   }

   .link:hover {
     text-decoration: underline;
   }

   .card-wrapper {
     margin: 20px 0;
     display: grid;
     grid-template-columns: repeat(3, 1fr);
     grid-template-rows: repeat(4, 350px);
     grid-gap: 24px;
   }

   .card {
     max-width: 300px;
     background-color: #FFF;
     border-radius: 8px;
     box-shadow: 0 2px 6px rgba(58, 57, 68, 0.2);
     position: relative;
   }

   span {
     position: absolute;
     top: 0;
     left: 0;
     width: 100%;
     height: 100%;
   }

   .card-image {
     width: 100%;
     border-radius: 8px 8px 0 0;
   }

   .card-description {
     padding: 15px;
   }

   .card-site {
     font-size: 16px;
     color: #777;
     font-weight: normal;
     margin-bottom: 10px;
   }

   .card-link {
     text-decoration: none;
     color: #000;
     font-weight: bold;
   }

   .card-link:hover {
     color: #0060DF;
   }

   .card-text {
     font-size: 14px;
     margin-top: 5px;
   }

   footer {
     display: flex;
     justify-content: space-between;
   }

   footer ul {
     display: flex;
     flex-wrap: wrap;
     list-style: none;
     gap: 10px;
     font-size: 14px;
   }

   @media (max-width: 1100px) {
     form {
       width: 600px;
     }

     .section-wrapper {
       width: 726px;
     }

     footer ul,
     footer .link {
       font-size: 10px;
     }
   }

   @media (max-width: 900px) {
     form {
       width: 360px;
     }

     .section-wrapper {
       width: 490px;
     }

     .card-wrapper {
       grid-template-columns: repeat(2, 1fr);
     }
   }

   @media (max-width: 600px) {
     form {
       width: 200px;
     }

     .section-wrapper {
       width: 246px;
     }

     .card-wrapper {
       grid-template-columns: 1fr;
     }
   }
   body {
     display: flex;
     flex-direction: column;
     align-items: center;
     background-color: #f9f9fb;
     padding: 30px;
     font-family: Segoe UI, sans-serif;
   }

   .logo-and-brand {
     display: flex;
     align-items: center;
     justify-content: center;
     gap: 10px;
     width: 80%;
     margin: 40px 0;
   }

   .firefox-logo {
     width: 80px;
     height: auto;
   }

   .brand {
     font-size: 46px;
   }

         </style>
         <meta charset="utf-8">
         <meta name="viewport" content="width=device-width, initial-scale=1">
         <title>Search-Cord</title>

       </head>
       <body>

       <section class="suchpart">
         <section class="logo-and-brand">
           <img
             class="firefox-logo"
             src="https://search-cord.com/uploads/3543843868965spaffel_sad_transpa22.png"
             alt="Cloud-logo">
           <a href="/" style="text-decoration: none; color: black;"><h1 class="brand">Search-Cord</h1></a>
         </section>
         <section class="search-wrapper">
           <form action="/search" method=post enctype=multipart/form-data class="float-container">
             <img
               class="ddg-logo"
               src="https://search-cord.com/uploads/329190864793search_icon_152764.png"
               alt="ddg-logo">
           <section class="float-container2">
               <div class="float-child">
             <input
               class="search-bar"
               type="text"

               name = "Suche"
               placeholder="Search in archived messages....">
               </div>
                   <div class="float-child2">
                       <div class="select">

                           <select id="fach" name="Fach" onchange="this.form.submit()">
                               <option value="false">User Content</option>
                               <option value="true">Bot Content</option>
                               
                           </select>
                       </div>
               </div>
           </section>
           </form>
         </section>
       </section>
    <div class="ergebnispart"></div>

 

      <div class="container bootstrap snippets bootdey">
        <div class="row">
            <div class="col-lg-12">
                <div class="ibox float-e-margins">
                    <div class="ibox-content">
    
            '''


  likes = db.messages
  likesbyuser = likes.find_one({"id": messageid})
  
  currenntimestamp = likesbyuser["createdTimestamp"]

  before = currenntimestamp 
  after = currenntimestamp + 3600000

  messagedb = db.messages
 
  test = messagedb.find(
{ "createdTimestamp": {

  "$gt": before,
  "$lt": after }
} 
)

  seite+= '<div class="hr-line-dashed"></div> <div class="search-result">'
  username = 'un'
  username = likesbyuser["username"]
  seite+=f'<h3><a target="_blank" href="https://search-cord.com/getcontext/{likesbyuser["id"]}">{username}</a></h3>'
  ts = likesbyuser["createdTimestamp"]
  ts /= 1000
  zeito = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
  seite+=f'<a target="_blank" href="https://search-cord.com/getcontext/{likesbyuser["id"]}">|  | {zeito} </a>'
  seite+=f'<p>{likesbyuser["cleanContent"]}</p>'
  seite+= '</div>'
  seite+= '<center><h3>Responses to this Message (up to 2hour later):</h3> </center>'
  liste = list(test)
  liste.reverse()
  
  for item in liste:
    
    if item["channelId"] == likesbyuser["channelId"]:
      #seite+='--------------------------'
      #seite += item["cleanContent"]
      #seite += '\n'
      
    #seite+= f'Messages 2 Hours After: "{likesbyuser["cleanContent"]}"'
  
      
      #print(item["document"]["message"])
       # append = "no"

    #print(item)
    
      
      
      
      
          
        
      seite+= '<div class="hr-line-dashed"></div> <div class="search-result">'
      username = 'un'
      username = item["username"]
      seite+=f'<h3><a target="_blank" href="https://search-cord.com/getcontext/{item["id"]}">{username}</a></h3>'
      ts = item["createdTimestamp"]
      ts /= 1000
      zeito = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
      seite+=f'<a target="_blank" href="https://search-cord.com/getcontext/{item["id"]}">|  | {zeito} </a>'
      seite+=f'<p>{item["cleanContent"]}</p>'
      seite+= '</div>'
      #cloudergs+= 1


      
    #print(item)


  
  seite+= '''
            
            
                                </div>

                    

                    
                    
                </div>
            </div>
        </div>
    </div>
</div>
                    
<center>A Project started by Bjarne D. and Calvin Erfmann. Thanks to all the People that Support Search-Cord <3</center> 

</body>
</html>
            
            '''
  return f'{seite} '
  


app.run(host='0.0.0.0', port='443', ssl_context=context)