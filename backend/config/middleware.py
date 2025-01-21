from admin_reorder.middleware import ModelAdminReorder
from django.urls import resolve, Resolver404


class CustomModelAdminReorder(ModelAdminReorder):
    def process_template_response(self, request, response):
        try:
            url = resolve(request.path_info)
        except Resolver404:
            return response
        if not url.app_name == "admin" and url.url_name not in ["index", "app_list"]:
            # current view is not a django admin index
            # or app_list view, bail out!
            return response

        app_list = response.context_data.get("app_list") or response.context_data.get(
            "available_apps", []
        )

        self.init_config(request, app_list)
        ordered_app_list = self.get_app_list()
        response.context_data["app_list"] = ordered_app_list
        response.context_data["available_apps"] = ordered_app_list
        return response
