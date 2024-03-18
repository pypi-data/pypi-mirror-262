from copy import deepcopy


class ProjectPreprocessor:
    def __init__(self, project_ksg):
        self.project_ksg = project_ksg

    def remove_extra_works(self, names_to_remove):
        removed_ids = {
            work["id"]
            for work in self.project_ksg["schedule"]["works"]
            if work.get("display_name") in names_to_remove
        }

        self.project_ksg["schedule"]["works"] = [
            work
            for work in self.project_ksg["schedule"]["works"]
            if work.get("display_name") not in names_to_remove
        ]

        self.project_ksg["wg"]["nodes"] = [
            node
            for node in self.project_ksg["wg"]["nodes"]
            if node.get("work_unit", {}).get("display_name") not in names_to_remove
        ]

        for node in self.project_ksg["wg"]["nodes"]:
            if "parent_edges" in node:
                node["parent_edges"] = [
                    edge for edge in node["parent_edges"] if edge[0] not in removed_ids
                ]
