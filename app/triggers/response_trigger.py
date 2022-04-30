from app.services import PipelineService


class PostResposeSubmitTrigger(object):
    @classmethod
    def trigger(
        cls,
    ):
        PipelineService.run_pipelines()
