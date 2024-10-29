from contextlib import _RedirectStream
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

#TODO fix this, use htmx and not abuse global state
@patch
def __ft__(self: Audits):
    formelements = P("missing")
    def forminput(item: Str, element, field, desc: str):
        label_input = Container(
            Grid(
                H3(
                    f"{item.title()}"
                ),
                Div(
                    Input(
                        id = element,
                        name = field,
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
                    self.TL_INTRODUCTION, 'TL_INTRODUCTION',
                    "Agent began with a warm opening explained purpose of the call."
                ),
                forminput(
                    'Objection',
                    self.TL_OBJECTION, 'TL_OBJECTION',
                    "Agent acknowledged and attempted to overcome client objections."
                ),
                forminput(
                    'Script',
                    self.TL_SCRIPT, 'TL_SCRIPT',
                    "Agent followed the correcct scripting."
                ),
                forminput(
                    'Verification',
                    self.TL_VERIFICATION, 'TL_VERIFICATION',
                    "Agent verified client information and eligibility."
                ),
                forminput(
                    'Tone',
                    self.TL_TONE, 'TL_TONE',
                    "Agent spoke clearly and with a friendly attitude."
                ),
                forminput(
                    'Deadair',
                    self.TL_DEADAIR, 'TL_DEADAIR',
                    "Agent did not leave excessive (5+ seconds) of silence without speaking."
                ),
                Input(
                    value=self.CALLID,
                    name='CALLID',
                    hidden=True
                ),
                Textarea(
                    placeholder='Notes',
                    value=self.TL_NOTES,
                    name='TL_NOTES'
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
                    self.QA_INTRODUCTION, 'QA_INTRODUCTION',
                    "Agent began with a warm opening explained purpose of the call."
                ),
                forminput(
                    'Objection',
                    self.QA_OBJECTION, 'QA_OBJECTION',
                    "Agent acknowledged and attempted to overcome client objections."
                ),
                forminput(
                    'Script',
                    self.QA_SCRIPT, 'QA_SCRIPT',
                    "Agent followed the correcct scripting."
                ),
                forminput(
                    'Verification',
                    self.QA_VERIFICATION, 'QA_VERIFICATION',
                    "Agent verified client information and eligibility."
                ),
                forminput(
                    'Tone',
                    self.QA_TONE, 'QA_TONE',
                    "Agent spoke clearly and with a friendly attitude."
                ),
                forminput(
                    'Deadair',
                    self.QA_DEADAIR, 'QA_DEADAIR',
                    "Agent did not leave excessive (5+ seconds) of silence without speaking."
                ),
                Textarea(
                    placeholder='Notes',
                    value=self.QA_NOTES,
                    name='QA_NOTES'
                ),
                Input(
                    type='submit'
                    , value='Submit'
                )
            )
        )
        print(f'/{formtype}/{self.CALLID}')
    return Form(
        formelements
        , action=f'/submit'
        , method='post'
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

async def submit_form(request):
    print('endpoint hit')
    form_data = await request.form()
    print(form_data)
    return RedirectResponse(f'/{formtype}', status_code=303)

app.post('/submit')(submit_form)

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
