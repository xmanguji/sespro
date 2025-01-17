from .base import CRUDBase
from model import Question
from schema import QuestionCreate, QuestionUpdate


class CRUDQuestion(CRUDBase[Question, QuestionCreate, QuestionUpdate]):

    pass


question = CRUDQuestion(Question)
