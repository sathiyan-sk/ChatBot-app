-- Convert all relational UUID-like identifiers to native PostgreSQL UUID columns.
-- Safe for a freshly cleaned database, or for a DB where the data has already been validated.

BEGIN;

ALTER TABLE applications
  ALTER COLUMN id TYPE UUID USING id::uuid;

ALTER TABLE knowledge_bases
  ALTER COLUMN id TYPE UUID USING id::uuid,
  ALTER COLUMN application_id TYPE UUID USING application_id::uuid;

ALTER TABLE documents
  ALTER COLUMN id TYPE UUID USING id::uuid,
  ALTER COLUMN application_id TYPE UUID USING application_id::uuid,
  ALTER COLUMN knowledge_base_id TYPE UUID USING knowledge_base_id::uuid;

ALTER TABLE conversations
  ALTER COLUMN id TYPE UUID USING id::uuid,
  ALTER COLUMN application_id TYPE UUID USING application_id::uuid;

ALTER TABLE messages
  ALTER COLUMN id TYPE UUID USING id::uuid,
  ALTER COLUMN conversation_id TYPE UUID USING conversation_id::uuid;

ALTER TABLE api_keys
  ALTER COLUMN id TYPE UUID USING id::uuid,
  ALTER COLUMN application_id TYPE UUID USING application_id::uuid;

ALTER TABLE application_settings
  ALTER COLUMN id TYPE UUID USING id::uuid,
  ALTER COLUMN application_id TYPE UUID USING application_id::uuid;

ALTER TABLE widgets
  ALTER COLUMN id TYPE UUID USING id::uuid,
  ALTER COLUMN application_id TYPE UUID USING application_id::uuid;

COMMIT;
