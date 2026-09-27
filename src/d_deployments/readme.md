# Deployment Concept

## Create a Deployment

1. **Create a Deployment Using the CLI**:
   You can create a deployment for this flow using the Prefect CLI. First, navigate to the directory containing your flow script and run the following command:

   ```bash
   prefect deploy
   ```

```bash
(intro-to-prefect) lokhandeganesh@SrcCode:~/workspace/intro-to-prefect/src/d_deployments$ prefect deploy
Unable to read the specified config file. Reason: [Errno 2] No such file or directory: 'prefect.yaml'.
Skipping.
? Select a flow to deploy [Use arrows to move; enter to select; n to select none]
┏━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃    ┃ Flow Name         ┃ Location                         ┃
┡━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ >  │ user_account_flow │ user_flow.py                     │
│    │                   │ Enter a flow entrypoint manually │
└────┴───────────────────┴──────────────────────────────────┘
? Deployment name (default):
? Which work pool would you like to deploy this flow to? [Use arrows to move; enter to select]
┏━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┓
┃   ┃ Work Pool Name ┃ Infrastructure Type ┃ Description ┃
┡━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━┩
│ > │ default        │ process             │ None        │
└───┴────────────────┴─────────────────────┴─────────────┘
? Your Prefect workers will need access to this flow's code in order to run it. Would you like your workers to
pull your flow code from a remote storage location when running this flow? [y/n] (y): n
Your Prefect workers will attempt to load your flow from:
/home/lokhandeganesh/workspace/intro-to-prefect/src/d_deployments/user_flow.py. To see more options for
managing your flow's code, run:

        $ prefect init

? Would you like to configure schedules for this deployment? [y/n] (y): n
╭─────────────────────────────────────────────────────────────────────────────────╮
│ Deployment 'user-account-flow/default' successfully created with id             │
│ '1f825963-892e-4e25-bfd2-fb9271dd7ec2'.                                         │
╰─────────────────────────────────────────────────────────────────────────────────╯

View Deployment in UI: http://127.0.0.1:4200/deployments/deployment/1f825963-892e-4e25-bfd2-fb9271dd7ec2


? Would you like to save configuration for this deployment for faster deployments in the future? [y/n]: y

Deployment configuration saved to prefect.yaml! You can now deploy using this deployment configuration with:

        $ prefect deploy -n default

You can also make changes to this deployment configuration by making changes to the YAML file.

To execute flow runs from these deployments, start a worker in a separate terminal that pulls work from the None work pool:

        $ prefect worker start --pool None

To schedule a run for this deployment, use the following command:

        $ prefect deployment run 'user-account-flow/default'
```

## Key Points to consider for Prefect Deployments

- **Deployments**: A way to wrap your flow with necessary metadata (like schedules, parameters, etc.) to manage and execute it remotely.
- **Parameterized Flows**: These allow you to pass in dynamic values during execution, which can be defined during the deployment creation or when triggering the flow.
- **Schedules and Triggers**: You can set deployments to run at specific times or in response to events. This is handled via work pools and the scheduling configuration of the deployment.

## Example Use Case

By creating this deployment, you can run the `user_account_flow` from the Prefect UI or CLI, adjusting the `user_id` dynamically each time you run it. This setup is particularly useful when you need to schedule regular flow executions or trigger flows based on external events.
