idmc
====

Informatica Cloud CLI Utility

**Getting Started**

    Run the below command to configure the credentials and the pod details that should be used when connecting to IDMC. You will be asked to enter the username, password, pod (e.g. "usw1") and region (e.g. "dm-us").
    
    idmc configure

**Usage:**

    idmc [OPTIONS] COMMAND [ARGS]...
    

**Options:**

      --help  Show this message and exit.
    

**Subcommands**

*   _agents_: Secure Agent management commands.
*   _configure_: Used to configure the global parameters for the CLI.
*   _folders_: Folder management commands.
*   _jobs_: Job management commands.
*   _login_: Used to login to Informatica Cloud and return the login details.
*   _logout_: Used to logout from Informatica Cloud.
*   _logs_: Log commands.
*   _lookup_: Lookup objects.
*   _objects_: Object management commands.
*   _orgs_: Organisation management commands.
*   _privileges_: Privilege management commands.
*   _projects_: Project management commands.
*   _roles_: Role management commands.
*   _schedules_: Schedule management commands.
*   _source-control_: Source control management commands.
*   _user-groups_: User group management commands.
*   _users_: User management commands.

agents
------

Secure Agent management commands.

**Usage:**

    idmc agents [OPTIONS] COMMAND [ARGS]...
    

**Options:**

      --help  Show this message and exit.
    

**Subcommands**

*   _delete_: Deletes a secure agent
*   _get_: Gets Secure Agents
*   _groups_: Secure Agent Group service management commands.
*   _service_: Secure Agent service management commands.
*   _status_: Gets Secure Agent Status

### delete

Deletes a secure agent

**Usage:**

    idmc agents delete [OPTIONS]
    

**Options:**

      -i, --id TEXT     Secure Agent ID. Either this option or the name option
                        must be included.
      -n, --name TEXT   Secure Agent Name. Either this option or the id option
                        must be included.
      -u, --unassigned  Flag to include a list of all the Secure Agents that are
                        currently not assigned to any group.
      -D, --debug       If true, will print the API request details to console.
      -P, --pretty      If true, will pretty print the returned JSON.
      --help            Show this message and exit.
    

### get

Gets Secure Agents

**Usage:**

    idmc agents get [OPTIONS]
    

**Options:**

      -i, --id TEXT     Secure Agent ID. If searching for a specific agent, either
                        this option or the name option must be included.
      -n, --name TEXT   Secure Agent Name. If searching for a specific agent,
                        either this option or the id option must be included.
      -u, --unassigned  Flag to include a list of all the Secure Agents that are
                        currently not assigned to any group.
      -D, --debug       If true, will print the API request details to console.
      -P, --pretty      If true, will pretty print the returned JSON.
      --help            Show this message and exit.
    

### groups

Secure Agent Group service management commands.

**Usage:**

    idmc agents groups [OPTIONS] COMMAND [ARGS]...
    

**Options:**

      --help  Show this message and exit.
    

**Subcommands**

*   _add-agent_: Add one or more agents to a secure agent group
*   _components_: Secure Agent Group component management commands.
*   _create_: Creates a secure agent group
*   _delete_: Deletes a secure agent group
*   _get_: Gets Secure Agent Groups
*   _properties_: Secure Agent Group property management commands.

#### add-agent

Add one or more agents to a secure agent group

**Usage:**

    idmc agents groups add-agent [OPTIONS]
    

**Options:**

      -gi, --group-id TEXT    Secure Agent Group ID. Either this option or the
                              group-name option must be included.
      -gn, --group-name TEXT  Secure Agent Group Name. Either this option or the
                              group-id option must be included.
      -ai, --agent-id TEXT    Secure Agent ID. Either this option or the agent-
                              name option must be included. This option can be
                              repeated to add multiple agents.
      -an, --agent-name TEXT  Secure Agent Name. Either this option or the agent-
                              id option must be included. This option can be
                              repeated to add multiple agents.
      -D, --debug             If true, will print the API request details to
                              console.
      -P, --pretty            If true, will pretty print the returned JSON.
      --help                  Show this message and exit.
    

#### components

Secure Agent Group component management commands.

**Usage:**

    idmc agents groups components [OPTIONS] COMMAND [ARGS]...
    

**Options:**

      --help  Show this message and exit.
    

**Subcommands**

*   _get_: Gets Secure Agent Group components
*   _update_: Can be used to enable or disable Secure Agent Group components

##### get

Gets Secure Agent Group components

**Usage:**

    idmc agents groups components get [OPTIONS]
    

**Options:**

      -i, --id TEXT      Secure Agent Group ID. Either this option or the name
                         option must be included.
      -n, --name TEXT    Secure Agent Group Name. Either this option or the id
                         option must be included.
      -a, --include-all  Flag to include disabled components in the response.
      -D, --debug        If true, will print the API request details to console.
      -P, --pretty       If true, will pretty print the returned JSON.
      --help             Show this message and exit.
    

##### update

Can be used to enable or disable Secure Agent Group components

**Usage:**

    idmc agents groups components update [OPTIONS]
    

**Options:**

      -i, --id TEXT          Secure Agent Group ID. Either this option or the name
                             option must be included.
      -n, --name TEXT        Secure Agent Group Name. Either this option or the id
                             option must be included.
      -e, --enable           Flag to enable components. Use this flag or the
                             disable flag.
      -d, --disable          Flag to disable components. Use this flag or the
                             enable flag.
      -s, --services TEXT    Service to be updated. Can be repeated for multiple
                             services.
      -c, --connectors TEXT  Connector to be updated. Can be repeated for multiple
                             connectors.
      -a, --additional TEXT  Additional service to be updated. Can be repeated for
                             multiple additional services.
      -D, --debug            If true, will print the API request details to
                             console.
      -P, --pretty           If true, will pretty print the returned JSON.
      --help                 Show this message and exit.
    

#### create

Creates a secure agent group

**Usage:**

    idmc agents groups create [OPTIONS]
    

**Options:**

      -n, --name TEXT  Secure Agent Group Name.
      -s, --shared     Flag whether the Secure Agent group can be shared with sub-
                       organizations.
      -D, --debug      If true, will print the API request details to console.
      -P, --pretty     If true, will pretty print the returned JSON.
      --help           Show this message and exit.
    

#### delete

Deletes a secure agent group

**Usage:**

    idmc agents groups delete [OPTIONS]
    

**Options:**

      -i, --id TEXT    Secure Agent Group ID. Either this option or the name
                       option must be included.
      -n, --name TEXT  Secure Agent Group Name. Either this option or the id
                       option must be included.
      -D, --debug      If true, will print the API request details to console.
      -P, --pretty     If true, will pretty print the returned JSON.
      --help           Show this message and exit.
    

#### get

Gets Secure Agent Groups

**Usage:**

    idmc agents groups get [OPTIONS]
    

**Options:**

      -i, --id TEXT    Secure Agent Group ID. If searching for a specific group,
                       use either this option or the name option.
      -n, --name TEXT  Secure Agent Group Name. If searching for a specific group,
                       use either this option or the id option.
      -D, --debug      If true, will print the API request details to console.
      -P, --pretty     If true, will pretty print the returned JSON.
      --help           Show this message and exit.
    

#### properties

Secure Agent Group property management commands.

**Usage:**

    idmc agents groups properties [OPTIONS] COMMAND [ARGS]...
    

**Options:**

      --help  Show this message and exit.
    

**Subcommands**

*   _delete_: Deletes Secure Agent Group properties
*   _get_: Gets Secure Agent Group properties
*   _update_: Updates Secure Agent Group properties

##### delete

Deletes Secure Agent Group properties

**Usage:**

    idmc agents groups properties delete [OPTIONS]
    

**Options:**

      -i, --id TEXT    Secure Agent Group ID. Either this option or the name
                       option must be included.
      -n, --name TEXT  Secure Agent Group Name. Either this option or the id
                       option must be included.
      -D, --debug      If true, will print the API request details to console.
      -P, --pretty     If true, will pretty print the returned JSON.
      --help           Show this message and exit.
    

##### get

Gets Secure Agent Group properties

**Usage:**

    idmc agents groups properties get [OPTIONS]
    

**Options:**

      -i, --id TEXT        Secure Agent Group ID. Either this option or the name
                           option must be included.
      -n, --name TEXT      Secure Agent Group Name. Either this option or the id
                           option must be included.
      -s, --service TEXT   Filter result by service name.
      -t, --type TEXT      Filter result by property type. Must be used in
                           conjunction with the service option.
      -k, --property TEXT  Filter result by property name. Must be used in
                           conjunction with the service and type options.
      -o, --overridden     Flag to show properties that have been overridden at
                           the secure agent group level.
      -p, --platform TEXT  Optionally, include the platform in the URI. You can
                           use linux64 or win64.
      -D, --debug          If true, will print the API request details to console.
      -P, --pretty         If true, will pretty print the returned JSON.
      --help               Show this message and exit.
    

