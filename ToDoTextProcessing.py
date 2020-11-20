import todostorage, textProcessing, datetime
#File = todostorage.toDoRead()
#print(File)
def chatbotread(command):
    chatbotkeys = ["what", "who", "get", "grab", "show", ]
    keysNotStart = ["free", "not started"]
    inProgress = ["in progress"]
    CompletedTasks = ["completed", "done"]
    notCompleted = [""]
    ChatbotFile = ""
    if (textProcessing.inArray(chatbotkeys, command)):#Bens FUNCTION
        file = todostorage.toDoRead()
        if textProcessing.inArray(CompletedTasks,command):
            for i in range(0,len(file)):
                if file[i]["Completed"].lower() == "completed":
                    ChatbotFile = ChatbotFile + "TaskId: " + file[i]["TaskID"] + " Task: " + file[i]["Task"] + " DateStart: " + file[i]["DateStart"] + " DateDue: " + file[i]["DateDue"] + " User: " +  file[i]["User"] + " Completed: " + file[i]["Completed"]+ " TaskDifficulty: " + file[i]["TaskDifficulty"] +"\n"
        elif textProcessing.inArray(inProgress,command):
            for i in range(0,len(file)):
                if file[i]["Completed"] == "in progress":
                    ChatbotFile = ChatbotFile + "TaskId: " + file[i]["TaskID"] + " Task: " + file[i]["Task"] + " DateStart: " + file[i]["DateStart"] + " DateDue: " + file[i]["DateDue"] + " User: " +  file[i]["User"] + " Completed: " + file[i]["Completed"]+ " TaskDifficulty: " + file[i]["TaskDifficulty"] +"\n"
        elif textProcessing.inArray(notCompleted,command):
            for i in range(0,len(file)):
                if file[i]["Completed"].lower() == "i":
                    ChatbotFile = ChatbotFile + "TaskId: " + file[i]["TaskID"] + " Task: " + file[i]["Task"] + " DateStart: " + file[i]["DateStart"] + " DateDue: " + file[i]["DateDue"] + " User: " +  file[i]["User"] + " Completed: " + file[i]["Completed"]+ " TaskDifficulty: " + file[i]["TaskDifficulty"] +"\n"
    return ChatbotFile

def AssignTask(Username, command ):
    completed = ["complete", "completed", "done", "finished"]
    inprogress = ["completing", "started", "starting", "initiating"]
    taskIDIndicator = ["task"]
    if textProcessing.inArray(taskIDIndicator, command):
        wordSplit = command.split()
        for i in range(0,len(wordSplit)):
            if textProcessing.inArray(taskIDIndicator, wordSplit[i].lower()):
                if len(wordSplit) > i + 1:
                    if textProcessing.isInt(wordSplit[i + 1]):
                        TaskID =  wordSplit[i + 1]
                    elif len(wordSplit) > i + 2:
                        if textProcessing.isInt(wordSplit[i + 2]):
                            TaskID = wordSplit[i + 2]
                    else:
                        TaskID = None
                else:
                    TaskID = None

    if TaskID != None:
        completedStatus = ""
        if (textProcessing.inArray(completed, command)):
            completedStatus = "completed"
        elif (textProcessing.inArray(inprogress, command)):
            completedStatus = "in progress"

        todostorage.todoEdit(Username, completedStatus, TaskID)

def TaskDifCheck(line): #checks if the task difficulty has been inputted correctly (made by Ben G)
    if textProcessing.isInt(line["TaskDifficulty"]):
        pass
    elif not(textProcessing.isInt(line["TaskDifficulty"])) and line["TaskID"] != "":
        line["TaskDifficulty"] = 1
    else:
        line["TaskDifficulty"] = 0
    return line

def daysDelta(): #FUNCTION Created by Ben G
    file = todostorage.toDoRead()
    now = datetime.datetime.now()
    now = datetime.datetime(now.year, now.month, now.day) #gets rid of the time since taht won't be needed
    startDay, startMonth, startYear = textProcessing.dateDetermineFromString(file[0]["DateStart"], ["/", "\\", "."])
    endDay, endMonth, endYear = textProcessing.dateDetermineFromString(file[0]["DateDue"], ["/", "\\", "."])
    startDate = datetime.datetime(startYear, startMonth, startDay) #all dates for each task has the same times (note year has to be full 2020 not just 20)
    endDate = datetime.datetime(endYear, endMonth, endDay)
    elapsedDays = now - startDate
    maxDays = endDate - startDate
    elapsedDays = (elapsedDays.total_seconds()) / (60*60*24) #makes the only unit of measurement of time I have to work with days
    maxDays = (maxDays.total_seconds()) / (60*60*24)
    

    maxPoints = 0
    currentPoints = 0
    for i in range(0,len(file)): #this counts all the points that are possible to get and the amount of points that have currently been earned
        file[i] = TaskDifCheck(file[i])
        maxPoints = maxPoints + float(file[i]["TaskDifficulty"])
        if "progress" in file[i]["Completed"]:
            currentPoints = currentPoints + (float(file[i]["TaskDifficulty"]) / 2)
        elif "completed" in file[i]["Completed"]:
            currentPoints = currentPoints + float(file[i]["TaskDifficulty"])

    pointsPDay = (maxPoints / maxDays)

    expectedPoints = pointsPDay * elapsedDays


    pointsDelta = currentPoints - expectedPoints
    dayDelta = pointsDelta / pointsPDay

    return dayDelta

print(chatbotread("what"))

