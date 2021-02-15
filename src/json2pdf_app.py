import base64
import json
# import os
from pylatex.utils import NoEscape, italic

import streamlit as st
from latex import build_pdf
from pylatex import Command, Document, Section, Subsection, UnsafeCommand

st.title("Resume Builder")
# we need to supply absolute paths
# current_dir = os.path.abspath(f'{os.path.dirname(__file__)}/../data/temp')
current_dir = 'data/temp'
st.beta_columns((1, 1))
d = dict()
input = st.sidebar.beta_container()
input_name = input.beta_columns((1, 1))
d['first_name'] = input_name[0].text_input('First name')
d['last_name'] = input_name[1].text_input('Last name')
d['job_title'] = input.text_input('Job title')
show_personal_details = input.checkbox('Show Personal Details')
if show_personal_details:
    d['birth_date'] = input.text_input('Date of Birth')
    d['address'] = input.text_input('Address')
    d['phone'] = input.text_input('Phone no.')
show_skills = input.checkbox('Show Skills')
if show_skills:
    d['hlang'] = input.text_input('Languages')
    d['plang'] = input.text_input('Programming Languages')
doc = Document(documentclass='article')


doc.preamble.append(Command("usepackage", "mdframed"))
doc.preamble.append(Command("usepackage", "babel","english"))
#    doc.preamble.append(Command("usepackage", "inputenc","utf8x"))
doc.preamble.append(Command("usepackage","microtype", ["protrusion=true" , "expansion=true"]))
doc.preamble.append(Command("usepackage", "amsmath"))
doc.preamble.append(Command("usepackage", "amsfonts"))
doc.preamble.append(Command("usepackage", "amsthm"))
doc.preamble.append(Command("usepackage", "graphicx"))
doc.preamble.append(Command("usepackage", "xcolor", "svgnames"))
doc.preamble.append(Command("usepackage", "geometry"))
doc.preamble.append(Command("usepackage", "url"))
doc.preamble.append(Command("usepackage", "sectsty"))


doc.append(Command('frenchspacing'))
doc.append(Command('pagestyle', 'empty'))
# \textheight=700px
# doc.append(Command("textheight=700px"))

# doc.append(Command("sectionfont", [
#     Command("usefont",["OT1","phv","b","n"]),
#     Command("sectionrule",["0pt","0pt",NoEscape("-5pt"),"3pt"])]))

# doc.append(Command("sectionfont", NoEscape(r""" \usefont{OT1}{phv}{b}{n} \sectionrule{0pt}{0pt}{-5pt}{3pt}}""")))


# doc.append(Command("sectionfont", [
#     Command("usefont",["OT1","phv","b","n"]),
#     NoEscape(Command("sectionrule",["0pt","0pt",NoEscape("-5pt"),"3pt"]))]))




doc.append(Command("newlength",Command("spacebox")))

doc.append(Command("settowidth",[Command("spacebox"), "8888888888"]))

# \newlength{\spacebox}
# \settowidth{\spacebox}{8888888888}


sepspace = UnsafeCommand('newcommand', r'\sepspace',
                         extra_arguments=r"""
                            \vspace*{1em}
                            """)

doc.append(sepspace)
MyName = UnsafeCommand('newcommand', r'\MyName', options=1,
                       extra_arguments=r"""
        \Huge \usefont{OT1}{phv}{b}{n} \hfill #1
        \par \normalsize \normalfont
        """)

doc.append(MyName)
MySlogan = UnsafeCommand('newcommand', r'\MySlogan', options=1,
                         extra_arguments=r"""
    \large \usefont{OT1}{phv}{m}{n}\hfill \textit{#1}
    \par \normalsize \normalfont
    """)
NewPart = UnsafeCommand('newcommand', r'\NewPart', options=1,
                        extra_arguments=r"""
                            \section*{\uppercase{#1}}
""")

doc.append(NewPart)


# ###########################

# ###########################