##### update

Updates Secure Agent Group properties

**Usage:**

    idmc agents groups properties update [OPTIONS]
    

**Options:**

      -i, --id TEXT        Secure Agent Group ID. Either this option or the name
                           option must be included.
      -n, --name TEXT      Secure Agent Group Name. Either this option or the id
                           option must be included.
      -s, --service TEXT   Service to be updated.  [required]
      -t, --type TEXT      Property type to be updated.  [required]
      -k, --property TEXT  Property name to be updated.  [required]
      -v, --value TEXT     New property value.  [required]
      -p, --platform TEXT  Optionally, include the platform in the URI. You can
                           use linux64 or win64.
      -c, --custom         Flag to indicate if property is a custom property.
      -S, --sensitive      Flag to indicate if property is a sensitive property
                           and should be masked.
      -D, --debug          If true, will print the API request details to console.
      -P, --pretty         If true, will pretty print the returned JSON.
      --help               Show this message and exit.
    

### service

Secure Agent service management commands.

**Usage:**

    idmc agents service [OPTIONS] COMMAND [ARGS]...
    

**Options:**

      --help  Show this message and exit.
    

**Subcommands**

*   _start_: Starts a service on a secure agent
*   _stop_: Stops a service on a secure agent

#### start

Starts a service on a secure agent

**Usage:**

    idmc agents service start [OPTIONS]
    

**Options:**

      -i, --id TEXT       Runtime environment ID. Either this option or the name
                          option must be included.
      -n, --name TEXT     Runtime environment Name. Either this option or the id
                          option must be included.
      -s, --service TEXT  Service to be started on the runtime environment.
                          [required]
      -D, --debug         If true, will print the API request details to console.
      -P, --pretty        If true, will pretty print the returned JSON.
      --help              Show this message and exit.
    

#### stop

Stops a service on a secure agent

**Usage:**

    idmc agents service stop [OPTIONS]
    

**Options:**

      -i, --id TEXT       Runtime environment ID. Either this option or the name
                          option must be included.
      -n, --name TEXT     Runtime environment Name. Either this option or the id
                          option must be included.
      -s, --service TEXT  Service to be stopped on the runtime environment.
                          [required]
      -D, --debug         If true, will print the API request details to console.
      -P, --pretty        If true, will pretty print the returned JSON.
      --help              Show this message and exit.
    

### status

Gets Secure Agent Status

**Usage:**

    idmc agents status [OPTIONS]
    

**Options:**

      -i, --id TEXT    Secure Agent ID. Either this option or the name option must
                       be included.
      -n, --name TEXT  Secure Agent Name. Either this option or the id option must
                       be included.
      -D, --debug      If true, will print the API request details to console.
      -P, --pretty     If true, will pretty print the returned JSON.
      --help           Show this message and exit.
    

configure
---------

Used to configure the global parameters for the CLI.

**Usage:**

    idmc configure [OPTIONS]
    

**Options:**

      --help  Show this message and exit.
    

folders
-------

Folder management commands.

**Usage:**

    idmc folders [OPTIONS] COMMAND [ARGS]...
    

**Options:**

      --help  Show this message and exit.
    

**Subcommands**

*   _create_: Creates a folder
*   _delete_: Deletes a folder
*   _update_: Updates a folder

### create

Creates a folder

**Usage:**

    idmc folders create [OPTIONS]
    

**Options:**

      -pi, --project-id TEXT    ID for the parent project. Use this option or
                                --project_name.
      -pn, --project-name TEXT  Name for the parent project. Use this option or
                                --project-id.
      -n, --name TEXT           Name for the new folder  [required]
      -d, --description TEXT    Description for the new folder
      -D, --debug               If true, will print the API request details to
                                console.
      -P, --pretty              If true, will pretty print the returned JSON.
      --help                    Show this message and exit.
    

### delete

Deletes a folder

**Usage:**

    idmc folders delete [OPTIONS]
    

**Options:**

      -i, --id TEXT    ID for the folder to be deleted. Use this option or --path.
      -p, --path TEXT  Path of the folder to be deleted. Use this option or --id.
      -D, --debug      If true, will print the API request details to console.
      -P, --pretty     If true, will pretty print the returned JSON.
      --help           Show this message and exit.
    

### update

Updates a folder

**Usage:**

    idmc folders update [OPTIONS]
    

**Options:**

      -i, --id TEXT           ID for the folder to be updated. Use this option or
                              --path.
      -p, --path TEXT         Path of the folder to be updated. Use this option or
                              --id.
      -n, --name TEXT         New name for the folder.
      -d, --description TEXT  New description for the folder.
      -D, --debug             If true, will print the API request details to
                              console.
      -P, --pretty            If true, will pretty print the returned JSON.
      --help                  Show this message and exit.
    

jobs
----

Job management commands.

**Usage:**

    idmc jobs [OPTIONS] COMMAND [ARGS]...
    

**Options:**

      --help  Show this message and exit.
    

**Subcommands**

*   _exp_: WARNING: Experimental unsupported job management commands.
*   _start_: Starts a job
*   _stop_: Stops running jobs

### exp

WARNING: Experimental unsupported job management commands.

**Usage:**

    idmc jobs exp [OPTIONS] COMMAND [ARGS]...
    

**Options:**

      --help  Show this message and exit.
    

**Subcommands**

*   _get_: Get job details from the monitor

#### get

Get job details from the monitor

**Usage:**

    idmc jobs exp get [OPTIONS]
    

**Options:**

      -n, --name TEXT          Filter the jobs by name.
      -s, --status TEXT        Comma separated list of statuses for the tasks. You
                               can filter by any of the following statuses:
                               'ABORTED', 'AWAITING_AUTO_RESTART',
                               'CHILD_SUSPENDED', 'COMPLETED', 'DEPLOYED',
                               'DEPLOYING', 'ERROR', 'FAILED', 'INITIALIZED',
                               'NOT_STARTED', 'PROCESSING_ABORT',
                               'PROCESSING_DEPLOY', 'PROCESSING_STOP',
                               'PROCESSING_UNDEPLOY', 'QUEUED', 'RUNNING',
                               'SKIPPED', 'STOPPED', 'SUBMITTED', 'SUCCESS',
                               'SUSPENDED', 'TRYING_TO_STOP', 'UNDEPLOYED',
                               'UNDEPLOYING', 'WARNING'
      -t, --type TEXT          Type of asset. You can filter by any of the
                               following types: 'API', 'APPMI_TASK',
                               'AS2_RECEIVE', 'AS2_SEND', 'BATCH_MAPPING',
                               'CodeTask', 'command', 'DBMI_GROUP_TASK',
                               'DBMI_TASK', 'DLT', 'DMASK', 'DRS', 'DSS', 'DTT',
                               'EXCEPTION', 'FILE_TRANSFER_TASK', 'FTP_CLIENT',
                               'FTPS_CLIENT', 'HTTPS_SERVER', 'MAPPING',
                               'MI_FILE_LISTENER', 'MI_TASK', 'MLLP_SERVER',
                               'MTT', 'MTT_DP', 'MTT_DP_CDIE', 'MTT_PDO',
                               'MTT_TEST', 'PCS', 'PROFILE', 'SFTP_CLIENT',
                               'SFTP_SERVER', 'SI_DATAFLOW', 'TASKFLOW',
                               'TunerTask', 'WORKFLOW'.
      -o, --order-by TEXT      Sort order in which to return the data. Ascending
                               by default. Include "desc" after order by field if
                               needed.
      -l, --location TEXT      Filter the jobs by project/folder location.
      -e, --error TEXT         Filter the jobs by error messages that contain this
                               value.
      -r, --runtime TEXT       Filter the jobs by the name of the runtime
                               environment.
      -ss, --start-since TEXT  Date and time the task started since.
      -su, --start-until TEXT  Date and time the task started until.
      -es, --end-since TEXT    Date and time the task ended since.
      -eu, --end-until TEXT    Date and time the task ended until.
      -D, --debug              If true, will print the API request details to
                               console.
      -P, --pretty             If true, will pretty print the returned JSON.
      --help                   Show this message and exit.
    

### start

Starts a job

**Usage:**

    idmc jobs start [OPTIONS]
    

