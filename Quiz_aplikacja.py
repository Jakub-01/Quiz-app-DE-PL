import tkinter 
from tkinter import simpledialog
from get_vocabulary import get_file
import pandas as pd
import pickle


#sourcing input data into two lists using predefined function
quest = get_file("PL-DE.xlsx",2)
answ = get_file("PL-DE.xlsx",1)
user_highscore = 0
user_name = None

#merging two input lists into one dataframe and radomizing the order
vocabulary_df = pd.DataFrame({'Question': quest, 'Answer': answ})
vocabulary_df = vocabulary_df.sample(frac=1).reset_index(drop=True)

#defining statistical variables
N = 0
score = 0
correct_answer_ratio = 0

#defining a function to begin the test
def begin_test():
    global user_name
    global user_highscore
    global user_name
    global question_label
    global answer_label
    global correct_answer
    global N
    global begin_next_button
    global check_answer_button
    global percentage
    
    #check if user name is provided and if not, ask for it.
    if user_name == None:
        user_name = simpledialog.askstring("Nazwa użytkownika", "Wprowadź swoje imię:")
        if user_name == "":
            user_name = "Gość"
        else:
            pass
    else:
        pass

    # try to open a pickle file with highscore data. If it doesn't exist, create one.
    try:
        with open('highscore_data.pickle', 'rb') as f:
            highscore_data = pickle.load(f)
    except FileNotFoundError:
        highscore_data = {}
    
    #check if user name is in the highscore data. If not, add it. 
    if user_name in highscore_data:
        user_highscore = highscore_data[user_name]['highscore']
    else:
        highscore_data[user_name] = {'highscore' : user_highscore} 
        with open('highscore_data.pickle', 'wb') as f:
            pickle.dump(highscore_data, f)

    #check if current socre is higher than user highscore. If so, update user highscore.
    if score > user_highscore:
        highscore_data[user_name]['highscore'] = score
        user_highscore = score
        with open('highscore_data.pickle', 'wb') as f:
            pickle.dump(highscore_data, f)
    else:
        pass

    #defining GUI elements
    answer.delete(0, 'end')
    begin_next_button.grid_remove()
    begin_next_button = tkinter.Button(window, text = 'Następne pytanie!', padx =30, pady=12, command = begin_test)
    begin_next_button.grid(row = 1, column = 0,columnspan=2)
    begin_next_button.config(state = 'disabled')
    check_answer_button.grid_remove()
    check_answer_button = tkinter.Button(window, text = "Sprawdź!",padx = 30, pady=12, command = check_answer)
    check_answer_button.grid(row = 5, column = 0, columnspan=2)
    check_answer_button.config(state = 'normal')
    N += 1
    question_label.grid_remove()
    answer_label.grid_remove()
    answer_label = tkinter.Label(window, text = "",wraplength=160)
    answer_label.grid(row = 6, column = 2, columnspan=1)
    #answer_label = tkinter.Label(window, text = "")
    question_list = vocabulary_df.at[N,'Question']
    correct_answer = vocabulary_df.at[N,'Answer'] 
    question_label = tkinter.Label(window, text = question_list, wraplength=160)
    question_label.grid(row = 2, column = 1,columnspan=1)
    N_indicator = tkinter.Label(window, text = N)
    N_indicator.grid(row = 7, column = 1)
    user_label.grid(row = 10, column = 0)
    user_highscore_label.grid(row = 11, column = 0)
    user_indicator = tkinter.Label(window, text = user_name)
    user_highscore_indicator = tkinter.Label(window, text = user_highscore)
    user_indicator.grid(row = 10, column = 1) 
    user_highscore_indicator.grid(row = 11, column = 1)
    

