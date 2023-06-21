def score_grade(score):
    if score <= 50:
        return "F"
    
    elif score <= 55:
        return "D"
    
    elif score <= 60:
        return "C-"
    
    elif score <= 65:
        return "C"
    
    elif score <= 70:
        return "C+"
    
    elif score <= 75:
        return "B-"
    
    elif score <= 80:
        return "B"
    
    elif score <= 85:
        return "B+"
    
    elif score <= 90:
        return "A-"
    
    elif score <= 95:
        return "A"
    
    elif score <= 100:
        return "A+"
    
    else:
        return "N/A"
    
def grade_point(grade):
    if grade == "F":
        return 0
    
    elif grade == "D":
        return 1
    
    elif grade == "C-":
        return 1.5
    
    elif grade == "C":
        return 2
    
    elif grade == "C+":
        return 2.5
    
    elif grade == "B-":
        return 3
    
    elif grade == "B":
        return 3.5
    
    elif grade == "B+":
        return 4
    
    elif grade == "A-":
        return 4.5
    
    elif grade == "A":
        return 5
    
    elif grade == "A+":
        return 5.5
    
    else:
        return 0