**Options:**

      -i, --ids TEXT             Comma separated list of global unique identifier
                                 for the task to start. Must be used if path is
                                 not included.
      -p, --paths TEXT           Comma separated list of paths to the task to be
                                 started. Supports the '*' (matches everything)
                                 and '?' (matches any single character) wildcard
                                 characters.
      -t, --type TEXT            The type of task. Valid values include: DMASK,
                                 DRS, DSS, MTT, PCS, WORKFLOW, TASKFLOW. The
                                 taskflow must be first published.  [required]
      -c, --callback TEXT        URL endpoint to be called when the job is
                                 finished.
      -f, --param-file TEXT      Parameter file name. Must be used in conjunction
                                 with the param-dir option.
      -d, --param-dir TEXT       Parameter file directory on the Secure Agent
                                 machine. Must be used in conjunction with the
                                 param-file option.
      -a, --api-names TEXT       Comma separated list of API names for the
                                 taskflows to be executed.
      -w, --wait                 Flag to wait for all jobs to finish.
      -pd, --poll-delay INTEGER  Time in seconds to wait between job status
                                 polling when waiting for them to finish.
      -D, --debug                If true, will print the API request details to
                                 console.
      -P, --pretty               If true, will pretty print the returned JSON.
      --help                     Show this message and exit.
    

### stop

Stops running jobs

**Usage:**

    idmc jobs stop [OPTIONS]
    

**Options:**

      -i, --ids TEXT        Comma separated list of global unique identifiers for
                            the running jobs.
      -n, --names TEXT      Comma separated list of names of jobs to be stopped.
      -l, --locations TEXT  Comma separated list of locations of jobs to be
                            stopped.
      -t, --types TEXT      Comma separated list of types of jobs to be stopped.
                            Valid values include: DMASK, DRS, DSS, MTT, PCS,
                            WORKFLOW, TASKFLOW. The taskflow must be first
                            published.
      -c, --clean           Flag to indicate a clean stop of the job should be
                            executed. Not applicable for TASKFLOW types.
      -D, --debug           If true, will print the API request details to
                            console.
      -P, --pretty          If true, will pretty print the returned JSON.
      --help                Show this message and exit.
    

login
-----

Used to login to Informatica Cloud and return the login details.

**Usage:**

    idmc login [OPTIONS]
    

**Options:**

      -D, --debug   If true, will print the API request details to console.
      -P, --pretty  If true, will pretty print the returned JSON.
      --help        Show this message and exit.
    

logout
------

Used to logout from Informatica Cloud.

**Usage:**

    idmc logout [OPTIONS]
    

**Options:**

      -D, --debug   If true, will print the API request details to console.
      -P, --pretty  If true, will pretty print the returned JSON.
      --help        Show this message and exit.
    

logs
----

Log commands.

**Usage:**

    idmc logs [OPTIONS] COMMAND [ARGS]...
    

**Options:**

      --help  Show this message and exit.
    

**Subcommands**

*   _activity_: Activity log commands.
*   _security_: Gets the security logs

### activity

Activity log commands.

**Usage:**

    idmc logs activity [OPTIONS] COMMAND [ARGS]...
    

**Options:**

      --help  Show this message and exit.
    

**Subcommands**

*   _completed_: Gets the completed activity logs
*   _running_: Gets the running activity logs

#### completed

Gets the completed activity logs

**Usage:**

    idmc logs activity completed [OPTIONS]
    

**Options:**

      -i, --id TEXT       Log entry ID. Include this attribute if you want to
                          receive information for a specific ID.
      -r, --run-id TEXT   Job ID associated with the log entry ID. Whenever runId
                          is included in a request, taskId is required.
      -t, --task-id TEXT  Task ID associated with the log entry ID. If taskId is
                          not specified, all activityLog entries for all tasks are
                          returned.
      -n, --name TEXT     Name of the job.
      -D, --debug         If true, will print the API request details to console.
      -P, --pretty        If true, will pretty print the returned JSON.
      --help              Show this message and exit.
    

#### running

Gets the running activity logs

**Usage:**

    idmc logs activity running [OPTIONS]
    

**Options:**

      -i, --id TEXT       Log entry ID. Include this attribute if you want to
                          receive information for a specific ID.
      -r, --run-id TEXT   Job ID associated with the log entry ID. Whenever runId
                          is included in a request, taskId is required.
      -t, --task-id TEXT  Task ID associated with the log entry ID. If taskId is
                          not specified, all activityLog entries for all tasks are
                          returned.
      -n, --name TEXT     Name of the job.
      -D, --debug         If true, will print the API request details to console.
      -P, --pretty        If true, will pretty print the returned JSON.
      --help              Show this message and exit.
    

### security

Gets the security logs

**Usage:**

    idmc logs security [OPTIONS]
    

**Options:**

      -c, --category TEXT  Category of the security log entry.
      -a, --actor TEXT     User name who performed the action.
      -n, --name TEXT      Name of the object acted upon.
      -f, --from TEXT      Date/time to search from. The maximum date range is 14
                           days.
      -t, --to TEXT        Date/time to search until. The maximum date range is 14
                           days.
      -D, --debug          If true, will print the API request details to console.
      -P, --pretty         If true, will pretty print the returned JSON.
      --help               Show this message and exit.
    

lookup
------

Lookup objects.

**Usage:**

    idmc lookup [OPTIONS] COMMAND [ARGS]...
    

**Options:**

      --help  Show this message and exit.
    

**Subcommands**

*   _object_: Lookup a single object
*   _objects_: Lookup multiple objects

### object

Lookup a single object

**Usage:**

    idmc lookup object [OPTIONS]
    

**Options:**

      -i, --id TEXT    Global unique identifier for the object. Required if object
                       path and type not included.
      -p, --path TEXT  Full path of the object including project, folder, and
                       object name. Required with type if object ID not included.
      -t, --type TEXT  Type of object. Required with path if object ID not
                       included.
      -D, --debug      If true, will print the API request details to console.
      -P, --pretty     If true, will pretty print the returned JSON.
      --help           Show this message and exit.
    

### objects

Lookup multiple objects

**Usage:**

    idmc lookup objects [OPTIONS]
    

**Options:**

      -b, --body TEXT  JSON payload containing the search conditions for the
                       objects.  [required]
      -D, --debug      If true, will print the API request details to console.
      -P, --pretty     If true, will pretty print the returned JSON.
      --help           Show this message and exit.
    

objects
-------

Object management commands.

**Usage:**

    idmc objects [OPTIONS] COMMAND [ARGS]...
    

**Options:**

      --help  Show this message and exit.
    

**Subcommands**

*   _add-tags_: Adds one or more tags to an object
*   _dependencies_: Returns dependencies for an object
*   _get_: Used to get objects
*   _permissions_: Permission management commands.
*   _query_: Used to query objects
*   _remove-tags_: Removes one or more tags from an object

### add-tags

Adds one or more tags to an object

**Usage:**

    idmc objects add-tags [OPTIONS]
    

**Options:**

      -i, --id TEXT    Global unique identifier for the object. Required if object
                       path and type not included.
      -p, --path TEXT  Full path of the object including project, folder, and
                       object name. Required with type if object ID not included.
      -t, --type TEXT  Type of object. Required with path if object ID not
                       included.
      -b, --body TEXT  If tagging multiple objects, use this property to include
                       the JSON body. Only use this if not using --id, --path,
                       --type or --tags options.
      -T, --tags TEXT  Comma separated list of tags to be added to the object.
      -D, --debug      If true, will print the API request details to console.
      -P, --pretty     If true, will pretty print the returned JSON.
      --help           Show this message and exit.
    

### dependencies

Returns dependencies for an object

**Usage:**

    idmc objects dependencies [OPTIONS]
    

**Options:**

      -i, --id TEXT        Global unique identifier for the object. Required if
                           object path and type not included.
      -p, --path TEXT      Full path of the object including project, folder, and
                           object name. Required with type if object ID not
                           included.
      -t, --type TEXT      Type of object. Required with path if object ID not
                           included.
      -r, --ref-type TEXT  Whether to list objects that the asset uses or objects
                           that use the asset. Use one of the following values:
                           uses, usedBy  [required]
      -D, --debug          If true, will print the API request details to console.
      -P, --pretty         If true, will pretty print the returned JSON.
      --help               Show this message and exit.
    

### get

Used to get objects

**Usage:**

    idmc objects get [OPTIONS]
    

**Options:**

      -i, --id TEXT        Filter the returned objects by id.
      -n, --name TEXT      Filter the returned objects by name.
      -t, --type TEXT      Asset type. Type can be project, folder, or one of the
                           following asset types: DTEMPLATE, MTT, DSS, DMASK, DRS,
                           DMAPPLET, MAPPLET, BSERVICE, HSCHEMA, PCS, FWCONFIG,
                           CUSTOMSOURCE, MI_TASK, WORKFLOW, TASKFLOW, UDF,
                           PROJECT, FOLDER, PROCESS, GUIDE, AI_CONNECTION,
                           AI_SERVICE_CONNECTOR, PROCESS_OBJECT, B2BGW_MONITOR,
                           B2BGW_CUSTOMER, B2BGW_SUPPLIER, MDM_BUSINESS_ENTITY,
                           MDM_REFERENCE_ENTITY, MDM_HIERARCHY, MDM_RELATIONSHIP,
                           MDM_JOB_DEFINITION, MDM_AUTHORIZATION,
                           MDM_BUSINESS_EVENT, MDM_REPORT_SET, MDM_REPORT,
                           MDM_DYNAMIC_POOL, MDM_APPLICATION, MDM_SRC_SYSTEM,
                           MDM_APP_COMPONENT, MDM_APP_PAGE, CLEANSE, DEDUPLICATE,
                           DICTIONARY, EXCEPTION, LABELER, PARSE,
                           RULE_SPECIFICATION, VERIFIER
      -l, --location TEXT  The project and folder path where the assets are
                           located, such as Default/Sales.
      -D, --debug          If true, will print the API request details to console.
      -P, --pretty         If true, will pretty print the returned JSON.
      --help               Show this message and exit.
    

