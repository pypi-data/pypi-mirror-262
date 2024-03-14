from nf_jira import wrapper_jira
from dotenv import load_dotenv
import json

load_dotenv()

def test_nota_de_pedido():

    with open("./issue_context_model.json", "r", encoding="utf-8") as arquivo_json: nota_pedido = json.load(arquivo_json)

    lib_jira = wrapper_jira(True)
    issue_data = lib_jira.get_nf_issue_context('GHN-8')

    assert issue_data == nota_pedido