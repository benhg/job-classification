
config = {}
config["sites"] = ["UC RCC MIDWAY", "BEAGLE", "CI CONNECT"]

config['site'] = {
    "definition": {
        "id ": "ced81a8b-6130-11e4-b652-12313940394d",
        "Name": "UC RCC Midway"
    },
    "security": {
        "ssh": {
            "Type": "SSH",
            "Login": "12.12.12.12",
            "auth": "publickey",
            "identity_file": "",
            "options": ""
        },
        "globusssh": {
            "Type": "GlobusSSH",
            "Login": "12.12.12.12"
        }
    },
    "execution": {
        "host": "midway.rcc.uchicago.edu",
        "type": "ipyparallel",
        "launcher": "slurm_scalable_executor",
        "job_queues": ["westmere", "sandyb"],
        "min_nodes": 1,
        "max_nodes": 25,
        "node_granularity": 5,
        "nodes_per_job": 1,
        "max_jobs": 25

    },
    "data": {
        "staging": "direct",
        "keep_site_dir": true,
        "protocols": [{
                        "type": "Globus",
                        "endpoint": "ced81a8b-6130-11e4-b652-12313940394d"
                     },
            {
                "type": "SCP",
                "tddress": "10.10.10.10",
                "maxChannels": 4
            }
        ],
        "work_directory": "/home/${REMOTE(user)}/parsl_work",
        "protocol_selection_logic": ""
    },
    "app": {
        "max_wall_time": "00:30:00",
        "tcp_port_range": "50000,51000",
        "lazy_errors": false,
        "execution_retries": 0,
        "provider_staging_pin_swift_files": true,
        "always_transfer_wrapper_log": true


    }

}