### permissions

Permission management commands.

**Usage:**

    idmc objects permissions [OPTIONS] COMMAND [ARGS]...
    

**Options:**

      --help  Show this message and exit.
    

**Subcommands**

*   _create_: Creates a permission ACL for an object
*   _delete_: Deletes permission ACL's for an object
*   _get_: Gets permission ACL's for an object
*   _update_: Updates a permission ACL for an object

#### create

Creates a permission ACL for an object

**Usage:**

    idmc objects permissions create [OPTIONS]
    

**Options:**

      -i, --id TEXT      Global unique identifier for the object. Required if
                         object path and type not included.
      -p, --path TEXT    Full path of the object including project, folder, and
                         object name. Required with type if object ID not
                         included.
      -t, --type TEXT    Type of object. Required with path if object ID not
                         included.
      -pt, --ptype TEXT  Principal type. Valid values are USER or GROUP.
                         [required]
      -pn, --pname TEXT  Principal name.  [required]
      -r, --read         Flag whether to allow the user or group to view the
                         object.
      -u, --update       Flag whether to allow the user or group to update the
                         object.
      -d, --delete       Flag whether to allow the user or group to delete the
                         object.
      -e, --execute      Flag whether to allow the user or group to execute the
                         object.
      -c, --change       Flag whether to allow the user or group to change the
                         object.
      -D, --debug        If true, will print the API request details to console.
      -P, --pretty       If true, will pretty print the returned JSON.
      --help             Show this message and exit.
    

#### delete

Deletes permission ACL's for an object

**Usage:**

    idmc objects permissions delete [OPTIONS]
    

**Options:**

      -i, --id TEXT    Global unique identifier for the object. Required if object
                       path and type not included.
      -a, --acl TEXT   Permissions ACL id. If not included all permissions are
                       deleted from the object.
      -p, --path TEXT  Full path of the object including project, folder, and
                       object name. Required with type if object ID not included.
      -t, --type TEXT  Type of object. Required with path if object ID not
                       included.
      -D, --debug      If true, will print the API request details to console.
      -P, --pretty     If true, will pretty print the returned JSON.
      --help           Show this message and exit.
    

#### get

Gets permission ACL's for an object

**Usage:**

    idmc objects permissions get [OPTIONS]
    

**Options:**

      -i, --id TEXT           Global unique identifier for the object. Required if
                              object path and type not included.
      -a, --acl TEXT          Permissions ACL id.
      -p, --path TEXT         Full path of the object including project, folder,
                              and object name. Required with type if object ID not
                              included.
      -t, --type TEXT         Type of object. Required with path if object ID not
                              included.
      -c, --check-access      Flag to check your access rights before you attempt
                              to create an asset in a project or folder.
      -ct, --check-type TEXT  Object type to be checked if you have permission to
                              create.
      -D, --debug             If true, will print the API request details to
                              console.
      -P, --pretty            If true, will pretty print the returned JSON.
      --help                  Show this message and exit.
    

#### update

Updates a permission ACL for an object

**Usage:**

    idmc objects permissions update [OPTIONS]
    

**Options:**

      -i, --id TEXT      Global unique identifier for the object. Required if
                         object path and type not included.
      -a, --acl TEXT     Permissions ACL id.
      -p, --path TEXT    Full path of the object including project, folder, and
                         object name. Required with type if object ID not
                         included.
      -t, --type TEXT    Type of object. Required with path if object ID not
                         included.
      -pt, --ptype TEXT  Principal type. Valid values are USER or GROUP.
                         [required]
      -pn, --pname TEXT  Principal name.  [required]
      -r, --read         Flag whether to allow the user or group to view the
                         object.
      -u, --update       Flag whether to allow the user or group to update the
                         object.
      -d, --delete       Flag whether to allow the user or group to delete the
                         object.
      -e, --execute      Flag whether to allow the user or group to execute the
                         object.
      -c, --change       Flag whether to allow the user or group to change the
                         object.
      -D, --debug        If true, will print the API request details to console.
      -P, --pretty       If true, will pretty print the returned JSON.
      --help             Show this message and exit.
    

### query

Used to query objects

**Usage:**

    idmc objects query [OPTIONS]
    

**Options:**

      -t, --type TEXT                 Asset type. Type can be project, folder, or
                                      one of the following asset types: DTEMPLATE,
                                      MTT, DSS, DMASK, DRS, DMAPPLET, MAPPLET,
                                      BSERVICE, HSCHEMA, PCS, FWCONFIG,
                                      CUSTOMSOURCE, MI_TASK, WORKFLOW, TASKFLOW,
                                      UDF, PROJECT, FOLDER, PROCESS, GUIDE,
                                      AI_CONNECTION, AI_SERVICE_CONNECTOR,
                                      PROCESS_OBJECT, B2BGW_MONITOR,
                                      B2BGW_CUSTOMER, B2BGW_SUPPLIER,
                                      MDM_BUSINESS_ENTITY, MDM_REFERENCE_ENTITY,
                                      MDM_HIERARCHY, MDM_RELATIONSHIP,
                                      MDM_JOB_DEFINITION, MDM_AUTHORIZATION,
                                      MDM_BUSINESS_EVENT, MDM_REPORT_SET,
                                      MDM_REPORT, MDM_DYNAMIC_POOL,
                                      MDM_APPLICATION, MDM_SRC_SYSTEM,
                                      MDM_APP_COMPONENT, MDM_APP_PAGE, CLEANSE,
                                      DEDUPLICATE, DICTIONARY, EXCEPTION, LABELER,
                                      PARSE, RULE_SPECIFICATION, VERIFIER
      -l, --location TEXT             The project and folder path where the assets
                                      are located, such as Default/Sales.
      -T, --tag TEXT                  The tag associated with the assets.
      -co, --checked-out-by TEXT      User who checked out the asset.
      -cos, --checked-out-since TEXT  Assets that have been checked out since
                                      date/time.
      -cou, --checked-out-until TEXT  Assets that have been checked out until
                                      date/time.
      -ci, --checked-in-by TEXT       User who last checked in the asset.
      -cis, --checked-in-since TEXT   Assets that have been checked in since
                                      date/time.
      -ciu, --checked-in-until TEXT   Assets that have been checked in until
                                      date/time.
      -s, --source-ctrld BOOLEAN      Flag to indicate that the asset is source
                                      controlled.
      -h, --hash TEXT                 Source control hash. Supports partial hash
                                      using a wildcard ( * ).
      -p, --published-by TEXT         User who published the asset. Applicable to
                                      Application Integration.
      -ps, --published-since TEXT     Assets that have been published since
                                      date/time.
      -pu, --published-until TEXT     Assets that have been published until
                                      date/time.
      -u, --updated-by TEXT           The user who last updated the assets. Use
                                      the userName value for the user.
      -us, --updated-since TEXT       Assets that have been updated since
                                      date/time.
      -uu, --updated-until TEXT       Assets that have been updated until
                                      date/time.
      -D, --debug                     If true, will print the API request details
                                      to console.
      -P, --pretty                    If true, will pretty print the returned
                                      JSON.
      --help                          Show this message and exit.
    

### remove-tags

Removes one or more tags from an object

**Usage:**

    idmc objects remove-tags [OPTIONS]
    

**Options:**

      -i, --id TEXT    Global unique identifier for the object. Required if object
                       path and type not included.
      -p, --path TEXT  Full path of the object including project, folder, and
                       object name. Required with type if object ID not included.
      -t, --type TEXT  Type of object. Required with path if object ID not
                       included.
      -b, --body TEXT  If removing tags from multiple objects, use this property
                       to include the JSON body. Only use this if not using --id,
                       --path, --type or --tags options.
      -T, --tags TEXT  Comma separated list of tags to be removed from the object.
      -D, --debug      If true, will print the API request details to console.
      -P, --pretty     If true, will pretty print the returned JSON.
      --help           Show this message and exit.
    

orgs
----

Organisation management commands.

**Usage:**

    idmc orgs [OPTIONS] COMMAND [ARGS]...
    

