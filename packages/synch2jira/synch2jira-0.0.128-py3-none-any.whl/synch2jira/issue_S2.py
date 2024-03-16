from datetime import datetime
import json
import requests
from requests.auth import HTTPBasicAuth

import config
from synch2jira.issue import Issue
from synch2jira.issue_S1 import IssueS1

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}
class IssueS2(Issue):
    key: str

    def __init__(self, key=None, summary=None, description=None, updated=None, status_updated=None, status=None):
        Issue.__init__(self, summary, description, updated, status, status_updated)
        self.key = key
        # if self.key is not None :
        #     self.miror = self.get_miror()  # id au lieu de IssueS1,
        if self.miror is not None:
            self.miror.miror = self
        # self.workflow_history = self.get_worflow_history()

    def format_issue_into_json(self):
        issue = {
            "fields": {
                "description": {
                    "content": [
                        {
                            "content": [
                                {
                                    "text": self.description if self.description else "",
                                    "type": "text"
                                }
                            ],
                            "type": "paragraph"
                        }
                    ],
                    "type": "doc",
                    "version": 1
                },
                "issuetype": {
                    "id": config.key_issue_type
                },
                "project": {
                    "id": config.project_key
                },
                "labels": config.labels if config.labels else [],
                "summary": self.summary
            },
            "update": {},
        }
        if self.miror is not None:
            issue['fields'][config.s1_id_in_jira] = str(self.miror.id)
        return json.dumps(issue)

    @staticmethod
    def convertir_json_en_issue(issue_json):
        try:
            issue_key = issue_json.get('key', None)
            issue_summary = issue_json['fields'].get('summary', None)
            description_data = issue_json['fields'].get('description', None)

            description_text = None
            if description_data is not None and 'content' in description_data:
                content_list = description_data['content']

                if content_list and content_list[0].get('content'):
                    description_text = content_list[0]['content'][0].get('text', None)

            issue_updated = issue_json['fields'].get('updated', None)
            status = issue_json['fields']['status']['name']
            status_updated = issue_json['fields'].get('statuscategorychangedate', None)
            return IssueS2(key=issue_key, summary=issue_summary, description=description_text,
                                         updated=issue_updated, status_updated=status_updated,
                                         status=status)
        except Exception as e:
            print(e)
            return None

    @classmethod
    def create_issue_lite(cls, issue_json):
        issue = IssueS2()
        issue.key = issue_json['key']
        issue.updated = issue_json['updated']
        return issue
    
    @staticmethod
    def get_miror(self):
        response = IssueS2.jira_resquest("GET", config.jira_url_ticket + self.key)
        if response.status_code == 200:
            mirror_id = response.json()['fields'].get(config.s1_id_in_jira, None)
            miror = IssueS1.find_by_id(mirror_id)
            return miror

    def get(self):
        try:
            #response = requests.request("GET", config.jira_url_ticket + self.key, headers=config.headers,auth=config.auth)
            response = IssueS2.jira_resquest("GET", config.jira_url_ticket + self.key)
            json_data = response.json()
            issue = IssueS2.convertir_json_en_issue(json_data)
            if issue is not None:
                return IssueS2(key=issue.key, summary=issue.summary, description=issue.description,
                                             status_updated=issue.status,
                                             updated=issue.updated, status=issue.status)
        except Exception as e:
            return e
    @staticmethod   
    def jira_resquest(method,url,auth = config.auth,headers = {},params = {},data = {}):
        response = requests.request(method,url,auth = auth,headers = headers,params = params,data = data,verify=config.verify_ssl_certificate)
        return response

    @staticmethod
    def find_by_id(key):
        try:
            #response = requests.request("GET", config.jira_url_ticket + key, headers=config.headers, auth=config.auth)
            response = IssueS2.jira_resquest(method = 'get',url=config.jira_url_ticket + key)
            json_data = response.json()
            issue = IssueS2.convertir_json_en_issue(json_data)
            if issue is not None:
                return IssueS2(key=issue.key, summary=issue.summary, description=issue.description,
                                             updated=issue.updated, status=issue.status)
        except Exception as e:
            return e

    @staticmethod
    def find_by(jql_query):
        print(jql_query, " ==== query")
        payload = {"jql": jql_query}
        #response = requests.get(config.jira_url_all, params=payload, headers=config.headers,auth=config.auth)  # à modifier
        response = IssueS2.jira_resquest(method = 'get',url=config.jira_url_all,params=payload)
        print("response code ", response.status_code)
        if response.status_code == 200:
            print("jql response", response.json().get("issues", []))
            return response.json().get("issues", [])
        else:
            return []

    # @staticmethod
    # def delete_all(jql_query):
    #     payload = {"jql": jql_query}
    #     response = requests.get(configurations.jira_url_all, params=payload, headers=configurations.headers, auth=configurations.auth)
    #     if response.status_code == 200:
    #         issues = response.json().get("issues", [])
    #         for issue in issues:
    #             IssueS2.delete(issue["key"])
    #     else:
    #         return f"Failed to execute search query. Status code: {response.status_code}"

    @staticmethod
    def get_jira_transitions_and_columns(issue_key):
        # transitions methode 2
        transitions_url = f"{config.jira_url_base}/rest/api/2/issue/createmeta"
        # workflow_url = f"{configurations.jira_url_base}rest/api/2/workflow"
        # print("workflow url ",workflow_url)
        # #  la liste des workflows
        # workflows_response = requests.get(workflow_url, auth=configurations.auth)
        # print("repose",workflows_response)
        # workflows_data = workflows_response.json()
        # # on veux  les colonnes du premier workflow trouvé
        # if len(workflows_data) > 0:
        #     for work in workflows_data:
        #         print("work ...",work)
        #         if work["name"] == configurations.workflow_name:
        #             workflow_id = work["scope"]["project"]["id"]
        #             workflow_columns_url = f"{configurations.jira_url_base}rest/api/2/workflow/{workflow_id}/properties/jira.meta.statuses" #/properties/jira.meta.statuses
        #             print("workflow columnnn url ",workflow_columns_url)
        #             #  colonnes du workflow
        #             columns_response = requests.get(workflow_columns_url, auth=configurations.auth)
        #             print(columns_response)
        #             #columns_data = columns_response.json()
        #             #columns = [status['name'] for status in columns_data]
        #         else:
        #             columns = []
        return [], []

    @staticmethod
    def get_jira_transitions(issue_key):
        transitions = []
        transition_url = config.jira_url_ticket + issue_key + "/transitions"
        #transitions_response = requests.get(transition_url, auth=config.auth)
        response = IssueS2.jira_resquest(method = 'get',url=transition_url)
        transitions_data = response.json()
        transitions = [transition['name'] for transition in transitions_data['transitions']]
        return transitions

    @staticmethod
    def get_jira_status():
        status = []
        status_url = f"{config.jira_url_base}rest/api/3/status"
        #status_response = requests.get(status_url, auth=config.auth)
        response = IssueS2.jira_resquest(method = 'get',url=status_url)
        status_data = response.json()
        status = [status["name"] for status in status_data]
        return status

    # @staticmethod
    # def get_worflow_history(self):
    #     results = []
    #     history_url = f"{config.jira_url_ticket}{self.key}/changelog"
    #     history_response = requests.get(history_url, auth=config.auth)
    #     if history_response.status_code != 200:
    #         #print(f"Erreur lors de la récupération des transitions pour le ticket {issue_key}. Code d'erreur : {history_response.status_code}")
    #         return []
    #     i = 0
    #     history_data = history_response.json()
    #     histories = history_data['values']
    #     # print("last",histories[-1])
    #     # print("first",histories[0])
    #     # print(histories)
    #     for history in histories:
    #         created = history['created']
    #         items = history['items']
    #         for item in items:
    #             field = item['field']
    #             # print(field)
    #             # print(item)
    #             if field == "status":

    #                 print(f" history number {i+1}", history)
    #                 from_state = item['fromString']
    #                 to_state = item['toString']
    #                 #results.append([created,from_state,to_state])
    #                 history_dict = {'status_change_time': created, 'from_state': from_state, 'to_state':to_state}
    #                 results.append(history_dict)
    #                 #print("created at ",created,"from state ",from_state,"to state ",to_state)
    #                 i+=1
    #     #self.workflow_history = results

    #     return results

    @staticmethod
    def all_():
        issues = IssueS2.get_issue_list_from_jira()
        issues_list = []
        for issue in issues:
            issues_list.append(IssueS2.convertir_json_en_issue(issue))

        return issues_list

    @staticmethod
    def all():
        if config.jql_query:
            return IssueS2.find_by(config.jql_query)
        issues = IssueS2.get_issue_list_from_jira()
        return issues

        # issue_list = IssueS2.find_by(config.jql_query)
        # return [IssueS2.convertir_json_en_issue(issue) for issue in issue_list]

    @staticmethod
    def all_lite():
        fields = ['updated', 'statuscategorychangedate']
        issues = IssueS2.get_issue_list_from_jira(fields)
        return [IssueS2(key=issue["key"], updated=issue["fields"].get("updated", None),
                                      status_updated=issue["fields"].get("statuscategorychangedate")) for issue in
                issues]

    @staticmethod
    def all_weight():
        fields = ["updated", 'statuscategorychangedate','summary','description']
        issues = IssueS2.get_issue_list_from_jira(fields)
        #print(issues, 'issue wieght')
        return [IssueS2.convertir_json_en_issue(issue) for issue in issues]

    @staticmethod
    def get_issue_list_from_jira_():
        #response = requests.get(config.jira_url_all, headers=config.headers, auth=config.auth)
        response = IssueS2.jira_resquest(method = 'get',url=config.jira_url_all)

        issues = response.json()["issues"]
        return issues

    # take a list of fiels as parameter : fiels you wwant to get in the response
    @staticmethod
    def get_issue_list_from_jira(fields):
        batch_size = 100
        issues = []
        start_at = 0
        while True:
            params = {'jql': '', "startAt": start_at, "maxResults": batch_size, "fields": fields}
            #response = requests.get(config.jira_url_all, headers=config.headers, params=params, auth=config.auth)
            response = IssueS2.jira_resquest(method = 'get',url=config.jira_url_all,params=params)

            if response.status_code == 200:
                batch_tickets = response.json()["issues"]
                issues.extend(batch_tickets)
                start_at += batch_size
                if len(batch_tickets) < batch_size:
                    break  # on arrete la boucle si moins de tickets sont retournés que le batch_size
            else:
                return []
        print(f'nombre de ticket {len(issues)}')
        return issues

    @staticmethod
    def all_jql():
        return [IssueS2(issue["key"], issue["fields"]["updated"]) for issue in
                IssueS2.find_by(config.jql_query)]

    @staticmethod
    def get_project_list():
        project_url = f'{config.jira_url_base}/rest/api/3/project'
        #response = requests.get(url, headers=config.headers, auth=config.auth)
        response = IssueS2.jira_resquest(method = 'get',url=project_url)
        if response.status_code == 200:
            projects = response.json()

            for project in projects:
                print(project)
                print(project['key'], '-', project['name'], '-', project['id'])
            return [[project['key'], project['name'], project['id']] for project in projects]
        else:
            print(f"La requête a échoué avec le code d'erreur {response.status_code}")

    @staticmethod
    def all_filtre_id_et_updated():
        issues = IssueS2.get_issue_list_from_jira()
        issues_list = []
        for issue in issues:
            issue_key = issue.get('key', None)
            issue_updated = issue['fields'].get('updated', None)
            issues_list.append(
                IssueS2(key=issue_key, summary="", description="", updated=issue_updated, status=""))
        return issues_list

    def save(self):
        #response = requests.request("POST", config.jira_url_ticket, data=self.format_issue_into_json(),headers=config.headers,auth=config.auth)
        response = IssueS2.jira_resquest(method = 'post',url=config.jira_url_ticket ,data=self.format_issue_into_json())
        if response.status_code == 201:
            return (json.loads(response.text)).get("key")
        else:
            return f"Erreur lors de la création du ticket. Code d'erreur : {response.json()}"

    # def delete(self):
    #     response = requests.request("DELETE", config.jira_url_ticket + self.key, auth=config.auth)
    #
    #     if response.status_code == 204:
    #         print(f"Suppression effectuée avec succées")
    #     else:
    #         print(f"Erreur lors de la suppression du ticket. Code d'erreur : {response.status_code}")

    def update(self):
        #response = requests.request("PUT", config.jira_url_ticket + self.key, data=self.format_issue_into_json(),headers=config.headers, auth=config.auth)
        response = IssueS2.jira_resquest(method = 'put',url=config.jira_url_ticket + self.key,data=self.format_issue_into_json())
        return response.text

    # takes transitions as argument not status Name (Columns)
    def change_issue_status(self, new_status):
        transition_url = config.jira_url_ticket + self.key + "/transitions"
        #response = requests.get(transition_url, auth=config.auth)
        response = IssueS2.jira_resquest(method = 'get',url=transition_url)
        transitions = response.json()['transitions']
        transition_id = None
        for transition in transitions:
            if transition['name'] == new_status:
                transition_id = transition['id']
                break
        if not transition_id:
            return None

        data = {
            "transition": {"id": transition_id}
        }
        headers = {'Content-Type': 'application/json'}

        response = requests.post(transition_url, json=data, headers=headers, auth=config.auth)

        if response.status_code == 204:
            return transition_id
        else:
            print("Erreur lors du changement de statut:", response.text)
            return None

    # @staticmethod
    # def supprimer_tickets_entre_a_and_b(a, b):
    #     for i in range(a, b):
    #         key = "KAN-" + str(i)
    #         issue_to_delete = IssueS2(key=key, summary="", description="", updated="", status="")
    #         issue_to_delete.delete()

    @staticmethod
    def check_connection(jira_url, username, api_token):
        try:
            auth = HTTPBasicAuth(username, api_token)
            response = requests.head(jira_url, auth=auth)
            if response.status_code == 200:
                return True
            else:
                return False
        except requests.RequestException as e:
            print("Erreur de connexion à Jira:", e)
            return False

    @staticmethod
    def try_jira_connection():
        response = IssueS2.jira_resquest(method = 'head',url=config.jira_url_base)
        if response.status_code == 200:
            return True
        return False

    @staticmethod
    def create_isssue_and_move_to_done_for_performance_test():
        new_status = 'Terminé'
        status = "Pret"
        key_list = []
        for i in range(307, 500):
            description = f'description_{i}'
            summary = f'summary_{i}'
            issue = IssueS2(summary=summary, description=description)
            key = issue.save()
            print(key)
            key_list.append(key)
            issue = IssueS2.find_by_id(key)
            result = issue.change_issue_status(new_status)
            print(f'transition id {result}   key {key}  iteration {i}')
            # issue.delete()
            # break
        print(key_list)
        return key_list
    
    @staticmethod
    def all_key():
        fields = ["updated"]
        return [issue.get('key') for issue in IssueS2.get_issue_list_from_jira(fields)]

