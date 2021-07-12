import os


class Document:
    def __init__(self, fileName, title, author):
        self.folder = os.getcwd()+'/pdfs/'
        self.fileName = self.folder+fileName
        self.file = open(self.fileName+'.tex', "w+")
        self.file.write("\\documentclass{article}\n")
        self.file.write("\\usepackage[utf8]{inputenc}\n")
        self.file.write("\\usepackage{breqn}")
        self.file.write('\\title{'+title+'}\n')
        self.file.write('\\author{'+author+'}\n')
        self.file.write('\\usepackage[dvipsnames]{xcolor}\n')
        self.file.write('\\begin{document}\n')
        self.file.write('\\maketitle\n')
        self.file.write("\\relpenalty   = 10000")
        self.file.write("\\relpenalty   = 10000")
        self.file.write("\\definecolor{backgroundcolor}{HTML}{FFFFEA}")
        self.file.write("\\definecolor{maintextcolor}{HTML}{42273B}")
        self.file.write("\\definecolor{rulecolor}{HTML}{360568}")

        self.file.write("\\color{maintextcolor}")
        self.file.write("\\pagecolor{backgroundcolor}")

    def addSection(self, name):
        self.file.write('\\section*{'+name+'}\n')

    def addSubsection(self, name):
        self.file.write('\\subsection*{'+name+'}\n')

    def addEquation(self, equation):
        self.file.write('\\begin{dmath*}')
        self.file.write(equation.toTex())
        self.file.write("\\end{dmath*}")

    def addValue(self, leftHandSide, equation):
        self.file.write('\\begin{dmath}')
        self.file.write(leftHandSide.toTex()+"="+equation.toTex())
        self.file.write("\\end{dmath}")

    def addEquationText(self, equation):
        self.file.write('\\begin{equation*}')
        self.file.write(equation)
        self.file.write("\\end{equation*}")

    def addText(self, text):
        self.file.write(text+'\\newline \n ')

    def addCode(self, tex):
        self.file.write(tex)

    def render(self):
        self.file.write('\end{document}\n')
        self.file.close()
        os.system('pdflatex '+' --output-directory=' +
                  self.folder+' '+self.fileName)
        os.system('google-chrome '+self.fileName+'.pdf')
        pass

    def addWorkings(self, workings):
        steps = workings.getSteps()
        self.addSubsection("Algorithmic Workings")
        self.file.write(workings.getProblem().toTex(False, "dmath*"))
        for step in steps:
            if not step.isTrivial():
                if step.rule:
                    self.file.write("\\begin{center} \\color{rulecolor} \\begin{math} \\text{using }" +
                                    step.ruleTex()+"\\end{math}\\color{maintextcolor} \\end{center} ")
                self.file.write(step.toTex(False, "dmath*"))
        self.addSubsection("Result:")
        self.file.write(workings.getResultTex(False, "dmath*"))

    def addEquals(self):
        self.addCode("\\begin{equation*}=\\end{equation*}")
