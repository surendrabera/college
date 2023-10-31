from flask import Flask
from flask import render_template, request
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')


tatus_flag=False
flag_s=False
flag_c=False

app=Flask(__name__)
@app.route('/', methods=["GET","POST"])
def data():
    if request.method=="GET":
        return render_template('index.html')
    elif request.method=="POST":
        ##if user do not provide input
        if "ID" not in request.form or "id_value" not in request.form:
            return render_template("data.html",title='Something went wrong', heading='Wrong Inputs',something='something went wrong')
    
        #data source
        data=pd.read_csv("data.csv")

        ##input
        id=request.form['ID']
        id_value=int(request.form["id_value"])

        ##for student details
        if id=="student_id" and id_value in list(data['Student id']) :
          student_tabel=data[data['Student id']==id_value]
          total=student_tabel.iloc[:,2].sum()
          column_title_list=list(data.columns)
          student_tabel=student_tabel.values.tolist()
          return render_template("data.html",title='Student Data', heading='Students Details' ,data=student_tabel, total=total, column_title_list=column_title_list, status_flag=True, flag_s=True)
        
        ## for course details
        elif id=="course_id" and id_value in list(data[' Course id'] ):
            course_tabel=data[data[' Course id']==id_value]
            avg_marks=course_tabel.iloc[:,2].mean()
            max_marks=course_tabel.iloc[:,2].max()

            ## image
            hist_plot=plt.hist(course_tabel[' Marks'])
            plt.xlabel('Marks')
            plt.ylabel('frequency')
            plt.savefig('static/histogram.png')
            title_list=['Average Marks','Maximum Marks']
            data_tabel=[[avg_marks,max_marks]]
            return render_template("data.html",title='Course Data', heading='Course Details',data=data_tabel,column_title_list=title_list,image='static/histogram.png',status_flag=True,flag_c=True)
        
        ## eror massage
        else:
            return render_template("data.html",title='Something went wrong', heading='Wrong Inputs',something='something went wrong')


if __name__ =='__main__':
    app.debug=True
    app.run(port=8000)