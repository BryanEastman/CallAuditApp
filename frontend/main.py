from fasthtml.common import *


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
def __ft__(self: Audits, formtype: Str):
    def forminput(item: Str, element):
        label_input = Label(
            f"{item.title()}",
            Input(
                name = element,
                type="checkbox",
                role="switch"
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

        return Details(
            Summary(
                formbody(),
                role='button',
                _class='outline contrast'
            )
        )


@rt('/leader')
def director_form():
    return Audits()

def auditor_form():
    return

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
