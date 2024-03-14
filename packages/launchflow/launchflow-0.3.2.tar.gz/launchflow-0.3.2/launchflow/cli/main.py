import asyncio
import os
from typing import Optional

import beaupy
import rich
import typer
import uvloop
from launchflow.cli import project_gen
from launchflow.cli.accounts import account_commands
from launchflow.cli.cloud import cloud_commands
from launchflow.cli.config import config_commands
from launchflow.cli.contants import ENVIRONMENT_HELP, PROJECT_HELP, SERVICE_HELP
from launchflow.cli.environments import environment_commands
from launchflow.cli.project import project_commands
from launchflow.cli.resources import resource_commands
from launchflow.cli.resources_ast import find_launchflow_resources
from launchflow.cli.templates import (
    dockerfile_template,
    infra_dot_py_template,
    main_template,
)
from launchflow.cli.utils import tar_source_in_memory
from launchflow.cli.utyper import UTyper
from launchflow.clients.client import LaunchFlowAsyncClient
from launchflow.clients.response_schemas import EnvironmentResponse, ProjectResponse
from launchflow.config import config
from launchflow.config.launchflow_yaml import LaunchFlowDotYaml, ServiceConfig
from launchflow.exceptions import LaunchFlowRequestFailure
from launchflow.flows.auth import login_flow, logout_flow
from launchflow.flows.environments_flows import get_environment
from launchflow.flows.project_flows import get_project
from launchflow.flows.resource_flows import clean as clean_resources
from launchflow.flows.resource_flows import create as create_resources
from launchflow.flows.resource_flows import import_resources
from rich.progress import Progress, SpinnerColumn, TextColumn

from launchflow.clients import async_launchflow_client_ctx

app = UTyper(help="LaunchFlow CLI.")
app.add_typer(account_commands.app, name="accounts")
app.add_typer(project_commands.app, name="projects")
app.add_typer(environment_commands.app, name="environments")
app.add_typer(cloud_commands.app, name="cloud")
app.add_typer(resource_commands.app, name="resources")
app.add_typer(config_commands.app, name="config")


_SCAN_DIRECTORY_HELP = (
    "Directory to scan for resources. Defaults to the current working directory."
)

_CWD_HELP = (
    "Directory to run automations from. Defaults to the current working directory."
)


async def _get_project_info(
    client: LaunchFlowAsyncClient,
    project_name: Optional[str] = None,
    prompt_for_creation: bool = True,
):
    # This check replaces the cli project arg with the configured project (if set)
    if project_name is None:
        project_name = config.project
    # Fetches the latest project info from the server
    return await get_project(
        client, project_name=project_name, prompt_for_creation=prompt_for_creation
    )


async def _get_environment_info(
    client: LaunchFlowAsyncClient,
    project: ProjectResponse,
    environment_name: Optional[str] = None,
    prompt_for_creation: bool = True,
):
    # This check replaces the cli env arg with the configured environment (if set)
    if environment_name is None:
        environment_name = config.environment
    # Fetches the latest environment info from the server
    return await get_environment(
        client=client,
        project=project,
        environment_name=environment_name,
        prompt_for_creation=prompt_for_creation,
    )


def _get_service_info(
    project: ProjectResponse,
    environment: EnvironmentResponse,
    service_name: Optional[str] = None,
    prompt_for_creation: bool = True,
):
    service_configs = config.list_service_configs()
    if service_name is not None:
        for service in service_configs:
            if service.name == service_name:
                return service
        raise ValueError(f"Service `{service_name}` not found in launchflow.yaml.")
    if len(service_configs) == 1:
        return service_configs[0]
    # TODO: Add a flow to help the user update their launchflow.yaml
    # Consider using the project / env info to filter the service options
    # i.e. a gcp project should recommend cloud run service options
    raise ValueError("No services configured in launchflow.yaml.")


