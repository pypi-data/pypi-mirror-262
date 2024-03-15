=============
**tfc_admin**
=============

Overview
--------

Make Terraform Cloud API calls for common platform administration tasks.

Reference
---------

`Terraform Cloud API Documentation <https://developer.hashicorp.com/terraform/cloud-docs/api-docs>`_

Available Functions
-------------------

- Show organization details
- List teams
- List projects
- Get project ID from project name
- List workspaces in a project
- Get workspace ID from workspace name
- Move workspace into a project

Examples
--------

.. code-block:: PYTHON

   import sys
   import tfc_admin

   # List all teams in an organization.
   teams_list = []
   page_number = 1

   # Iterate through all pages of teams.
   while True:
      teams = tfc_admin.get_teams(
         sys.argv[1],  # token
         sys.argv[2],  # organization
         page_number
      )
      if not teams['data']:
         break
      for team in teams['data']:
         teams_list.append(team['attributes']['name'])
      page_number += 1
   
   # Print the list of teams.
   print(teams_list)
