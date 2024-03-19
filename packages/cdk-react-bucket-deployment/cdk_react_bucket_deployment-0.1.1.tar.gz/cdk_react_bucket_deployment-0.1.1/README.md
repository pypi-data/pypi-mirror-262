# ReactBucketDeployment for AWS CDK

A custom AWS CDK construct that integrates node for building react projects, automating the process of dependency resolution, packaging, and deployment preparation to AWS S3.

## Features

- Automates the build process of React applications using `npm`.
- Deploys the built React application to an AWS S3 bucket for hosting.
- Handles dependency resolution and packaging with `npm ci` and `npm run build`.
- Easily integrates with AWS CDK projects, providing a seamless deployment workflow.


## Prerequisites

- [Python 3.x](https://www.python.org/downloads/)
- [AWS CDK](https://github.com/aws/aws-cdk)
- [Node.js](https://nodejs.org/en)

## Installation

To use ReactBucketDeployment in your CDK project, install it via pip:

```bash
pip install cdk-react-bucket-deployment
```

## Usage
Here's a basic example of how to use ReactBucketDeployment in your AWS CDK stack:

```python
from aws_cdk import Stack
from aws_cdk.aws_s3 import Bucket
from constructs import Construct
from react_bucket_deployment import ReactBucketDeployment

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

Replace ./path/to/react/project with the path to your React project directory.

## Configuration

The ReactBucketDeployment construct accepts the following parameters:

- `scope`: The scope in which to define this construct (usually self in the context of a stack).
- `id`: The scoped construct ID.
- `react_project_path`: The file system path to the React project directory.
- `destination_bucket`: The S3 bucket instance where the React application will be deployed.

Additional AWS CDK BucketDeployment options can be passed through **kwargs to customize the deployment behavior further.


## Local Development

This project uses [Poetry](https://python-poetry.org/) for dependency management and packaging, and it's recommended to use Poetry to run local development tasks to ensure consistency with the project's dependencies.

### Running tests
All the tests are based on [pytest](https://docs.pytest.org/) so running them boils down to executing one command:
```shell
poetry run pytest
```

### Running Pre-commit Hooks

The project uses pre-commit hooks to ensure code quality and formatting standards. To set up pre-commit hooks within the Poetry environment, which ensures that the hooks are run automatically before each commit, execute the following command:

```bash
poetry run pre-commit install
```

This command installs pre-commit hooks as Git pre-commit hooks, so they are automatically executed before you commit changes. It's a convenient way to ensure your changes adhere to the project's standards without needing to manually run checks before each commit.

If you prefer to run pre-commit hooks manually, perhaps to check files before committing, you can use the following command:
```bash
poetry run pre-commit run --all-files
```
This will manually execute all configured pre-commit hooks on all files in the repository. It's useful for performing a one-time check or for scenarios where you haven't set up automatic pre-commit hooks with pre-commit install.


### Running Pyright
Pyright is used for static type checking to catch errors early in development. To run Pyright through Poetry, use the following command:

bash
```
poetry run pyright
```

This will execute Pyright type checking based on the project's pyrightconfig.json configuration. Running Pyright helps ensure type consistency and can catch common errors.


## Contributing
- Submitting bug reports and feature requests in the Issues section.
- Opening pull requests with improvements to code or documentation.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.

## Acknowledgments
- Thanks to the AWS CDK team for providing the framework.
- Thanks to the Poetry team for simplifying Python package management.