**Options:**

      --help  Show this message and exit.
    

**Subcommands**

*   _get_: Get organisation and sub-organisation details

### get

Get organisation and sub-organisation details

**Usage:**

    idmc orgs get [OPTIONS]
    

**Options:**

      -i, --suborg-id TEXT    ID of sub-organisation to be returned.
      -n, --suborg-name TEXT  Name of sub-organisation to be returned.
      -D, --debug             If true, will print the API request details to
                              console.
      -P, --pretty            If true, will pretty print the returned JSON.
      --help                  Show this message and exit.
    

privileges
----------

Privilege management commands.

**Usage:**

    idmc privileges [OPTIONS] COMMAND [ARGS]...
    

**Options:**

      --help  Show this message and exit.
    

**Subcommands**

*   _get_: Returns privileges

### get

Returns privileges

**Usage:**

    idmc privileges get [OPTIONS]
    

**Options:**

      --all         If included will return a full list of privileges, even those
                    that are disabled or unassigned.
      -D, --debug   If true, will print the API request details to console.
      -P, --pretty  If true, will pretty print the returned JSON.
      --help        Show this message and exit.
    

projects
--------

Project management commands.

**Usage:**

    idmc projects [OPTIONS] COMMAND [ARGS]...
    

**Options:**

      --help  Show this message and exit.
    

**Subcommands**

*   _create_: Creates a project
*   _delete_: Deletes a project
*   _update_: Updates a project

### create

Creates a project

**Usage:**

    idmc projects create [OPTIONS]
    

**Options:**

      -n, --name TEXT         Name for the new project.  [required]
      -d, --description TEXT  Description of the new project.
      -D, --debug             If true, will print the API request details to
                              console.
      -P, --pretty            If true, will pretty print the returned JSON.
      --help                  Show this message and exit.
    

### delete

Deletes a project

**Usage:**

    idmc projects delete [OPTIONS]
    

**Options:**

      -i, --id TEXT    ID for the project to be deleted. Use this option or
                       --path.
      -p, --path TEXT  Path of the project to be deleted. Use this option or --id.
      -D, --debug      If true, will print the API request details to console.
      -P, --pretty     If true, will pretty print the returned JSON.
      --help           Show this message and exit.
    

### update

Updates a project

**Usage:**

    idmc projects update [OPTIONS]
    

**Options:**

      -i, --id TEXT           ID for the project to be updated. Use this option or
                              --path.
      -p, --path TEXT         Path of the project to be updated. Use this option
                              or --id.
      -n, --name TEXT         New name for the project.
      -d, --description TEXT  New description for the project.
      -D, --debug             If true, will print the API request details to
                              console.
      -P, --pretty            If true, will pretty print the returned JSON.
      --help                  Show this message and exit.
    

roles
-----

Role management commands.

**Usage:**

    idmc roles [OPTIONS] COMMAND [ARGS]...
    

**Options:**

      --help  Show this message and exit.
    

**Subcommands**

*   _add-privileges_: Adds privilege assignments to a role
*   _create_: Creates a new role
*   _delete_: Deletes a role
*   _get_: Returns roles
*   _remove-privileges_: Remove privilege assignments from a role

### add-privileges

Adds privilege assignments to a role

**Usage:**

    idmc roles add-privileges [OPTIONS]
    

**Options:**

      -i, --id TEXT                ID of role to be updated. Must specify this
                                   option or --name.
      -n, --name TEXT              Name of role to be updated. Must specify this
                                   option or --id.
      -pi, --privilege-ids TEXT    Comma separated list of privilege ids to be
                                   added to user. Must specify this option or
                                   --privilege-names.
      -pn, --privilege-names TEXT  Comma separated list of privilege names to be
                                   added to user. Must specify this option or
                                   --privilege-ids.
      -D, --debug                  If true, will print the API request details to
                                   console.
      -P, --pretty                 If true, will pretty print the returned JSON.
      --help                       Show this message and exit.
    

### create

Creates a new role

**Usage:**

    idmc roles create [OPTIONS]
    

**Options:**

      -n, --name TEXT              Name for new role.  [required]
      -d, --description TEXT       Description of the new role.
      -pi, --privilege-ids TEXT    Comma separated list of privilege IDs for the
                                   new role. Must include this option or the
                                   --privilege-names option.
      -pn, --privilege-names TEXT  Comma separated list of privilege names for the
                                   new role. Must include this option or the
                                   --privilege-ids option.
      -D, --debug                  If true, will print the API request details to
                                   console.
      -P, --pretty                 If true, will pretty print the returned JSON.
      --help                       Show this message and exit.
    

### delete

Deletes a role

**Usage:**

    idmc roles delete [OPTIONS]
    

**Options:**

      -i, --id TEXT    Role id to be deleted. Use this option or the --name
                       option.
      -n, --name TEXT  Role name to be deleted. Use this option or the --id
                       option.
      -D, --debug      If true, will print the API request details to console.
      -P, --pretty     If true, will pretty print the returned JSON.
      --help           Show this message and exit.
    

### get

Returns roles

**Usage:**

    idmc roles get [OPTIONS]
    

**Options:**

      -i, --id TEXT    Filter by role id.
      -n, --name TEXT  Filter by role name.
      -e, --expand     Expand role privileges.
      -D, --debug      If true, will print the API request details to console.
      -P, --pretty     If true, will pretty print the returned JSON.
      --help           Show this message and exit.
    

### remove-privileges

Remove privilege assignments from a role

**Usage:**

    idmc roles remove-privileges [OPTIONS]
    

**Options:**

      -i, --id TEXT                ID of role to be updated. Must specify this
                                   option or --name.
      -n, --name TEXT              Name of role to be updated. Must specify this
                                   option or --id.
      -pi, --privilege-ids TEXT    Comma separated list of privilege ids to be
                                   removed from user. Must specify this option or
                                   --privilege-names.
      -pn, --privilege-names TEXT  Comma separated list of privilege names to be
                                   removed from user. Must specify this option or
                                   --privilege-ids.
      -D, --debug                  If true, will print the API request details to
                                   console.
      -P, --pretty                 If true, will pretty print the returned JSON.
      --help                       Show this message and exit.
    

schedules
---------

Schedule management commands.

**Usage:**

    idmc schedules [OPTIONS] COMMAND [ARGS]...
    

**Options:**

      --help  Show this message and exit.
    

**Subcommands**

*   _create_: Creates a schedule
*   _delete_: Deletes a schedule
*   _disable_: Disables a schedule
*   _enable_: Enables a schedule
*   _get_: Gets schedules details
*   _update_: Updates a schedule

### create

Creates a schedule

**Usage:**

    idmc schedules create [OPTIONS]
    

**Options:**

      -n, --name TEXT              Schedule name.  [required]
      -d, --description TEXT       Description of the schedule.
      -s, --status TEXT            Status of the schedule. Can be 'enabled' or
                                   'disabled'.
      -S, --start-time TEXT        Date and time when the schedule starts running,
                                   in UTC format.  [required]
      -e, --end-time TEXT          Date and time when the schedule stops running.
                                   If you do not use this parameter, the schedule
                                   runs indefinitely.
      -I, --interval TEXT          Interval or repeat frequency at which the
                                   schedule runs tasks. Use one of the following
                                   options: None, Minutely, Hourly, Daily, Weekly,
                                   Biweekly or Monthly.
      -f, --frequency INTEGER      Repeat frequency for tasks. Use one of the
                                   following values:   - For Minutely intervals,
                                   use one of the following options: 5, 10, 15,
                                   20, 30, 45. Default is 5.   - For Hourly
                                   intervals, use one of the following options: 1,
                                   2, 3, 4, 6, 8, 12. Default is 1.    - For Daily
                                   intervals, use number of days between 1 -30.
                                   Default is 1. Use with Minutely, Hourly, and
                                   Daily intervals only.
      -rs, --range-start TEXT      The start of the time range within a day that
                                   you want tasks to run. Enter a date and time
                                   using standard date/time format. Only the time
                                   portion is used. Use with Minutely, Hourly, and
                                   Daily intervals only.
      -re, --range-end TEXT        The end of the time range within a day that you
                                   want tasks to run. Enter a date and time using
                                   standard date/time format. Only the time
                                   portion is used. Use with Minutely, Hourly, and
                                   Daily intervals only.
      -t, --timezone TEXT          Time zone that the schedule uses for the
                                   dayOfMonth, weekOfMonth, and dayOfWeek fields.
                                   Default is UTC.
      -w, --weekday TEXT           Flag to indicate that tasks run on weekdays.
                                   Use with the Daily interval only.
      -dm, --day-of-month INTEGER  Date of the month that tasks should run. Use a
                                   date between 1-28. Use with the Monthly
                                   interval only. Tip: To run tasks on the last
                                   day of the month, use the Last weekOfMonth
                                   parameter with the Day dayOfWeek parameter.
      -wm, --week-of-month TEXT    Week of the month that tasks should run. Use
                                   with dayOfWeek to specify the day and week of
                                   the month that tasks should run. For example,
                                   the First Day or the Last Wednesday of the
                                   month. Use one of the following options:   -
                                   First   - Second   - Third   - Fourth   - Last
                                   Use with the Monthly interval only.
      -dw, --day-of-week TEXT
      -sun, --sunday BOOLEAN       Runs tasks on Sunday at the configured time.
                                   You can use the sun - sat parameters to run
                                   tasks on several days of the week.
      -mon, --monday BOOLEAN       Runs tasks on Monday at the configured time.
                                   You can use the sun - sat parameters to run
                                   tasks on several days of the week.
      -tue, --tuesday BOOLEAN      Runs tasks on Tuesday at the configured time.
                                   You can use the sun - sat parameters to run
                                   tasks on several days of the week.
      -wed, --wednesday BOOLEAN    Runs tasks on Wednesday at the configured time.
                                   You can use the sun - sat parameters to run
                                   tasks on several days of the week.
      -thu, --thursday BOOLEAN     Runs tasks on Thursday at the configured time.
                                   You can use the sun - sat parameters to run
                                   tasks on several days of the week.
      -fri, --friday BOOLEAN       Runs tasks on Friday at the configured time.
                                   You can use the sun - sat parameters to run
                                   tasks on several days of the week.
      -sat, --saturday BOOLEAN     Runs tasks on Saturday at the configured time.
                                   You can use the sun - sat parameters to run
                                   tasks on several days of the week.
      -D, --debug                  If true, will print the API request details to
                                   console.
      -P, --pretty                 If true, will pretty print the returned JSON.
      --help                       Show this message and exit.
    