@app.command()
async def init(
    directory: str = typer.Argument(None, help="Directory to initialize launchflow."),
    account_id: str = typer.Option(
        None,
        help="Account ID to use for this project. Defaults to the account ID set in the config.",
    ),
):
    """Initialize a new launchflow project."""
    async with async_launchflow_client_ctx() as client:
        try:
            project = await project_gen.project(client, account_id)
            environment = await get_environment(
                client=client,
                project=project,
                environment_name=None,
                prompt_for_creation=True,
            )
        except Exception as e:
            typer.echo(e)
            raise typer.Exit(1)

        if not directory:
            relative_path = project.name
            full_directory_path = os.path.join(os.path.abspath("."), relative_path)
        else:
            relative_path = directory
            full_directory_path = os.path.abspath(relative_path)
        while os.path.exists(full_directory_path):
            typer.echo(f"Directory `{full_directory_path}` already exists.")
            directory_name = beaupy.prompt("Enter a directory name for your project:")
            full_directory_path = os.path.join(
                os.path.abspath(directory), directory_name
            )

        framework = project_gen.framework()
        resources = project_gen.resources()
        infra = infra_dot_py_template.template(project.name, framework, resources)
        requirements = project_gen.requirements(framework, resources)
        dockerfile = dockerfile_template.template(framework)
        if "aws" in project.configured_cloud_providers:
            product = "aws_ecs_fargate"
        elif "gcp" in project.configured_cloud_providers:
            product = "gcp_cloud_run"
        services = [ServiceConfig(name="fastapi-service", product=product)]
        launchflow_dot_yaml = LaunchFlowDotYaml(
            project.name, environment.name, services
        )
        main = main_template.template(framework, resources)

        app_directory_path = os.path.join(full_directory_path, "app")
        os.makedirs(app_directory_path)

        # App level files
        infra_py = os.path.join(app_directory_path, "infra.py")
        main_py = os.path.join(app_directory_path, "main.py")
        # Top level files
        requirements_txt = os.path.join(full_directory_path, "requirements.txt")
        dockerfile_path = os.path.join(full_directory_path, "Dockerfile")
        launchflow_yaml_path = os.path.join(full_directory_path, "launchflow.yaml")

        with open(infra_py, "w") as f:
            f.write(infra)

        with open(main_py, "w") as f:
            f.write(main)

        with open(requirements_txt, "w") as f:
            f.write(requirements + "\n")

        with open(dockerfile_path, "w") as f:
            f.write(dockerfile)

        launchflow_dot_yaml.save_to_file(launchflow_yaml_path)

        print()
        print("Done!")
        print()
        print("Navigate to your project directory:")
        rich.print(f"  $ [green]cd {relative_path}")
        print()
        print("To create your resources run:")
        rich.print("  $ [green]launchflow create")
        print()
        print("To build and deploy your app remotely run:")
        rich.print("  $ [green]launchflow deploy")
        print()
        print("To run all of the above in one command run:")
        rich.print("  $ [green]launchflow launch")


@app.command()
async def create(
    resource: str = typer.Argument(
        None,
        help="Resource to create. If none we will scan the directory for resources.",
    ),
    project: Optional[str] = typer.Option(None, help=PROJECT_HELP),
    environment: Optional[str] = typer.Option(None, help=ENVIRONMENT_HELP),
    scan_directory: str = typer.Option(".", help=_SCAN_DIRECTORY_HELP),
):
    """Create any resources that are not already created."""
    try:
        async with async_launchflow_client_ctx() as client:
            project_info = await _get_project_info(client, project)
            environment_info = await _get_environment_info(
                client, project_info, environment
            )

            if resource is None:
                resources = find_launchflow_resources(scan_directory)
            else:
                resources = [resource]

            await create_resources(
                project_info.name,
                environment_info.name,
                *import_resources(resources),
            )

    except LaunchFlowRequestFailure as e:
        e.pretty_print()
        raise typer.Exit(1)


