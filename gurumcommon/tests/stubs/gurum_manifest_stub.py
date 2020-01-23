# Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

"""
Stubs for testing gurum_manifest.py
"""

valid_manifest = {
    'project': {
        'name': 'game',
        'source': {
            'provider': 'github/cfn',
            'repo': 'kalleeh/2048'
        },
        'type': 'ecs-fargate'
    },
    'environments': [
        {
            'name': 'dev',
            'config': {
                'HealthCheckPath': '/',
                'DesiredCount': '2'
            },
            'env_vars': {
                'environment': 'dev'
            }
        },
        {
            'name': 'prod',
            'config': {
                'HealthCheckPath': '/',
                'DesiredCount': '2'
            },
            'env_vars': {
                'environment': 'prod'
            }
        }
    ],
    'services': [
        {
            'name': 'block_storage',
            'type': 's3',
            'config': {
                'BucketName': 'my-block-storage-bucket',
                'LoggingPrefix': 'log-prefix'
            }
        },
        {
            'name': 'customer_database',
            'type': 'rds',
            'config': {
                'DBEngine': 'mysql',
                'InstanceClass': 'db.t2.small'
            }
        }
    ]
}

invalid_missing_project_manifest = {
    'environments': [
        {
            'name': 'dev',
            'config': {
                'HealthCheckPath': '/',
                'DesiredCount': '2'
            },
            'env_vars': {
                'environment': 'dev'
            }
        },
        {
            'name': 'prod',
            'config': {
                'HealthCheckPath': '/',
                'DesiredCount': '2'
            },
            'env_vars': {
                'environment': 'prod'
            }
        }
    ],
    'services': [
        {
            'name': 'block_storage',
            'type': 's3',
            'config': {
                'BucketName': 'my-block-storage-bucket',
                'LoggingPrefix': 'log-prefix'
            }
        }
    ]
}

invalid_missing_environments_manifest = {
    'project': {
        'name': 'game',
        'source': {
            'provider': 'github/cfn',
            'repo': 'kalleeh/2048'
        },
        'type': 'ecs-fargate'
    },
    'services': [
        {
            'name': 'block_storage',
            'type': 's3',
            'config': {
                'BucketName': 'my-block-storage-bucket',
                'LoggingPrefix': 'log-prefix'
            }
        }
    ]
}

valid_missing_services_manifest = {
    'project': {
        'name': 'game',
        'source': {
            'provider': 'github/cfn',
            'repo': 'kalleeh/2048'
        },
        'type': 'ecs-fargate'
    },
    'environments': [
        {
            'name': 'dev',
            'config': {
                'HealthCheckPath': '/',
                'DesiredCount': '2'
            },
            'env_vars': {
                'environment': 'dev'
            }
        }
    ]
}

valid_project = {
    'name': 'game',
    'source': {
        'provider': 'github/cfn',
        'repo': 'kalleeh/2048'
    },
    'type': 'ecs-fargate'
}

valid_environments = [
    {
        'name': 'dev',
        'config': {
            'HealthCheckPath': '/',
            'DesiredCount': '2'
        },
        'env_vars': {
            'environment': 'dev'
        }
    },
    {
        'name': 'prod',
        'config': {
            'HealthCheckPath': '/',
            'DesiredCount': '2'
        },
        'env_vars': {
            'environment': 'prod'
        }
    }
]

valid_services = [
    {
        'name': 'block_storage',
        'type': 's3',
        'config': {
            'BucketName': 'my-block-storage-bucket',
            'LoggingPrefix': 'log-prefix'
        }
    },
    {
        'name': 'customer_database',
        'type': 'rds',
        'config': {
            'DBEngine': 'mysql',
            'InstanceClass': 'db.t2.small'
        }
    }
]
