-- table for total number of active and engaged users on a given date
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    total_active_users INT NOT NULL,
    total_engaged_users INT NOT NULL
);

-- ** optional:
    -- entire table, info can be distributed to other tables
-- name [copilot_dot_com, copilot_dotcom_pull_requests, copilot_ide_chat, copilot_ide_code_completions]
CREATE TABLE copilot_engagement (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    name VARCHAR(255) NOT NULL,
    total_engaged_users INT NOT NULL
);

-- ** optional: 
    -- entire table, info can be distributed to other tables
    -- total_engaged_users (info is in copilot_engagement)
-- name [copilot_ide_chat, copilot_ide_code_completions]
CREATE TABLE editor_engagement (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    name VARCHAR(255) NOT NULL,
    total_engaged_users INT NOT NULL,
    editor_name VARCHAR(255) NOT NULL,
    total_engaged_users_in_editor INT NOT NULL
);

-- ** optional: 
    -- total_engaged_users (info is in copilot_engagement)
    -- total_engaged_users_in_editor (info is in editor_engagement)
-- name [copilot_ide_chat]
CREATE TABLE editor_chat_engagement (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    name VARCHAR(255) NOT NULL,
    total_engaged_users INT NOT NULL,
    editor_name VARCHAR(255) NOT NULL,
    total_engaged_users_in_editor INT NOT NULL,
    model_name VARCHAR(255) NOT NULL,
    total_chats INI NOT NULL,
    is_custom_model BOOLEAN NOT NULL,
    total_engaged_users_in_model INT NOT NULL,
    total_chat_copy_events INT NOT NULL,
    total_chat_insertion_events INT NOT NULL
);

-- ** optional:
    -- entire table, info can be distributed to other tables
    -- total_engaged_users (info is in copilot_engagement)
    -- total_engaged_users_in_editor (info is in editor_engagement)
-- name [copilot_ide_code_completions]
CREATE TABLE editor_code_completion_engagement (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    name VARCHAR(255) NOT NULL,
    total_engaged_users INT NOT NULL,
    editor_name VARCHAR(255) NOT NULL,
    total_engaged_users_in_editor INT NOT NULL,
    model_name VARCHAR(255) NOT NULL,
    is_custom_model BOOLEAN NOT NULL,
    total_engaged_users_in_model INT NOT NULL
);

-- ** optional:
    -- total_engaged_users (info is in copilot_engagement)
    -- total_engaged_users_in_editor (info is in editor_engagement)
    -- model_name, is_custom_model, total_engaged_users_in_model (info is in editor_code_completion_engagement)
-- name [copilot_ide_code_completions]
CREATE TABLE editor_code_completion_model_language_engagement (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    name VARCHAR(255) NOT NULL,
    total_engaged_users INT NOT NULL,
    editor_name VARCHAR(255) NOT NULL,
    total_engaged_users_in_editor INT NOT NULL,
    model_name VARCHAR(255) NOT NULL,
    is_custom_model BOOLEAN NOT NULL,
    total_engaged_users_in_model INT NOT NULL,
    language_name VARCHAR(255) NOT NULL,
    total_engaged_users_in_language INT NOT NULL,
    total_code_acceptances INT NOT NULL,
    total_code_suggestions INT NOT NULL,
    total_code_lines_accepted INT NOT NULL,
    total_code_lines_suggested INT NOT NULL
);

-- ** optional:
    -- entire table could be combined with above table
-- output separates this into serparate list, but it's a sum of above table
-- name [copilot_ide_code_completions]
CREATE TABLE editor_code_completion_language_engagement (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    name VARCHAR(255) NOT NULL,
    language_name VARCHAR(255) NOT NULL,
    total_engaged_users_in_language INT NOT NULL
);