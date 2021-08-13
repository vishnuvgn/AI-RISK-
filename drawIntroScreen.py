from cmu_112_graphics import *

# https://i.kinja-img.com/gawker-media/image/upload/t_original/1462528836859457569.jpg
# ^ for risk piece pics

def loadRiskPieces(app):
    app.riskMan = app.loadImage('risk_man.png')
    app.riskMan = app.scaleImage(app.riskMan, 2/3)

    app.riskHorse = app.loadImage('risk_horse.png')
    app.riskHorse = app.scaleImage(app.riskHorse, 2/3)

    app.riskCannon = app.loadImage('risk_cannon.png')
    app.riskCannon = app.scaleImage(app.riskCannon, 2/3)


def drawRiskPieces(app, canvas):
    canvas.create_image(app.width/4, 1*app.height/4, image=ImageTk.PhotoImage(app.riskMan))
    canvas.create_image(3*app.width/4, 2*app.height/4, image=ImageTk.PhotoImage(app.riskHorse))
    canvas.create_image(app.width/4, 3*app.height/4, image=ImageTk.PhotoImage(app.riskCannon))


def drawTitle(app, canvas):
    font = "Papyrus 150 bold"
    fill="red"
    canvas.create_text(app.width/2, 10+app.height/10, text="RISK", fill=fill, font=font)