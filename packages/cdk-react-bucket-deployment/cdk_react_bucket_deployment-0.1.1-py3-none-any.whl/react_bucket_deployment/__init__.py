import subprocess

from pathlib import Path
from typing import Any

from aws_cdk.aws_s3 import IBucket
from aws_cdk.aws_s3_deployment import BucketDeployment
from aws_cdk.aws_s3_deployment import Source
from constructs import Construct


class ReactBucketDeployment(BucketDeployment):
    """
    A custom AWS CDK BucketDeployment that builds a React project using npm and deploys it to an S3 bucket.

    This class handles the process of installing dependencies, building the React project,
    and deploying the build artifacts to an S3 bucket. It is designed for React projects
    that use npm for dependency management.

    Prerequisites:
    - Node.js must be installed in the environment where the CDK app is executed.
        For installation instructions, refer to: https://nodejs.org/en


    Example:
        Below is an example of how to use the `ReactBucketDeployment` within an AWS CDK Stack:

        ```python
        from aws_cdk import Stack
        from aws_cdk.aws_s3 import Bucket
        from constructs import Construct
        from react_asset_code import ReactBucketDeployment

        class MyReactAppStack(Stack):
            def __init__(self, scope: Construct, id: str, **kwargs):
                super().__init__(scope, id, **kwargs)

                bucket = Bucket(self, "MyReactAppBucket")

                ReactBucketDeployment(
                    self, "DeployReactApp",
                    react_project_path="./path/to/react/project",
                    destination_bucket=bucket
                )
        ```
    """

    def __init__(
        self,
        scope: Construct,
        id: str,
        sources: str,
        destination_bucket: IBucket,
        **kwargs: Any,
    ) -> None:
        """
        Args:
            :param scope: The scope in which to define this construct.
            :param id: The scoped construct ID.
            :param sources (str): The file system path to the React project.
            :param destination_bucket: The S3 bucket where the React application will be deployed.
            > Please see the parent class _init__ for information about other params.
        """
        src_path = Path(sources)
        node_build_path = src_path / "build"
        self._build_react_project(src_path)
        super().__init__(
            scope,
            id,
            sources=[Source.asset(str(node_build_path))],
            destination_bucket=destination_bucket,
            **kwargs,
        )

    @staticmethod
    def _build_react_project(project_path: Path) -> None:
        subprocess.run(["npm", "ci"], check=True, cwd=project_path)
        subprocess.run(["npm", "run", "build"], check=True, cwd=project_path)
