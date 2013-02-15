def getAnnounceMessage(date, location, presenters, footer):
    message = "Dear All, <br><br>"
    message += "The WAI presentations coming Monday (%s) will be held in <strong>room %s</strong> at 11:00.<br><br>\n\n" % (date, location)
    for presenter in presenters:
        message += "<strong>%s</strong>: <i>%s</i>\n<br>%s\n\n<br><br>" % (presenter["name"], presenter["title"], presenter["abstract"])
    
    message += "\n\n<br>For the list of upcoming wai talks, visit the WAI site at <a href='http://wai.few.vu.nl' target='_blank'>http://wai.few.vu.nl</a>.<br>\n";
    message += footer
    return message

def getAnnounceSubject(date, presenters, locationName):
    return "WAI Monday (%s): %s (11:00 %s)" % (date, presenters, locationName)

def getRequestMessage(presenters, date, footer):
    message = "Dear " + presenters
    
    message += "<br><br>"
        
    message += "Your presentation is scheduled for %s at 11am.\n" % date
    message += "Please send us the title and the abstract of your talk as soon as possible, not later than coming Wednesday, so we can send the announcement to the list.\n"
    
    message += "<br><br>\n"
    
    message += "Please note, that:\n"
    message += "<ul>"
    message += "<li> In case of cancellation, go to <a target='_blank' href='http://wai.few.vu.nl'>http://wai.few.vu.nl</a> and find someone from the top of the reserve list to fill your slot. Let us know when you have done so.</li>\n"
    message += "<li> In order to ease the interaction with the audience, you should announce the purpose of your talk before you start. Some examples :\n"
    message += "<ul>"
    message += "<li> Rehearse a presentation for a conference,</li>\n"
    message += "<li> Ask for feedback on an on-going project,</li>\n"
    message += "<li> Discuss a new idea</li>\n"
    message += "<li> Have a general discussion</li>\n"
    message += "</ul>"
    message += "</li>"
    message += "<li> In any case, the presentation must not be no longer than 30 minutes.</li>\n"
    message += "</ul>\n"
    message += "If you want to answer to some questions during the talk, be sure to manage your time accordingly.\n"
    message += "We will chair the session and indicate the beginning of the last 5 minutes relative to the half an hour.\n"
    
    message += "<br>\n"
    
    message += "It is also important to note that:\n"
    message += "<ul>"
    message += "<li> A beamer will be available on the spot but you need to bring your own laptop. Please be present 5 minutes before starting, so we can get everything connected and tested.</li>\n"
    message += "<li> The time slot is fairly short. Please do not prepare too many slides (10-15 is probably about right depending on your style)</li>\n"
    message += "<li> The point of the WAI is to let your colleagues know what you're doing, not to give an in-depth lecture about certain algorithms or theories. Keep your presentation limited to things that are relevant to understand the main point of your talk, and accessible to the general AI public.</li>\n"
    message += "<li> The presenter is responsible to timing his/her presentation and for managing discussions. Feel free to cut people short if their questions are irrelevant or if you do not have time to answer them. It's your show, and we are only responsible for stopping it after 30 minutes.</li>\n"
    message += "</ul><br>\n"
    message += footer
    return message
    
def getRequestSubject():
    return "WAI - Presenter reminder"
    