### delete

Deletes a schedule

**Usage:**

    idmc schedules delete [OPTIONS]
    

**Options:**

      -i, --id TEXT    ID of the schedule to be deleted. Use this option or the
                       name option.
      -n, --name TEXT  Name of the schedule to be deleted. Use this option or the
                       id option.
      -D, --debug      If true, will print the API request details to console.
      -P, --pretty     If true, will pretty print the returned JSON.
      --help           Show this message and exit.
    

### disable

Disables a schedule

**Usage:**

    idmc schedules disable [OPTIONS]
    

**Options:**

      -i, --id TEXT    ID of the schedule to be disabled. Use this option or the
                       name option.
      -n, --name TEXT  Name of the schedule to be disabled. Use this option or the
                       id option.
      -D, --debug      If true, will print the API request details to console.
      -P, --pretty     If true, will pretty print the returned JSON.
      --help           Show this message and exit.
    

### enable

Enables a schedule

**Usage:**

    idmc schedules enable [OPTIONS]
    

**Options:**

      -i, --id TEXT    ID of the schedule to be enabled. Use this option or the
                       name option.
      -n, --name TEXT  Name of the schedule to be enabled. Use this option or the
                       id option.
      -D, --debug      If true, will print the API request details to console.
      -P, --pretty     If true, will pretty print the returned JSON.
      --help           Show this message and exit.
    

### get

Gets schedules details

**Usage:**

    idmc schedules get [OPTIONS]
    

**Options:**

      -i, --id TEXT        Filter the response by schedule id.
      -n, --name TEXT      Filter the response by schedule name.
      -s, --status TEXT    Filter by schedule status.
      -I, --interval TEXT  Filter by schedule interval. Valid values include
                           Minutely, Hourly, Daily, Weekly, Biweekly, and Monthly.
      -f, --from TEXT      Filter by schedule updated since.
      -t, --to TEXT        Filter by schedule updated up until.
      -D, --debug          If true, will print the API request details to console.
      -P, --pretty         If true, will pretty print the returned JSON.
      --help               Show this message and exit.
    

### update

Updates a schedule

**Usage:**

    idmc schedules update [OPTIONS]
    

**Options:**

      -i, --id TEXT                ID of the schedule to be updated. If not
                                   included then the name option must be included.
      -n, --name TEXT              Schedule name.
      -d, --description TEXT       Description of the schedule.
      -s, --status TEXT            Status of the schedule. Can be 'enabled' or
                                   'disabled'.
      -S, --start-time TEXT        Date and time when the schedule starts running,
                                   in UTC format.
      -e, --end-time TEXT          Date and time when the schedule stops running.
                                   If you do not use this parameter, the schedule
                                   runs indefinitely.
      -I, --interval TEXT          Interval or repeat frequency at which the
                                   schedule runs tasks. Use one of the following
                                   options: None, Minutely, Hourly, Daily, Weekly,
                                   Biweekly or Monthly.
      -f, --frequency INTEGER      Repeat frequency for tasks. Use one of the
                                   following values:   - For Minutely intervals,
                                   use one of the following options: 5, 10, 15,
                                   20, 30, 45. Default is 5.   - For Hourly
                                   intervals, use one of the following options: 1,
                                   2, 3, 4, 6, 8, 12. Default is 1.    - For Daily
                                   intervals, use number of days between 1 -30.
                                   Default is 1. Use with Minutely, Hourly, and
                                   Daily intervals only.
      -rs, --range-start TEXT      The start of the time range within a day that
                                   you want tasks to run. Enter a date and time
                                   using standard date/time format. Only the time
                                   portion is used. Use with Minutely, Hourly, and
                                   Daily intervals only.
      -re, --range-end TEXT        The end of the time range within a day that you
                                   want tasks to run. Enter a date and time using
                                   standard date/time format. Only the time
                                   portion is used. Use with Minutely, Hourly, and
                                   Daily intervals only.
      -t, --timezone TEXT          Time zone that the schedule uses for the
                                   dayOfMonth, weekOfMonth, and dayOfWeek fields.
                                   Default is UTC.
      -w, --weekday TEXT           Flag to indicate that tasks run on weekdays.
                                   Use with the Daily interval only.
      -dm, --day-of-month INTEGER  Date of the month that tasks should run. Use a
                                   date between 1-28. Use with the Monthly
                                   interval only. Tip: To run tasks on the last
                                   day of the month, use the Last weekOfMonth
                                   parameter with the Day dayOfWeek parameter.
      -wm, --week-of-month TEXT    Week of the month that tasks should run. Use
                                   with dayOfWeek to specify the day and week of
                                   the month that tasks should run. For example,
                                   the First Day or the Last Wednesday of the
                                   month. Use one of the following options:   -
                                   First   - Second   - Third   - Fourth   - Last
                                   Use with the Monthly interval only.
      -dw, --day-of-week TEXT
      -sun, --sunday BOOLEAN       Runs tasks on Sunday at the configured time.
                                   You can use the sun - sat parameters to run
                                   tasks on several days of the week.
      -mon, --monday BOOLEAN       Runs tasks on Monday at the configured time.
                                   You can use the sun - sat parameters to run
                                   tasks on several days of the week.
      -tue, --tuesday BOOLEAN      Runs tasks on Tuesday at the configured time.
                                   You can use the sun - sat parameters to run
                                   tasks on several days of the week.
      -wed, --wednesday BOOLEAN    Runs tasks on Wednesday at the configured time.
                                   You can use the sun - sat parameters to run
                                   tasks on several days of the week.
      -thu, --thursday BOOLEAN     Runs tasks on Thursday at the configured time.
                                   You can use the sun - sat parameters to run
                                   tasks on several days of the week.
      -fri, --friday BOOLEAN       Runs tasks on Friday at the configured time.
                                   You can use the sun - sat parameters to run
                                   tasks on several days of the week.
      -sat, --saturday BOOLEAN     Runs tasks on Saturday at the configured time.
                                   You can use the sun - sat parameters to run
                                   tasks on several days of the week.
      -D, --debug                  If true, will print the API request details to
                                   console.
      -P, --pretty                 If true, will pretty print the returned JSON.
      --help                       Show this message and exit.
    

source-control
--------------

Source control management commands.

**Usage:**

    idmc source-control [OPTIONS] COMMAND [ARGS]...
    

**Options:**

      --help  Show this message and exit.
    

**Subcommands**

*   _check-in_: Checks in one or more objects
*   _check-out_: Checks out one or more objects
*   _commit-details_: Gets the details for a commit
*   _commit-history_: Gets the commit history for an asset
*   _compare-versions_: Used to compare two versions of an asset.
*   _pull_: Pulls one or more objects
*   _pull-commit-hash_: Pulls all objects in a commit hash
*   _repo-details_: Gets the source control repository details
*   _status_: Gets the status of a source control action
*   _undo-check-out_: Undo check out for one or more objects

### check-in

Checks in one or more objects

**Usage:**

    idmc source-control check-in [OPTIONS]
    

