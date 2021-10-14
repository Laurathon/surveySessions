from flask import Flask, request, render_template,  redirect, flash,  jsonify, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import Survey, satisfaction_survey,surveys

app = Flask(__name__)

app.config['SECRET_KEY'] = "secret key"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

##responses = []
KEY = "responses"
SURVEY_KEY = 'current_survey'

@app.route('/begin')
def begin():
  """Shows title, instructions and button to start survey"""
  title = satisfaction_survey.title
  instructions = satisfaction_survey.instructions
  return render_template('home.html', title=title, instructions=instructions)

@app.route('/')
def home_page():
  """Shows title, instructions and button to start survey"""  
  survey_list =list(surveys.keys()) 
  return render_template('home.html',survey=survey_list)

@app.route('/chooseSurvey', methods=["POST"])    
def choose_survey():
  """get the survey user choose """
  survey_id = request.form['choose_survey']  
  survey = surveys[survey_id]
  session[SURVEY_KEY] = survey_id
  title =survey.title
  instructions = survey.instructions
  return render_template('begin.html', title=title, instructions=instructions,survey=survey)

 
@app.route('/start', methods =["POST"])
def start_survey():
  """ start the survey. Clear the responses session """
  session[KEY] =[]
  return redirect("/questions/0")
  
@app.route('/questions/<int:num>')
def display_questions(num):
  """ Display the questions one after another """
  responses =session.get(KEY)
  survey_code = session[SURVEY_KEY]
  survey = surveys[survey_code]

  if (len(responses) == len(survey.questions)):
        # All questions answered
        return redirect("/finished")

  if num != len(responses):
    ## questions not in order
    flash("Answering questions out of order", "error")
    question=survey.questions[len(responses)]
    return render_template('question_page.html',question_number=len(responses), question=question)
   
  question=survey.questions[num]

  return render_template('question_page.html',question_number=num, question=question)

@app.route('/answer', methods=["POST"])  
def answer_survey():
  """ gather the answers and append them to responses which goes into the session """
  answer = request.form['answer'] 
  responses = session[KEY]
  responses.append(answer)
  session[KEY] =responses
  lr =len(session[KEY])
  if lr == len(satisfaction_survey.questions ):
    return redirect('/finished')
  else:
    return redirect(f"/questions/{lr}")

@app.route('/finished')
def finish_survey():
  responses =session.get(KEY)
  survey_code = session[SURVEY_KEY]
  survey = surveys[survey_code]
  survey_questions=survey.questions
  """ when finished, display thank you screen  """
  return render_template('thank_you.html',questions=survey_questions, responses =responses)

    

