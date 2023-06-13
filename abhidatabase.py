import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
import tkinter as tk
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https:/"
})
ref=db.reference('Students')
def submit_data():
    roll_number = roll_entry.get()
    name = name_entry.get()
    age = age_entry.get()
    branch = branch_entry.get()
    year = year_entry.get()
    attendance = attendance_entry.get()
    last=time_entry.get()

    data[roll_number] = {
        'Name': name,
        'Age': age,
        'Branch': branch,
        'Year': year,
        'Attendance': attendance,
        'last_attendance_time':last
    }

    # Clear input fields
    roll_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    branch_entry.delete(0, tk.END)
    year_entry.delete(0, tk.END)
    attendance_entry.delete(0, tk.END)

def display_data():
    print(data)

data = {}

window = tk.Tk()
window.title("Student Details")
window.geometry("400x300")

# Roll Number
roll_label = tk.Label(window, text="Roll Number:")
roll_label.pack()
roll_entry = tk.Entry(window)
roll_entry.pack()

# Name
name_label = tk.Label(window, text="Name:")
name_label.pack()
name_entry = tk.Entry(window)
name_entry.pack()

# Age
age_label = tk.Label(window, text="Age:")
age_label.pack()
age_entry = tk.Entry(window)
age_entry.pack()

# Branch
branch_label = tk.Label(window, text="Branch:")
branch_label.pack()
branch_entry = tk.Entry(window)
branch_entry.pack()

# Year
year_label = tk.Label(window, text="Year:")
year_label.pack()
year_entry = tk.Entry(window)
year_entry.pack()

time_label = tk.Label(window, text="Last time attendance:")
time_label.pack()
time_entry = tk.Entry(window)
time_entry.pack()

# Attendance
attendance_label = tk.Label(window, text="Attendance:")
attendance_label.pack()
attendance_entry = tk.Entry(window)
attendance_entry.pack()

# Submit Button
submit_button = tk.Button(window, text="Submit", command=submit_data)
submit_button.pack()

# Display Button
display_button = tk.Button(window, text="Display Data", command=display_data)
display_button.pack()

window.mainloop()

data={
    '1':{
        'name':'Abhinai',
        'age':'19',
        'branch':"CSE",
        'year':'2',

        'last_attendance':'2023-12-06 00:54:34',
        'attendace':0

    },
    '2':{
        'name':'elon',
        'age':'20',
        'branch':"Mechanical",
        'year':'3',
        'attendace':0,
        'last_attendance':'2023-12-06 00:54:34'

    },
    '3':{
        'name':'Priyanka',
        'age':'20',
        'branch':"IT",
        'year':'2',
        'attendace':0,
        'last_attendance':'2023-12-06 00:54:34'

    }
}
for k,v in data.items():
    ref.child(k).set(v)