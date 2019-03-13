import os
import json

# Use ${ENV.USER} for remote vars

site = {
    "midway_single": {
        "app": {
            "bash_single": {
                "executable": "/bin/bash"
            }
        },
        "maxParallelTasks": 201,
        "comments": "",
        "initialParallelTasks": 200,
        "filesystem": {
            "URL": "localhost",
            "type": "local"
        },
        "execution": {
            "URL": "localhost:1",
            "jobManager": "local:slurm",
            "type": "coaster",
            "options": {
                "maxNodesPerJob": 1,
                "maxJobs": 1,
                "highOverallocation": 100,
                "nodeGranularity": 1,
                "jobQueue": "sandyb",
                "lowOverallocation": 100,
                "tasksPerNode": 1
            }
        },
        "workDirectory": "/scratch/midway/" + os.getenv("USER")
    },
    "midway_multiple": {
        "app": {
            "bash_multiple": {
                "executable": "/bin/bash"
            }
        },
        "maxParallelTasks": 201,
        "comments": "",
        "initialParallelTasks": 200,
        "filesystem": {
            "URL": "localhost",
            "type": "local"
        },
        "execution": {
            "URL": "localhost:2",
            "jobManager": "local:slurm",
            "type": "coaster",
            "options": {
                "maxNodesPerJob": 1,
                "maxJobs": 1,
                "highOverallocation": 100,
                "nodeGranularity": 1,
                "jobQueue": "sandyb",
                "lowOverallocation": 100,
                "tasksPerNode": 16
            }
        },
        "workDirectory": "/scratch/midway/${ENV.USER}" + os.getenv("USER")
    }
}

print(json.dumps(site, indent=4))
sites = [site['midway_single'], site['midway_multiple']]
