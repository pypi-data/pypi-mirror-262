from cdktf import S3Backend
from constructs import Construct


class SbpBackendS3Backend(S3Backend):
    """SBP version of cdktf.S3Backend"""

    def __init__(self, scope: Construct, _ns: str, **kwargs):
        """Does very little, it is just an overlay for including the s3 backend as a resource"""

        # call the original resource
        super().__init__(
            scope=scope,
            **kwargs,
        )
