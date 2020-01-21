# Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

"""
Stubs for testing transform_utils.py
"""

pipeline_states_response = {
    "body": {
        "states": [
            {
                "stage_name": "Source",
                "name": "Source",
                "status": "Succeeded",
                "percent_complete": "N/A",
                "last_status_change": "2020-01-08 15:26:23",
                "error_details": "N/A"
            },
            {
                "stage_name": "Build",
                "name": "ContainerBuild",
                "status": "Succeeded",
                "percent_complete": "N/A",
                "last_status_change": "2020-01-08 15:27:27",
                "error_details": "N/A"
            },
            {
                "stage_name": "Build",
                "name": "GenerateTemplate",
                "status": "Succeeded",
                "percent_complete": "N/A",
                "last_status_change": "2020-01-08 15:27:27",
                "error_details": "N/A"
            },
            {
                "stage_name": "Development",
                "name": "DeployDev",
                "status": "InProgress",
                "percent_complete": "N/A",
                "last_status_change": "2020-01-08 15:27:28",
                "error_details": "N/A"
            },
            {
                "stage_name": "ApprovalStage",
                "name": "Approval",
                "status": "N/A",
                "percent_complete": "N/A",
                "last_status_change": "N/A",
                "error_details": "N/A"
            },
            {
                "stage_name": "Production",
                "name": "DeployProd",
                "status": "N/A",
                "percent_complete": "N/A",
                "last_status_change": "N/A",
                "error_details": "N/A"
            }
        ]
    }, "statusCode": 200
}

get_states_response = {
    "states": [
        {
            "stage_name": "Source",
            "name": "Source",
            "status": "Succeeded",
            "percent_complete": "N/A",
            "last_status_change": "2020-01-08 15:26:23",
            "error_details": "N/A"
        },
        {
            "stage_name": "Build",
            "name": "ContainerBuild",
            "status": "Succeeded",
            "percent_complete": "N/A",
            "last_status_change": "2020-01-08 15:27:27",
            "error_details": "N/A"
        },
        {
            "stage_name": "Build",
            "name": "GenerateTemplate",
            "status": "Succeeded",
            "percent_complete": "N/A",
            "last_status_change": "2020-01-08 15:27:27",
            "error_details": "N/A"
        },
        {
            "stage_name": "Development",
            "name": "DeployDev",
            "status": "InProgress",
            "percent_complete": "N/A",
            "last_status_change": "2020-01-08 15:27:28",
            "error_details": "N/A"
        },
        {
            "stage_name": "ApprovalStage",
            "name": "Approval",
            "status": "N/A",
            "percent_complete": "N/A",
            "last_status_change": "N/A",
            "error_details": "N/A"
        },
        {
            "stage_name": "Production",
            "name": "DeployProd",
            "status": "N/A",
            "percent_complete": "N/A",
            "last_status_change": "N/A",
            "error_details": "N/A"
        }
    ]
}
