import random

import pytest
from cdktf import Testing

from src.terrajinja.sbp.backend.s3_backend import SbpBackendS3Backend
from .helper import stack, has_backend


class TestSbpVault:
    def test_json_formatting(self, stack):
        SbpBackendS3Backend(
            scope=stack,
            _ns="sbp_backend_s3",
            bucket="test-bucket",
            key="test-key"
        )
        synthesized = Testing.synth(stack)

        has_backend(synthesized, "backend")


if __name__ == "__main__":
    pytest.main()