**Options:**

      -s, --summary TEXT       The summary that should be included in the git
                               commit.  [required]
      -d, --description TEXT   The description that should be included in the git
                               commit.
      -i, --id TEXT            Global unique identifier for the object. Required
                               if object path and type not included.
      -p, --path TEXT          Full path of the object including project, folder,
                               and object name. Required with type if object ID
                               not included.
      -t, --type TEXT          Type of object. Required with path if object ID not
                               included.
      -b, --body TEXT          If checking in multiple objects, use this property
                               to include the JSON body. Only use this if not
                               using --id, --path or --type.
      -I, --include-container  Whether all objects in a project or folder are
                               included in the check-in.
      -D, --debug              If true, will print the API request details to
                               console.
      -P, --pretty             If true, will pretty print the returned JSON.
      --help                   Show this message and exit.
    

### check-out

Checks out one or more objects

**Usage:**

    idmc source-control check-out [OPTIONS]
    

**Options:**

      -i, --id TEXT            Global unique identifier for the object. Required
                               if object path and type not included.
      -p, --path TEXT          Full path of the object including project, folder,
                               and object name. Required with type if object ID
                               not included.
      -t, --type TEXT          Type of object. Required with path if object ID not
                               included.
      -b, --body TEXT          If checking out multiple objects, use this property
                               to include the JSON body. Only use this if not
                               using --id, --path or --type.
      -I, --include-container  Whether all objects in a project or folder are
                               included in the check-out.
      -D, --debug              If true, will print the API request details to
                               console.
      -P, --pretty             If true, will pretty print the returned JSON.
      --help                   Show this message and exit.
    

### commit-details

Gets the details for a commit

**Usage:**

    idmc source-control commit-details [OPTIONS]
    

**Options:**

      -h, --hash TEXT     Commit hash for the details to be returned.  [required]
      -s, --search-all    Flag whether to search project-level repositories if the
                          commit hash wasn't found for the global repository.
      -r, --repo-id TEXT  Connection ID of the project-level repository to search.
      -D, --debug         If true, will print the API request details to console.
      -P, --pretty        If true, will pretty print the returned JSON.
      --help              Show this message and exit.
    

### commit-history

Gets the commit history for an asset

**Usage:**

    idmc source-control commit-history [OPTIONS]
    

**Options:**

      -i, --id TEXT      ID of the project, folder, or asset.
      -p, --path TEXT    Project or path where the assets are located. Required if
                         --id is not specified.
      -t, --type TEXT    Type of the asset. Required if --id is not specified.
      -b, --branch TEXT  Repository branch, if different from the branch that's
                         configured for the organization.
      -D, --debug        If true, will print the API request details to console.
      -P, --pretty       If true, will pretty print the returned JSON.
      --help             Show this message and exit.
    

### compare-versions

Used to compare two versions of an asset.

**Usage:**

    idmc source-control compare-versions [OPTIONS]
    

**Options:**

      -i, --id TEXT           ID of the project, folder, or asset.
      -p, --path TEXT         Project or path where the assets are located.
                              Required if --id is not specified.
      -t, --type TEXT         Type of the asset. Required if --id is not
                              specified.
      -o, --old-version TEXT  The base version of the asset to compare. If the
                              asset version to compare is checked in to the
                              repository, use the commit hash for the value. If
                              the asset version to compare hasn't been checked in,
                              use the following value: CURRENT-VERSION  [required]
      -n, --new-version TEXT  The asset version to compare to the base version. If
                              the asset version to compare is checked in to the
                              repository, use the commit hash for the value. If
                              the asset version to compare hasn't been checked in,
                              use the following value: CURRENT-VERSION  [required]
      -f, --format TEXT       Response format. Use either JSON or TEXT.
                              [required]
      -D, --debug             If true, will print the API request details to
                              console.
      -P, --pretty            If true, will pretty print the returned JSON.
      --help                  Show this message and exit.
    

### pull

Pulls one or more objects

**Usage:**

    idmc source-control pull [OPTIONS]
    

**Options:**

      -i, --id TEXT           Global unique identifier for the object. Required if
                              object path and type not included.
      -p, --path TEXT         Full path of the object including project, folder,
                              and object name. Required with type if object ID not
                              included.
      -t, --type TEXT         Type of object. Required with path if object ID not
                              included.
      -h, --hash TEXT         Unique commit hash to pull.  [required]
      -r, --relax-validation  The objectSpecification objects are ignored if the
                              sources don't exist in the assets that are included
                              in the pull.
      -b, --body TEXT         If checking out multiple objects, use this property
                              to include the JSON body. Only use this if not using
                              --id, --path or --type.
      -D, --debug             If true, will print the API request details to
                              console.
      -P, --pretty            If true, will pretty print the returned JSON.
      --help                  Show this message and exit.
    

### pull-commit-hash

Pulls all objects in a commit hash

**Usage:**

    idmc source-control pull-commit-hash [OPTIONS]
    

**Options:**

      -h, --hash TEXT         Unique commit hash to pull.  [required]
      -s, --search            Flag to search project-level repositories if the
                              commit hash wasn't found for the global repository.
      -ri, --repo-id TEXT     Connection ID of the project-level repository to
                              search. If not specified, the global repository is
                              searched.
      -r, --relax-validation  The objectSpecification objects are ignored if the
                              sources don't exist in the assets that are included
                              in the pull.
      -D, --debug             If true, will print the API request details to
                              console.
      -P, --pretty            If true, will pretty print the returned JSON.
      --help                  Show this message and exit.
    

### repo-details

Gets the source control repository details

**Usage:**

    idmc source-control repo-details [OPTIONS]
    

**Options:**

      -i, --project-ids TEXT    Comma separated list of project id's to return the
                                repository details for. Required if --project-
                                names is not used.
      -n, --project-names TEXT  Comma separated list of project names to return
                                the repository details for. Required if --project-
                                ids is not used.
      -D, --debug               If true, will print the API request details to
                                console.
      -P, --pretty              If true, will pretty print the returned JSON.
      --help                    Show this message and exit.
    

### status

Gets the status of a source control action

**Usage:**

    idmc source-control status [OPTIONS]
    

**Options:**

      -i, --id TEXT  ID of the source control action.  [required]
      -D, --debug    If true, will print the API request details to console.
      -P, --pretty   If true, will pretty print the returned JSON.
      --help         Show this message and exit.
    

### undo-check-out

Undo check out for one or more objects

**Usage:**

    idmc source-control undo-check-out [OPTIONS]
    

**Options:**

      -i, --id TEXT            Global unique identifier for the object. Required
                               if object path and type not included.
      -p, --path TEXT          Full path of the object including project, folder,
                               and object name. Required with type if object ID
                               not included.
      -t, --type TEXT          Type of object. Required with path if object ID not
                               included.
      -b, --body TEXT          If undoing check out multiple objects, use this
                               property to include the JSON body. Only use this if
                               not using --id, --path or --type.
      -I, --include-container  Whether all objects in a project or folder are
                               included in the undo check-out.
      -D, --debug              If true, will print the API request details to
                               console.
      -P, --pretty             If true, will pretty print the returned JSON.
      --help                   Show this message and exit.
    

user-groups
-----------

User group management commands.

**Usage:**

    idmc user-groups [OPTIONS] COMMAND [ARGS]...
    

**Options:**

      --help  Show this message and exit.
    

**Subcommands**

*   _add-roles_: Adds role assignments to a user group
*   _create_: Creates a new user group
*   _delete_: Deletes a user group
*   _get_: Returns user groups

### add-roles

Adds role assignments to a user group

**Usage:**

    idmc user-groups add-roles [OPTIONS]
    

**Options:**

      -i, --id TEXT           ID of user group to be updated. Must specify this
                              option or --group-name.
      -gn, --group-name TEXT  Name of user group to be updated. Must specify this
                              option or --id.
      -ri, --role-ids TEXT    Comma separated list of role ids to be added to
                              user. Must specify this option or --role-names.
      -rn, --role-names TEXT  Comma separated list of role names to be added to
                              user. Must specify this option or --role-ids.
      -D, --debug             If true, will print the API request details to
                              console.
      -P, --pretty            If true, will pretty print the returned JSON.
      --help                  Show this message and exit.
    

### create

Creates a new user group

**Usage:**

    idmc user-groups create [OPTIONS]
    

**Options:**

      -n, --name TEXT         Name of the new user group.  [required]
      -d, --description TEXT  Description of the new user group.
      -ri, --role-ids TEXT    Comma separated list of role ids to be added to the
                              new user group. Either this or the --role-names
                              group is required.
      -rn, --role-names TEXT  Comma separated list of role names to be added to
                              the new user group. Either this or the --role-ids
                              group is required.
      -ui, --user-ids TEXT    Comma separated list of user ids to be added to the
                              new user group.  Use this option or the --user-names
                              option.
      -un, --user-names TEXT  Comma separated list of user names to be added to
                              the new user group. Use this option or the --user-
                              ids option.
      -D, --debug             If true, will print the API request details to
                              console.
      -P, --pretty            If true, will pretty print the returned JSON.
      --help                  Show this message and exit.
    

