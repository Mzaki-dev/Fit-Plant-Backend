# Fit Plant Backend Instructions

- [x] Verify that the copilot-instructions.md file in the .github directory is created. - Created the file with initial checklist.

- [x] Clarify Project Requirements - Requirements are clear: FastAPI backend with admin/worker roles, admin CRUD on workers with specified fields.

- [x] Scaffold the Project - Created FastAPI project structure with models, schemas, CRUD, auth, routers, and main app.

- [x] Customize the Project - Implemented user roles, authentication, and CRUD operations for workers by admin.

- [x] Install Required Extensions - No extensions needed.

- [x] Compile the Project - Installed dependencies and resolved issues with password hashing and Pydantic config.

- [x] Create and Run Task - Not needed for this project.

- [x] Launch the Project - Ready to launch with uvicorn main:app --reload

- [x] Ensure Documentation is Complete - README.md created with setup and API instructions.

## Execution Guidelines

PROGRESS TRACKING:
- After completing each step, mark it complete and add a summary.

COMMUNICATION RULES:
- Avoid verbose explanations or printing full command outputs.
- If a step is skipped, state that briefly (e.g. "No extensions needed").
- Do not explain project structure unless asked.
- Keep explanations concise and focused.

DEVELOPMENT RULES:
- Use '.' as the working directory unless user specifies otherwise.
- Avoid adding media or external links unless explicitly requested.
- Use placeholders only with a note that they should be replaced.
- Use VS Code API tool only for VS Code extension projects.
- Once the project is created, it is already opened in Visual Studio Code—do not suggest commands to open this project in Visual Studio again.

FOLDER CREATION RULES:
- Always use the current directory as the project root.
- If you are running any terminal commands, use the '.' argument to ensure that the current working directory is used ALWAYS.
- Do not create a new folder unless the user explicitly requests it besides a .vscode folder for a tasks.json file.

EXTENSION INSTALLATION RULES:
- Only install extension specified by the get_project_setup_info tool. DO NOT INSTALL any other extensions.

PROJECT CONTENT RULES:
- Avoid adding links of any type (URLs, files, folders, etc.) or integrations that are not explicitly required.
- Avoid generating images, videos, or any other media files unless explicitly requested.
- Ensure all generated components serve a clear purpose within the user's requested workflow.

TASK COMPLETION RULES:
- Your task is complete when:
  - Project is successfully scaffolded and compiled without errors
  - copilot-instructions.md file in the .github directory exists in the project
  - README.md file exists and is up to date
  - User is provided with clear instructions to debug/launch the project

- Work through each checklist item systematically.
- Keep communication concise and focused.
- Follow development best practices.