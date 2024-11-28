from admin_reorder.middleware import ModelAdminReorder
from django.urls import resolve, Resolver404


class CustomModelAdminReorder(ModelAdminReorder):
    def process_template_response(self, request, response):
        try:
            url = resolve(request.path_info)
        except Resolver404:
            print("Resolver404")
            return response
        if not url.app_name == "admin" and url.url_name not in ["index", "app_list"]:
            print("not admin or name")
            # current view is not a django admin index
            # or app_list view, bail out!
            return response

        try:
            app_list = response.context_data["app_list"]
        except KeyError:
            # there is no app_list! nothing to reorder
            app_list = response.context_data["available_apps"]

        print(app_list)
        self.init_config(request, app_list)
        ordered_app_list = self.get_app_list()
        response.context_data["app_list"] = ordered_app_list
        response.context_data["available_apps"] = ordered_app_list
        return response