@app.command()
async def clean(
    scan_directory: str = typer.Option(".", help=_SCAN_DIRECTORY_HELP),
    project: Optional[str] = typer.Option(None, help=PROJECT_HELP),
    environment: Optional[str] = typer.Option(None, help=ENVIRONMENT_HELP),
):
    """Clean up any resources that are not in the current directory but are part of the project / environment."""
    try:
        async with async_launchflow_client_ctx() as client:
            project_info = await _get_project_info(client, project)
            environment_info = await _get_environment_info(
                client, project_info, environment
            )

            resources = find_launchflow_resources(scan_directory)
            await clean_resources(
                project_info.name,
                environment_info.name,
                *import_resources(resources),
            )

    except LaunchFlowRequestFailure as e:
        e.pretty_print()
        raise typer.Exit(1)


@app.command(hidden=True)
async def deploy(
    cwd: str = typer.Option(".", help=_CWD_HELP),
    project: Optional[str] = typer.Option(None, help=PROJECT_HELP),
    environment: Optional[str] = typer.Option(None, help=ENVIRONMENT_HELP),
    service: Optional[str] = typer.Option(None, help=SERVICE_HELP),
):
    async with async_launchflow_client_ctx() as client:
        try:
            project_info = await _get_project_info(client, project)
            environment_info = await _get_environment_info(
                client, project_info, environment
            )
            service_info = _get_service_info(project_info, environment_info, service)

            service_ref = (
                f'Service(name="{service_info.name}", product="{service_info.product}")'
            )

            answer = beaupy.confirm(
                f"Deploy {service_ref} to `{project_info.name}/{environment_info.name}`?",
                default_is_yes=True,
            )
            if not answer:
                print("User cancelled deployment. Exiting.")
                return
            else:
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                ) as progress:
                    bundle_task = progress.add_task(
                        "Bundling service files...", total=None
                    )
                    tar_bytes = tar_source_in_memory(directory=cwd)
                    progress.remove_task(bundle_task)

                    # TODO: List out the infra changes that will be made in the user's
                    # account, like creating the docker repo, docker image, cloud run service, etc.

                    # TODO: Add a way to notify the user of build progress

                    # TODO: (maybe) add a ETA for the build
                    deploy_task = progress.add_task(
                        f"Deploying {service_ref}...", total=None
                    )
                    operation = await client.services.deploy(
                        project_name=project_info.name,
                        environment_name=environment_info.name,
                        product_name=service_info.product,
                        service_name=service_info.name,
                        tar_bytes=tar_bytes,
                        create_args=service_info.product_config.to_dict(),
                    )
                    async for status in client.operations.stream_operation_status(
                        operation.id
                    ):
                        if status.is_error():
                            progress.remove_task(deploy_task)
                            progress.console.print(
                                f"[red]✗[/red] Deployment failed for [blue]{service_ref}[/blue]"
                            )
                            raise typer.Exit(1)
                        elif status.is_cancelled():
                            progress.remove_task(deploy_task)
                            progress.console.print(
                                f"[yellow]✗[/yellow] Deployment cancelled for [blue]{service_ref}[/blue]"
                            )
                            raise typer.Exit(1)
                        elif status.is_success():
                            progress.remove_task(deploy_task)
                            progress.console.print(
                                f"[green]✓[/green] Deployment successful for [blue]{service_ref}[/blue]"
                            )
                            break

        except LaunchFlowRequestFailure as e:
            e.pretty_print()
            raise typer.Exit(1)


@app.command()
async def login():
    """Login to LaunchFlow. If you haven't signup this will create a free account for you."""
    try:
        async with async_launchflow_client_ctx() as client:
            await login_flow(client)
    except Exception as e:
        typer.echo(f"Failed to login. {e}")
        typer.Exit(1)


@app.command()
def logout():
    """Logout of LaunchFlow."""
    try:
        logout_flow()
    except Exception as e:
        typer.echo(f"Failed to logout. {e}")
        typer.Exit(1)


@app.command()
async def async_test():
    await asyncio.sleep(1)
    print("Done.")


if __name__ == "__main__":
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    app()
