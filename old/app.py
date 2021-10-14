from flask import Flask, request, render_template,  redirect, flash,  jsonify, session
from random import randint,  choice, sample
from flask_debugtoolbar import DebugToolbarExtension
from surveys import Survey, satisfaction_survey,surveys

app = Flask(__name__)

app.config['SECRET_KEY'] = "secret key"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

responses = []

@app.route('/')
def home_page():
  """Shows title, instructions and button to start survey"""
  title = satisfaction_survey.title
  instructions = satisfaction_survey.instructions

  return render_template('home.html', title=title, instructions=instructions)

@app.route('/start')
def start_survey():
  """ start the survey """
  responses = [] 
  return redirect("/questions/0")
  
@app.route('/questions/<int:num>')
def display_questions(num):
  """ Display the questions one after another """
  if (len(responses) == len(satisfaction_survey.questions)):
        # All questions answered
        return redirect("/finished")

  if num != len(responses):
    flash("Answering questions out of order", "error")
    question=satisfaction_survey.questions[len(responses)]
    return render_template('question_page.html',question_number=len(responses), question=question)
   
  question=satisfaction_survey.questions[num]

  return render_template('question_page.html',question_number=num, question=question)

@app.route('/answer', methods=["POST"])  
def answer_survey():
  """ gather the answers and append them to responses string """
  answer = request.form['answer']   
  res = responses.append(answer)
  lr =len(responses)
  if lr == len(satisfaction_survey.questions ):
    return redirect('/finished')
  else:
    return redirect(f"/questions/{lr}")

@app.route('/finished')
def finish_survey():
  """ when finished, display thank you screen  """
  return render_template('thank_you.html')

    