### delete

Deletes a user group

**Usage:**

    idmc user-groups delete [OPTIONS]
    

**Options:**

      -i, --id TEXT    User group id to be deleted. Use this option or the --name
                       option.
      -n, --name TEXT  User group name to be deleted. Use this option or the --id
                       option.
      -D, --debug      If true, will print the API request details to console.
      -P, --pretty     If true, will pretty print the returned JSON.
      --help           Show this message and exit.
    

### get

Returns user groups

**Usage:**

    idmc user-groups get [OPTIONS]
    

**Options:**

      -i, --id TEXT    Filter by user group id. Use this option or the --username
                       option.
      -n, --name TEXT  Filter by user group name. Use this option or the --id
                       option.
      -D, --debug      If true, will print the API request details to console.
      -P, --pretty     If true, will pretty print the returned JSON.
      --help           Show this message and exit.
    

users
-----

User management commands.

**Usage:**

    idmc users [OPTIONS] COMMAND [ARGS]...
    

**Options:**

      --help  Show this message and exit.
    

**Subcommands**

*   _add-groups_: Adds group assignments to a user
*   _add-roles_: Adds role assignments to a user
*   _create_: Used to create new users
*   _delete_: Deletes a user
*   _get_: Returns users
*   _password_: Password management commands.
*   _remove-groups_: Removes group assignments from a user
*   _remove-roles_: Removes role assignments from a user

### add-groups

Adds group assignments to a user

**Usage:**

    idmc users add-groups [OPTIONS]
    

**Options:**

      -i, --id TEXT            ID of user to be updated. Must specify this option
                               or --username.
      -u, --username TEXT      Username to be updated. Must specify this option or
                               --id.
      -gi, --group-ids TEXT    Comma separated list of group ids to be added to
                               user. Must specify this option or --group-names.
      -gn, --group-names TEXT  Comma separated list of group names to be added to
                               user. Must specify this option or --group-ids.
      -D, --debug              If true, will print the API request details to
                               console.
      -P, --pretty             If true, will pretty print the returned JSON.
      --help                   Show this message and exit.
    

### add-roles

Adds role assignments to a user

**Usage:**

    idmc users add-roles [OPTIONS]
    

**Options:**

      -i, --id TEXT           ID of user to be updated. Must specify this option
                              or --username.
      -u, --username TEXT     ID of user to be updated. Must specify this option
                              or --id.
      -ri, --role-ids TEXT    Comma separated list of role ids to be added to
                              user. Must specify this option or --role-names.
      -rn, --role-names TEXT  Comma separated list of role names to be added to
                              user. Must specify this option or --role-ids.
      -D, --debug             If true, will print the API request details to
                              console.
      -P, --pretty            If true, will pretty print the returned JSON.
      --help                  Show this message and exit.
    

### create

Used to create new users

**Usage:**

    idmc users create [OPTIONS]
    

**Options:**

      -n, --name TEXT                 Informatica Intelligent Cloud Services user
                                      name.  [required]
      -f, --first-name TEXT           First name for the user account.  [required]
      -l, --last-name TEXT            Last name for the user account.  [required]
      -p, --password TEXT             Informatica Intelligent Cloud Services
                                      password. If password is empty, the user
                                      receives an activation email. Maximum length
                                      is 255 characters.
      -d, --description TEXT          Description of the user.
      -e, --email TEXT                Email address for the user.  [required]
      -t, --title TEXT                Job title of the user.
      -ph, --phone TEXT               Phone number for the user.
      -fp, --force-password-change BOOLEAN
                                      Determines whether the user must reset the
                                      password after the user logs in for the
                                      first time.
      -ml, --max-login-attempts INTEGER
                                      Number of times a user can attempt to log in
                                      before the account is locked.
      -a, --authentication INTEGER    Determines whether the user accesses
                                      Informatica Intelligent Cloud Services
                                      through single sign-in (SAML). Use one of
                                      the following values: 0 (Native), 1 (SAML).
      -an, --alias-name TEXT          Required when authentication is not 0. The
                                      user identifier or user name in the 3rd
                                      party system.
      -ri, --role-ids TEXT            Required when no group IDs are included.
                                      Comma separated list of IDs for the roles to
                                      assign to the user.
      -rn, --role-names TEXT          Required when no group IDs are included.
                                      Comma separated list of Names for the roles
                                      to assign to the user.
      -gi, --group-ids TEXT           Required when no role IDs are included.
                                      Comma separated list of IDs for the user
                                      groups to assign to the user.
      -gn, --group-names TEXT         Required when no role IDs are included.
                                      Comma separated list of Names for the user
                                      groups to assign to the user.
      -D, --debug                     If true, will print the API request details
                                      to console.
      -P, --pretty                    If true, will pretty print the returned
                                      JSON.
      --help                          Show this message and exit.
    

### delete

Deletes a user

**Usage:**

    idmc users delete [OPTIONS]
    

**Options:**

      -i, --id TEXT        User id to be deleted. Use this option or the
                           --username option.
      -u, --username TEXT  User name to be deleted. Use this option or the --id
                           option.
      -D, --debug          If true, will print the API request details to console.
      -P, --pretty         If true, will pretty print the returned JSON.
      --help               Show this message and exit.
    

### get

Returns users

**Usage:**

    idmc users get [OPTIONS]
    

**Options:**

      -i, --id TEXT        (Optional) Filter by user id. Use this option or the
                           --username option.
      -u, --username TEXT  (Optional) Filter by user name. Use this option or the
                           --id option.
      -D, --debug          If true, will print the API request details to console.
      -P, --pretty         If true, will pretty print the returned JSON.
      --help               Show this message and exit.
    

### password

Password management commands.

**Usage:**

    idmc users password [OPTIONS] COMMAND [ARGS]...
    

**Options:**

      --help  Show this message and exit.
    

**Subcommands**

*   _change_: Change a users password
*   _reset_: Resets a users password using their security answer

#### change

Change a users password

**Usage:**

    idmc users password change [OPTIONS]
    

**Options:**

      -i, --id TEXT            User id to be updated. Use this option or the
                               --username option. This or the --username option is
                               required if an administrator is changing the
                               password for another user.
      -u, --username TEXT      User name to be updated. Use this option or the
                               --id option. This or the --id option is required if
                               an administrator is changing the password for
                               another user.
      -o, --old-password TEXT  The old password for the user. Required if you are
                               changing your own password.
      -n, --new-password TEXT  The new password for the user.  [required]
      -D, --debug              If true, will print the API request details to
                               console.
      -P, --pretty             If true, will pretty print the returned JSON.
      --help                   Show this message and exit.
    

#### reset

Resets a users password using their security answer

**Usage:**

    idmc users password reset [OPTIONS]
    

**Options:**

      -i, --id TEXT               User id to be updated. Use this option or the
                                  --username option.
      -u, --username TEXT         User name to be updated. Use this option or the
                                  --id option.
      -s, --security-answer TEXT  Security answer to the user's security question.
                                  [required]
      -n, --new-password TEXT     The new password for the user.  [required]
      -D, --debug                 If true, will print the API request details to
                                  console.
      -P, --pretty                If true, will pretty print the returned JSON.
      --help                      Show this message and exit.
    

### remove-groups

Removes group assignments from a user

**Usage:**

    idmc users remove-groups [OPTIONS]
    

**Options:**

      -i, --id TEXT            ID of user to be updated. Must specify this option
                               or --username.
      -u, --username TEXT      Username to be updated. Must specify this option or
                               --id.
      -gi, --group-ids TEXT    Comma separated list of group ids to be removed
                               from the user. Must specify this option or --group-
                               names.
      -gn, --group-names TEXT  Comma separated list of group names to be removed
                               from the user. Must specify this option or --group-
                               ids.
      -D, --debug              If true, will print the API request details to
                               console.
      -P, --pretty             If true, will pretty print the returned JSON.
      --help                   Show this message and exit.
    

### remove-roles

Removes role assignments from a user

**Usage:**

    idmc users remove-roles [OPTIONS]
    

**Options:**

      -i, --id TEXT           ID of user to be updated. Must specify this option
                              or --username.
      -u, --username TEXT     Username to be updated. Must specify this option or
                              --id.
      -ri, --role-ids TEXT    Comma separated list of role ids to be added to
                              user. Must specify this option or --roleNames.
      -rn, --role-names TEXT  Comma separated list of role names to be added to
                              user. Must specify this option or --roleIds.
      -D, --debug             If true, will print the API request details to
                              console.
      -P, --pretty            If true, will pretty print the returned JSON.
      --help                  Show this message and exit.
    

