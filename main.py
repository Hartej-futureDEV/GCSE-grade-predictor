from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

if __name__ == '__main__':
    app.run()

print("This is the GCSE and mock grade predictor.")
print("It will ask for your previous grades from mocks and school reports in Year 10 and Year 11.")
print("Just a reminder: nothing here is 100% accurate. It is merely a prediction.")
print("-------------------------------------------------------------------------------------")

def get_int_input(prompt): 
    while True:
        try:
            value = int(input(prompt))
            if value < 0:
                print("Please enter a non-negative number.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number.")

choice = int(input("What is the mock year prediction you want? Enter 10 for Year 10 or 11 for Year 11: "))

if choice == 11:
    print("Enter your grades for the subjects listed. If you haven't done one, enter 0.")

    mathsF = get_int_input("Maths Foundation (total of all papers): ")
    mathsH = get_int_input("Maths Higher (total of all papers): ")
    englishL = get_int_input("English Language total: ")
    englishLit = get_int_input("English Literature total: ")
    scienceF = get_int_input("Combined Science Foundation total (all papers combined): ")
    scienceH = get_int_input("Combined Science Higher total (all papers combined): ")
    biologyTriple = get_int_input("Biology Triple Science total: ")
    chemistryTriple = get_int_input("Chemistry Triple Science total: ")
    physicsTriple = get_int_input("Physics Triple Science total: ")
    history = get_int_input("History total: ")
    geography = get_int_input("Geography total: ")
    CS = get_int_input("Computer Science total (Paper 1 + 2): ")
    french = get_int_input("French total (all components): ")
    spanish = get_int_input("Spanish total (all components): ")
    german = get_int_input("German total (all components): ")

    # Maths Foundation
    if mathsF >= 186:
        print("Maths Foundation estimate: Grade 5 (max)")
    elif 157 <= mathsF < 186:
        print("Maths Foundation estimate: Grade 4-5")
    elif 117 <= mathsF < 157:
        print("Maths Foundation estimate: Grade 3-4")
    elif 77 <= mathsF < 117:
        print("Maths Foundation estimate: Grade 2-3")
    elif 37 <= mathsF < 77:
        print("Maths Foundation estimate: Grade 1-2")
    elif mathsF > 0:
        print("Maths Foundation estimate: Below Grade 1")

    # Maths Higher
    if mathsH >= 219:
        print("Maths Higher estimate: Grade 9")
    elif 191 <= mathsH < 219:
        print("Maths Higher estimate: Grade 8")
    elif 163 <= mathsH < 191:
        print("Maths Higher estimate: Grade 7")
    elif 129 <= mathsH < 163:
        print("Maths Higher estimate: Grade 6")
    elif 95 <= mathsH < 129:
        print("Maths Higher estimate: Grade 5")
    elif 61 <= mathsH < 95:
        print("Maths Higher estimate: Grade 4")
    elif 44 <= mathsH < 61:
        print("Maths Higher estimate: Grade 3")
    elif mathsH > 0:
        print("Maths Higher estimate: Below Grade 3")

    # English Language
    if englishL >= 138:
        print("English Language estimate: Grade 9")
    elif 125 <= englishL < 138:
        print("English Language estimate: Grade 8")
    elif 112 <= englishL < 125:
        print("English Language estimate: Grade 7")
    elif 102 <= englishL < 112:
        print("English Language estimate: Grade 6")
    elif 92 <= englishL < 102:
        print("English Language estimate: Grade 5")
    elif 82 <= englishL < 92:
        print("English Language estimate: Grade 4")
    elif 73 <= englishL < 82:
        print("English Language estimate: Grade 3")
    elif englishL > 0:
        print("English Language estimate: Below Grade 3")

    # English Literature
    if englishLit >= 137:
        print("English Literature estimate: Grade 9")
    elif 121 <= englishLit < 137:
        print("English Literature estimate: Grade 8")
    elif 106 <= englishLit < 121:
        print("English Literature estimate: Grade 7")
    elif 90 <= englishLit < 106:
        print("English Literature estimate: Grade 6")
    elif 74 <= englishLit < 90:
        print("English Literature estimate: Grade 5")
    elif 58 <= englishLit < 74:
        print("English Literature estimate: Grade 4")
    elif 42 <= englishLit < 58:
        print("English Literature estimate: Grade 3")
    elif 27 <= englishLit < 42:
        print("English Literature estimate: Grade 2")
    elif 12 <= englishLit < 27:
        print("English Literature estimate: Grade 1")
    elif englishLit > 0:
        print("English Literature estimate: Below Grade 1")

    # Combined Science Foundation
    if scienceF >= 234:
        print("Combined Science Foundation estimate: Grade 5")
    elif 204 <= scienceF < 234:
        print("Combined Science Foundation estimate: Grade 4")
    elif 174 <= scienceF < 204:
        print("Combined Science Foundation estimate: Grade 3")
    elif 144 <= scienceF < 174:
        print("Combined Science Foundation estimate: Grade 2")
    elif 114 <= scienceF < 144:
        print("Combined Science Foundation estimate: Grade 1")
    elif scienceF > 0:
        print("Combined Science Foundation estimate: Below Grade 1")

    # Combined Science Higher
    if scienceH >= 306:
        print("Combined Science Higher estimate: Grade 9")
    elif 270 <= scienceH < 306:
        print("Combined Science Higher estimate: Grade 8")
    elif 234 <= scienceH < 270:
        print("Combined Science Higher estimate: Grade 7")
    elif 198 <= scienceH < 234:
        print("Combined Science Higher estimate: Grade 6")
    elif 162 <= scienceH < 198:
        print("Combined Science Higher estimate: Grade 5")
    elif 126 <= scienceH < 162:
        print("Combined Science Higher estimate: Grade 4")
    elif 90 <= scienceH < 126:
        print("Combined Science Higher estimate: Grade 3")
    elif scienceH > 0:
        print("Combined Science Higher estimate: Below Grade 3")

    # Triple Sciences (B/C/P same boundaries)
    for subject, score in [("Biology", biologyTriple), ("Chemistry", chemistryTriple), ("Physics", physicsTriple)]:
        if score >= 180:
            grade = 9
        elif 160 <= score < 180:
            grade = 8
        elif 140 <= score < 160:
            grade = 7
        elif 120 <= score < 140:
            grade = 6
        elif 100 <= score < 120:
            grade = 5
        elif 80 <= score < 100:
            grade = 4
        elif 60 <= score < 80:
            grade = 3
        elif score > 0:
            grade = "Below Grade 3"
        else:
            grade = None

        if grade is not None:
            print(f"{subject} Triple Science estimate: Grade {grade}")

    # History
    if history >= 117:
        print("History estimate: Grade 9")
    elif 105 <= history < 117:
        print("History estimate: Grade 8")
    elif 93 <= history < 105:
        print("History estimate: Grade 7")
    elif 81 <= history < 93:
        print("History estimate: Grade 6")
    elif 69 <= history < 81:
        print("History estimate: Grade 5")
    elif 57 <= history < 69:
        print("History estimate: Grade 4")
    elif 40 <= history < 57:
        print("History estimate: Grade 3")
    elif 24 <= history < 40:
        print("History estimate: Grade 2")
    elif 8 <= history < 24:
        print("History estimate: Grade 1")
    elif history > 0:
        print("History estimate: Below Grade 1")

    # Geography
    if geography >= 202:
        print("Geography estimate: Grade 9")
    elif 182 <= geography < 202:
        print("Geography estimate: Grade 8")
    elif 162 <= geography < 182:
        print("Geography estimate: Grade 7")
    elif 142 <= geography < 162:
        print("Geography estimate: Grade 6")
    elif 123 <= geography < 142:
        print("Geography estimate: Grade 5")
    elif 104 <= geography < 123:
        print("Geography estimate: Grade 4")
    elif 76 <= geography < 104:
        print("Geography estimate: Grade 3")
    elif 48 <= geography < 76:
        print("Geography estimate: Grade 2")
    elif 20 <= geography < 48:
        print("Geography estimate: Grade 1")
    elif geography > 0:
        print("Geography estimate: Below Grade 1")

    # Computer Science
    if CS >= 144:
        print("Computer Science estimate: Grade 9")
    elif 128 <= CS < 144:
        print("Computer Science estimate: Grade 8")
    elif 112 <= CS < 128:
        print("Computer Science estimate: Grade 7")
    elif 96 <= CS < 112:
        print("Computer Science estimate: Grade 6")
    elif 80 <= CS < 96:
        print("Computer Science estimate: Grade 5")
    elif 64 <= CS < 80:
        print("Computer Science estimate: Grade 4")
    elif 48 <= CS < 64:
        print("Computer Science estimate: Grade 3")
    elif 32 <= CS < 48:
        print("Computer Science estimate: Grade 2")
    elif 16 <= CS < 32:
        print("Computer Science estimate: Grade 1")
    elif CS > 0:
        print("Computer Science estimate: Below Grade 1")

    # Languages (same boundaries used for French, Spanish, German Higher Tier)
    def predict_language(name, score):
        if score >= 200:
            print(f"{name} estimate: Grade 9")
        elif 180 <= score < 200:
            print(f"{name} estimate: Grade 8")
        elif 160 <= score < 180:
            print(f"{name} estimate: Grade 7")
        elif 140 <= score < 160:
            print(f"{name} estimate: Grade 6")
        elif 120 <= score < 140:
            print(f"{name} estimate: Grade 5")
        elif 100 <= score < 120:
            print(f"{name} estimate: Grade 4")
        elif 80 <= score < 100:
            print(f"{name} estimate: Grade 3")
        elif score > 0:
            print(f"{name} estimate: Below Grade 3")

    predict_language("French", french)
    predict_language("Spanish", spanish)
    predict_language("German", german)
