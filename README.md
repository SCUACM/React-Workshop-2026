# Backend: Introduction to Firebase

Learning how to use the Google's FireStore database to store infromation sent from your frontend through API calls.

---

## Prerequisites

1. Download the _main branch_ of this project as zip by clicking on the green `code` button and selecting `Download ZIP` (This branch will contain the final code for your reference!)
   1. If you're comfortable with Github, simply clone the repo and switch branches to this one
2. Select a folder you want the project to be in, then unpack the zip to get the contents in the folder
3. Open this folder in VSCode, you should see the `backend-26` and `ReactWorkshop` folders
4. Open the terminal in VSCode (`CTRL + ~`)
5. Install the npm packages for the frontend
   1. `cd ReactWorkshop`
   2. `npm install`
   3. `npm run dev` to confirm the frontend is loading (`ctrl + C` to stop running program)
6. Install the pip packages for the backend
   1. `cd ../backend-26` (cd `../` means "get out of the current folder")
   2. Create virtual env
      1. MacOS/Linux: `python3 -m venv venv`
      2. Windows: `py -m venv venv`
   3. Select the virtual environment
      1. MacOS/Linux: `source venv/bin/activate`
      2. Windows: `.\venv\Scripts\activate`
      3. It's correct when you see `(venv)` at the start of every termainal command
   4. `pip install -r requirements.txt`
   5. `python app.py` to confirm the backend is loading

---

## Getting Started With FireBase

### Create a Project

- Sign in to your _personal gmail_ (Do NOT use your SCU account, yet)
- Navigate to the FireBase [console](https://console.firebase.google.com)
- Create a new FireBase project
  - Name your project
  - You will be promped to opt-in or opt-out of:
    - Google Developer Program
    - Enabling Gemini in FireBase
    - Enabling Google Analytics
  - These are _optional_ and you will be able to run your code no matter what you choose
- _If you want to include your SCU email account in your project_
  - Gear Icon -> Users And Permissions -> Add Member -> <youremail> -> Owner -> Add Member

---

### Connect Your Project to Your Code

- Gear Icon -> Service Accounts -> Admin SDK Configuration Snippet -> Python
- Copy this into your app.py file

- OR copy here:

```py
import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("path/to/serviceAccountKey.json")
firebase_admin.initialize_app(cred)
```

- You can update the import line to include FireStore as so:

```py
import firebase_admin
from firebase_admin import credentials, firestore
```

### Create Your Servive Account Key (_SENSITIVE INFORMATION_)

- Generate New Private Key
  - Click on the 'file' icon in your downloads to find its location
  - Drag the newly downloaded file into your project folder
  - In app.py replace the `"path/to/serviceAccountKey.json"` with the filepath to your credentials. Following this tutorial, it would be `"credentials.json"` as long as the credetials is in your backend folder

- **Put your filename into a .gitignore**
  - If you do not have one already, create a .gitignore file
  - Take the name of your Service Account Key file and copy it into your .gitignore file
  - OR - Rename your Service Account Key file to credentials.json IF you are using our provided code
  - More information about [.gitignore](https://www.w3schools.com/git/git_ignore.asp)

---

### Create Your FireStore Database

- Navigate back to your FireBase project
- Navigate to 'FireStore Database'
- Create a database
  - When you are prompted, choose:
    - Edition: Standard Edition
    - Location: nam5 (United States)
    - Mode: Test Mode

- Create your first collection!
  - Name your collection 'clicker'
  - Create your document by naming the ID 'counter'
    - Usually, you would generate a random ID, but for the purposes of this workshop we will name it this
  - Create your first field 'current_value' as a int64 with value 0
  - Create your second field 'history' as an array
    - Delete the first field of the array so that it becomes empty

---

### Begin coding

- First, we are going to work in our app.py file to implement the following functions

1. Initialize the database

```py
db = firestore.client()
```

2. Import Flask

- Put this at the TOP of your file

- This is pretty important, but we don't have time to go over this now... you'll understand how this works during our next workshop about API's

```py
from flask import Flask, jsonify, request, send_from_directory
app = Flask(__name__, static_folder="../clicker/dist", static_url_path="/")
```

- You also need to import flask_cors, which is necessary because otherwise CORS will block your API calls for security reasons

```py
from flask_cors import CORS
CORS(app, origins=["http://localhost:5173"])
```

- When you run your React program, if the link you use is anything other than `http://localhost:5173` then you should change the line above and replace it with your link

3. Add a GET method for our history

```py
@app.route("/firebase/get" , methods=["GET"])
def firebase_get():
    db = firestore.client()
    doc = db.collection("clicker").document("counter").get()
    if doc.exists:
        return jsonify(doc.to_dict())
    return jsonify({"error": "Document not found"}), 404
```

4. Add a POST method for our history

```py
@app.route("/firebase/set", methods=["POST"])
def firebase_set():
    data = request.get_json()
    print("Received data for Firebase update:", data)
    db.collection("clicker").document("counter").set(data)
    return jsonify({"message": "Data updated successfully"}), 200
```

5. Last, make sure you have the closing statement for flask app to run

```py
if __name__ == "__main__":
    app.run(port=8080,debug=True)
```

- Second, we are going to work in the Counter.jsx file to tie these functions into our frontend

1. Begin by adding UseEffects to your import at the top of the file

   Our original line

   ```jsx
   import { useState } from "react";
   ```

   will become

   ```jsx
   import { useState, useEffect } from "react";
   ```

2. Update the Increment Function
   Our orignal function

```jsx
const increment = () => {
  const next = count + 1;
  setCount(next);
  setHistory([...history, next]);
};
```

will become

```jsx
const increment = () => {
  const next = count + 1;
  setCount(next);
  setHistory([...history, next]);
  fetch("http://127.0.0.1:8080/firebase/set", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      current_value: next,
      history: [...history, next],
    }),
  }).catch((err) => console.error("Failed to update firebase data:", err));
};
```

3. Update the Decrement Function
   Our original function

```jsx
const decrement = () => {
  const next = count - 1;
  setCount(next);
  setHistory([...history, next]);
};
```

will become

```jsx
const decrement = () => {
  const next = count - 1;
  setCount(next);
  setHistory([...history, next]);
  fetch("http://127.0.0.1:8080/firebase/set", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      current_value: next,
      history: [...history, next],
    }),
  }).catch((err) => console.error("Failed to update firebase data:", err));
};
```

---

### Running you code

- Running your code will be a bit more complicated than it was for running your frontend. Now that you have a backend, you're gonna need to run both at the same time! To do this, you will need two terminals.

1. Run your React Program

- Start by running your React Program like you were before!
  1. Open a new terminal and navigate to the `React-Workshop-2026\ReactWorkshop` folder using ls, cd, etc!
  2. Begin running your React app using the line `npm run dev`
  3. Note, you can stop running this program at any time using CTRL + C

2. Run your Backend

- This will be very similar to what we did before!
  1. Open a new terminal and navigate to the `React-Workshop-2026\backend` folder using ls, cd, etc!
  2. Begin running your React app using the line `python app.py`
  3. Note, you can stop running this program at any time using CTRL + C

---

And that's all we have for our workshop! Now, you should have a fully functional frontend, API calls, and backend, and most importantly, we were able to put them all together!

Happy Coding!
ACM