PersonalEntry = UnsafeCommand('newcommand', r'\PersonalEntry', options=2,
                              extra_arguments=r"""
    \noindent\hangindent=2em\hangafter=0 % Indentation
    \parbox{\spacebox}{        % Box to align text
    \textit{#1}}               % Entry name (birth, address, etc.)
    \hspace{1.5em} #2 \par    % Entry value
""")

doc.append(PersonalEntry)


###########################

###########################


SkillsEntry = UnsafeCommand('newcommand', r'\SkillsEntry', options=2,
                            extra_arguments=r"""
    \noindent\hangindent=2em\hangafter=0 % Indentation
    \parbox{\spacebox}{        % Box to align text
    \textit{#1}}			   % Entry name (birth, address, etc.)
    \hspace{1.5em} #2 \par    % Entry value
""")

doc.append(SkillsEntry)

# ###########################

# ###########################


# EducationEntry = UnsafeCommand('newcommand', r'\EducationEntry', options=4,
#                                extra_arguments=r"""
#     \noindent \textbf{#1} \hfill      % Study
#     \colorbox{Black}{%
#         \parbox{6em}{%
#         \hfill\color{White}#2}} \par  % Duration
#     \noindent \textit{#3} \par        % School
#     \noindent\hangindent=2em\hangafter=0 \small #4 % Description
#     \normalsize \par
# """)

# doc.append(EducationEntry)


# ###########################

# ###########################


# WorkEntry = UnsafeCommand('newcommand', r'\WorkEntry', options=4,
#                           extra_arguments=r"""
#         % Same as \EducationEntry
#     \noindent \textbf{#1} \hfill      % Jobname
#     \colorbox{Black}{\color{White}#2} \par  % Duration
#     \noindent \textit{#3} \par              % Company
#     \noindent\hangindent=2em\hangafter=0 \small #4 % Description
#     \normalsize \par
# """)

# doc.append(WorkEntry)
json_file_path = f'{current_dir}/jg.json'
with open(json_file_path, 'w+') as outfile:
    json.dump(d, outfile, indent=4)
with open(json_file_path) as json_file:
    data = json.load(json_file)
# d = data
doc.append(MySlogan)
doc.append(Command("MyName", f"{d['first_name']} {d['last_name']}"))
doc.append(Command("MySlogan", f"{d['job_title']}"))
doc.append(Command('sepspace'))

if show_personal_details:
    doc.append(Command('NewPart', ["Personal details", NoEscape("")]))
    if len(d['birth_date']): doc.append(Command('PersonalEntry', ["Birth", d['birth_date']]))
    if len(d['address']): doc.append(Command('PersonalEntry', ["Address", d['address']]))
    if len(d['phone']): doc.append(Command('PersonalEntry', ["Phone", d['phone']]))

if show_skills:
    doc.append(Command('NewPart', ["Skills", NoEscape("")]))
    if len(d['hlang']): doc.append(Command("SkillsEntry", [ "Human Languages", d['hlang']]))
    if len(d['plang']): doc.append(Command("SkillsEntry", [ "Programming Languages", d['plang']]))
    
tex = doc.dumps()  # The document as string in LaTeX syntax

tex_file_path = f'{current_dir}/jg'
doc.generate_tex(tex_file_path)


pdf = build_pdf(open(f'{tex_file_path}.tex'))
pdf_path = f'{current_dir}/myresume.pdf'
pdf.save_to(pdf_path)

# def show_pdf(pdf_file):
#     with open(pdf_file,"rb") as f:
#       base64_pdf = base64.b64encode(f.read()).decode('utf-8')
#       pdf_display = f'<embed src=”data:application/pdf;base64,{base64_pdf}” width=”700″ height=”1000″ type=”application/pdf”>’
#       st.markdown(pdf_display, unsafe_allow_html=True)


def show_pdf(pdf_file):
    st.markdown('## PDF')
    with open(pdf_file, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf">'
    st.markdown(pdf_display, unsafe_allow_html=True)


show_pdf(pdf_path)