#defining a function to check user answer
def check_answer():
    global answer_label
    global correct_answer
    global score
    global correct_answer_ratio
    global percentage
    global check_answer_button 
    begin_next_button.config(state = 'normal')
    check_answer_button.grid_remove()
    percentage.grid_remove()
    answer_label.grid_remove()
    answer_label = tkinter.Label(window, text = correct_answer,wraplength=160)
    answer_label.grid(row = 6, column = 1, columnspan=2)
    user_answer = answer.get().split()
    #checking if user correctly transalted the word.
    check1 = all(user_answer[i] in correct_answer for i in range(len(user_answer)))
    #checking if user used correct article.
    for article in ["der","die","das"]:
        if article in correct_answer:
            if len(user_answer) > 1:
                check2 = True
                break
            else:
                check2 = False
                break       
        else:
            check2 = True
            break
    #checking if user provided any answer. 
    if len(user_answer) > 0:
        check3 = True
    else:
        check3 = False
    #checking if all three conditions are met. If so, user gets a point, if not, he doesn't, but he can still move on to the next question, by clicking "Następne pytanie!" button.       
    if all([check1,check2,check3]):
        score += 1
        check_answer_button = tkinter.Button(window, text = "Dobra odpowiedź!"
        ,padx =30, pady=12, bg = '#32CD32', fg = 'black' , command = check_answer)
        check_answer_button.grid(row = 5, column = 0, columnspan=2)
    else:
        check_answer_button = tkinter.Button(window, text = "Zła odpowiedź :("
        ,padx =30, pady=12, bg = 'red', fg = 'black' , command = check_answer)
        check_answer_button.grid(row = 5, column = 0, columnspan=2)

    #updating score and percentage of correct answers.
    score_indicator = tkinter.Label(window, text = score)
    score_indicator.grid(row = 8, column = 1)    
    correct_answer_ratio = (score/N) * 100
    correct_answer_ratio = "{:.2f}%".format(round(correct_answer_ratio,2))
    percentage = tkinter.Label(window, text = correct_answer_ratio)
    percentage.grid(row = 9, column = 1)
    answer.delete(0, 'end')
    check_answer_button.config(state = 'disabled')
    correctAnswerPrompt.grid(row = 6, column = 0)

#defining window    
window = tkinter.Tk()

#defining window title
window.title("Quiz - język niemiecki")

#defining GUI elements
welcome_message = tkinter.Label(window, text = "Quiz - 1000 niemieckich słówek")
translateRequest = tkinter.Label(window, text = "Przetłumacz:")
question_label = tkinter.Label(window, text = "")
answerPrompt = tkinter.Label(window, text = "Odpowiedź wpisz obok:")
answer = tkinter.Entry(window, width=25, borderwidth = 5)
begin_next_button = tkinter.Button(window, text = 'Zaczynajmy', padx =30, pady=12, command = begin_test)
correctAnswerPrompt = tkinter.Label(window, text = "Poprawna odpowiedź to:")
check_answer_button = tkinter.Button(window, text = "Sprawdź!",padx =30, pady=12, command = check_answer,state='disabled')
answer_label = tkinter.Label(window, text = " ",wraplength=160) 
N_label = tkinter.Label(window, text = "Ilość prób:")
score_indicator_label = tkinter.Label(window, text = "Twój wynik to:")
percentagePrompt = tkinter.Label(window, text = "% poprawnych odpowiedzi:")
N_indicator = tkinter.Label(window, text = N)
score_indicator = tkinter.Label(window, text = score)
percentage = tkinter.Label(window, text = correct_answer_ratio)
user_label = tkinter.Label(window, text = "Użytkownik:")
user_highscore_label = tkinter.Label(window, text = "Najlepszy wynik:")
user_indicator = tkinter.Label(window, text = user_name)
user_highscore_indicator = tkinter.Label(window, text = user_highscore)

#placing GUI elements on the grid
window.columnconfigure(0, minsize=170)
window.columnconfigure(1, minsize=170)
welcome_message.grid(row = 0, column = 0, columnspan=2)
translateRequest.grid(row = 2, column = 0)
question_label.grid(row = 2, column = 1, columnspan=1)
answerPrompt.grid(row = 3, column = 0)
answer.grid(row = 3, column = 1, columnspan=2)
begin_next_button.grid(row = 1, column = 0, columnspan=2)
check_answer_button.grid(row = 5, column = 0,columnspan=2)
#correctAnswerPrompt.grid(row = 6, column = 0)
answer_label.grid(row = 6, column = 1, columnspan=1)
N_label.grid(row = 7, column = 0)
score_indicator_label.grid(row = 8, column = 0)
percentagePrompt.grid(row = 9, column =0)
N_indicator.grid(row = 7, column = 1)
score_indicator.grid(row = 8, column = 1)
percentage.grid(row = 9, column = 1)
#user_indicator.grid(row = 10, column = 1) 
#user_highscore_indicator.grid(row = 11, column = 1)


#setting window size
window.geometry('350x320')

#running the window
window.mainloop()

