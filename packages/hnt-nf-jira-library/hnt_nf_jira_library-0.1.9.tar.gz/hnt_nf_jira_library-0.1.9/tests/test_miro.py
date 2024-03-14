from nf_jira import wrapper_jira
from dotenv import load_dotenv
import json

load_dotenv()

def test_nota_de_pedido():

    with open("./miro_context_model.json", "r", encoding="utf-8") as arquivo_json: miro = json.load(arquivo_json)

    lib_jira = wrapper_jira(True)
    issue_data = lib_jira.get_nf_miro_context('GHN-8','123456')

    assert issue_data == miro