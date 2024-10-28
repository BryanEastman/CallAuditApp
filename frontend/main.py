from fasthtml.common import *

formtype = 'unset'
db = Database('./data/state.db')

audits = db.t.audits

if audits not in db.t:
    audits.create(
        dict(
            CALLID=int,
            CALLSTARTDATE=str,
            CONVERTED=bool,
            CALLENDREASON=str,
            AGENTID=int,
            AGENTTITLE=str,
            AGENTLEADERID=int,
            QA_INTRODUCTION=bool,
            QA_OBJECTION=bool,
            QA_SCRIPT=bool,
            QA_VERIFICATION=bool,
            QA_TONE=bool,
            QA_DEADAIR=bool,
            QA_NOTES=str,
            TL_INTRODUCTION=bool,
            TL_OBJECTION=bool,
            TL_SCRIPT=bool,
            TL_VERIFICATION=bool,
            TL_TONE=bool,
            TL_DEADAIR=bool,
            TL_NOTES=str,
        ), pk='CALLID'
    )

Audits = audits.dataclass()
app = FastHTML(
    hdrs=(picolink)
)
rt = app.route

#TODO fix this
@patch
def __ft__(self: Audits):
    formelements = P("missing")
    def forminput(item: Str, element, desc: str):
        label_input = Container(
            Grid(
                H3(
                    f"{item.title()}"
                ),
                Div(
                    Input(
                        name = element,
                        type="checkbox",
                        role="switch"
                    )
                )
            ),
                P(
                    desc
                )
        )

        return label_input

    def formbody():
        bod = Div(
            H2("Agent: ", self.AGENTID),
            P("Call ID: ", self.CALLID),
            P("Call Start: ", self.CALLSTARTDATE),
            P("Call End Reason: ", self.CALLENDREASON)
        )
        return bod

    if formtype == 'leader':
        formelements = Details(
            Summary(
                formbody(),
                role='button',
                _class='outline contrast'
            ),
            Container(
                forminput(
                    'Introduction',
                    self.TL_INTRODUCTION,
                    "Agent began with a warm opening explained purpose of the call."
                ),
                forminput(
                    'Objection',
                    self.TL_OBJECTION,
                    "Agent acknowledged and attempted to overcome client objections."
                ),
                forminput(
                    'Script',
                    self.TL_SCRIPT,
                    "Agent followed the correcct scripting."
                ),
                forminput(
                    'Verification',
                    self.TL_VERIFICATION,
                    "Agent verified client information and eligibility."
                ),
                forminput(
                    'Tone',
                    self.TL_TONE,
                    "Agent spoke clearly and with a friendly attitude."
                ),
                forminput(
                    'Deadair',
                    self.TL_DEADAIR,
                    "Agent did not leave excessive (5+ seconds) of silence without speaking."
                ),
                Textarea(
                    'Notes',
                    name=self.TL_NOTES
                ),
                Input(
                    type='submit'
                    , value='Submit'
                )
            )
        )

    elif formtype == 'auditor':
        formelements = Details(
            Summary(
                formbody(),
                role='button',
                _class='outline contrast'
            ),
            Container(
                forminput(
                    'Introduction',
                    self.QA_INTRODUCTION,
                    "Agent began with a warm opening explained purpose of the call."
                ),
                forminput(
                    'Objection',
                    self.QA_OBJECTION,
                    "Agent acknowledged and attempted to overcome client objections."
                ),
                forminput(
                    'Script',
                    self.QA_SCRIPT,
                    "Agent followed the correcct scripting."
                ),
                forminput(
                    'Verification',
                    self.QA_VERIFICATION,
                    "Agent verified client information and eligibility."
                ),
                forminput(
                    'Tone',
                    self.QA_TONE,
                    "Agent spoke clearly and with a friendly attitude."
                ),
                forminput(
                    'Deadair',
                    self.QA_DEADAIR,
                    "Agent did not leave excessive (5+ seconds) of silence without speaking."
                ),
                Textarea(
                    'Notes',
                    name=self.QA_NOTES
                ),
                Input(
                    type='submit'
                    , value='Submit'
                )
            )
        )

    return Form(
        formelements
    )


@rt('/leader')
def director_form():
    global formtype
    formtype = 'leader'
    return audits()

@rt('/auditor')
def auditor_form():
    global formtype
    formtype = 'auditor'
    return audits()

@rt('/')
def get():
    return Container(
        H1("Select App"),
        Grid(
            Group(A('leader', href='/leader', role='button')),
            Group(A('auditor', href='/auditor', role='button'))
        )
    )

serve()
