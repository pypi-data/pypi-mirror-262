import os
from typing import Optional

from toolboxv2 import get_app, App, MainTool, FileHandler
from .content_gen import PipelineManager

Name = "diffuser"
version = "0.0.1"
export = get_app(from_="diffuser.EXPORT").tb
no_test = export(mod_name=Name, test=False, version=version)
test_only = export(mod_name=Name, test_only=True, version=version, state=True)
to_api = export(mod_name=Name, api=True, version=version)


class Tools(MainTool, FileHandler):
    version = version
    pipeline_manager = Optional[PipelineManager]

    def __init__(self, app=None):
        self.name = Name
        self.color = "YELLOW"

        self.keys = {"mode": "db~mode~~:"}
        self.encoding = 'utf-8'

        self.pipeline_manager = None

        MainTool.__init__(self,
                          load=self.on_start,
                          v=self.version,
                          name=self.name,
                          color=self.color,
                          on_exit=self.on_exit)

    @export(
        mod_name=Name,
        name="Version",
        version=version,
    )
    def get_version(self):
        return self.version

    @export(mod_name=Name, initial=True, name="on_start", version=version)
    def on_start(self):
        self.pipeline_manager = PipelineManager()

    @export(mod_name=Name, exit_f=True, name="on_exit", version=version)
    def on_exit(self):
        if self.pipeline_manager is None:
            return
        self.pipeline_manager = None

    @export(mod_name=Name, name="start_ui", test=False, version=version)
    def start_ui(self, app: App):
        """starting the application"""
        os.system(f"streamlit run {app.start_dir}/mods/diffuser/st_runner.py")

    @export(mod_name=Name, name="get_pipline_manager", version=version)
    def get_pipline_manager(self):
        if self.pipeline_manager is None:
            return None
        return self.pipeline_manager
