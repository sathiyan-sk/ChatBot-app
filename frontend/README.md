# AI Knowledge Platform --- Frontend

## 1. Frontend Purpose

The frontend is the client layer of the AI Knowledge Platform. It
provides two separate interfaces:

1.  **Admin Portal** --- used by the platform administrator to create
    and manage applications, knowledge bases, documents, widget
    configuration, and testing.
2.  **Chat Widget** --- an embeddable client-side chat interface that
    runs on a client application website and communicates with the
    platform through the client APIs.

The frontend must consume the backend through stable REST APIs. Business
rules remain in the FastAPI backend; the frontend is responsible for
presentation, user interaction, API communication, client-side state,
and integration behavior.

The frontend should remain compact and understandable. The architecture
is organized by responsibility rather than creating a large number of
folders or abstractions before they are needed.

------------------------------------------------------------------------

## 2. Frontend Architecture

The frontend consists of two distinct runtime surfaces:

``` text
                         FRONTEND
                            |
              +-------------+-------------+
              |                           |
              v                           v
        ADMIN PORTAL                  CHAT WIDGET
         React + Vite                 widget.js
              |                           |
              |                           |
              +-------------+-------------+
                            |
                            v
                     FASTAPI REST API
                            |
              +-------------+-------------+
              |                           |
              v                           v
         ADMIN APIs                  CLIENT APIs
              |                           |
              v                           v
       Application                 Widget Session
       Knowledge Base              Conversation
       Documents                   Chat
       Settings
       Widget Configuration
```

The Admin Portal and Chat Widget share the same backend platform but
have different responsibilities and deployment behavior.

------------------------------------------------------------------------

## 3. Recommended Frontend Structure

The frontend should use the following compact structure:

``` text
frontend/
|
├── index.html
├── package.json
├── vite.config.js
├── eslint.config.js
|
├── public/
│   └── assets/
│       ├── hero.png
│       ├── favicon.svg
│       └── icons.svg
|
├── src/
│   ├── main.jsx
│   ├── App.js
│   ├── App.css
│   ├── index.css
│   |
│   ├── pages/
│   |
│   ├── components/
│   │   ├── Navbar.jsx
│   │   └── Sonner.jsx
│   |
│   ├── api/
│   |
│   └── utils/
|
└── widget/
    ├── index.html
    ├── widget.js
    └── widget.css
```

This is the baseline structure. New folders should only be introduced
when actual implementation requires them.

------------------------------------------------------------------------

## 4. Directory Responsibilities

### `index.html`

The Vite entry HTML for the Admin Portal.

Runtime:

``` text
index.html
    |
    v
main.jsx
    |
    v
App.js
    |
    v
React Admin Portal
```

### `src/main.jsx`

The React application entry point.

Its responsibility is to:

-   Load global CSS.
-   Initialize the React application.
-   Mount `App.js`.
-   Register application-level providers when required.

It should not contain business logic.

### `src/App.js`

The root React application component.

Its responsibility is to provide the main application shell and
route/page composition.

It should not contain backend business logic.

### `src/App.css`

Application-level styling.

### `src/index.css`

Global styles, base typography, reset rules, and global CSS variables.

------------------------------------------------------------------------

# 5. Pages

The `pages/` directory contains complete user-facing screens.

``` text
src/pages/
├── Login.jsx
├── Dashboard.jsx
├── ApplicationDetail.jsx
└── Chat.jsx
```

### `Login.jsx`

Admin authentication screen.

Responsibilities:

-   Collect admin credentials.
-   Submit authentication request.
-   Display validation and authentication errors.
-   Store/establish the frontend authentication state.
-   Redirect to the protected admin area after successful
    authentication.

### `Dashboard.jsx`

Main admin overview screen.

It can display information such as:

-   Application count.
-   Knowledge-base status.
-   Document processing status.
-   Recent operational information.
-   Basic platform status.

### `ApplicationDetail.jsx`

Application management screen.

It will eventually cover:

-   Application metadata.
-   Application status.
-   Knowledge base information.
-   Application configuration.
-   Widget configuration entry.
-   Credential management where permitted.
-   Related documents.

### `Chat.jsx`

Admin testing console.

The administrator can select an application and test questions against
the application's knowledge base.

Expected flow:

``` text
Select Application
       |
       v
Enter Question
       |
       v
Client Chat API
       |
       v
FastAPI
       |
       v
Hybrid RAG
       |
       v
Answer + Citations
       |
       v
Render Result
```

------------------------------------------------------------------------

# 6. Shared Components

The `components/` directory contains UI elements reused by multiple
pages.

``` text
src/components/
├── Navbar.jsx
└── Sonner.jsx
```

### `Navbar.jsx`

Shared admin navigation.

### `Sonner.jsx`

Shared notification/toast presentation.

Reusable UI should be placed here only when it is genuinely shared. Do
not create a component for every small HTML element.

------------------------------------------------------------------------

# 7. API Layer

The `api/` directory is the frontend boundary to the FastAPI backend.

``` text
src/api/
```

The important architectural rule is:

``` text
React Component
      |
      v
Feature API module
      |
      v
Central API Client
      |
      v
FastAPI REST API
```

React components should not contain repeated raw HTTP configuration.

### `client.js`

Central HTTP client.

Responsibilities:

-   Base API URL.
-   Request configuration.
-   Authentication headers.
-   Common headers.
-   Response handling.
-   Common error handling.
-   Request ID handling when applicable.

### `application management`

Application API operations.
Request/response shapes:

Create:

json

// POST /api/admin/applications
{
  "name": "My App",
  "description": "Support chatbot",
  "client_type": "website",
  "allowed_origins": ["https://my-site.com"]
}
Response includes API key once:

json

{
  "application": {
    "id": "...",
    "name": "My App",
    "slug": "my-app",
    "client_type": "website",
    "allowed_origins": ["https://my-site.com"],
    "is_active": true,
    "created_at": "...",
    "updated_at": "..."
  },
  "api_key": "akp_my-app_...",
  "api_key_prefix": "akp_my-app_"
}
Examples:

``` text
POST   /api/admin/applications
GET    /api/admin/applications
GET    /api/admin/applications/{application_id}
PUT    /api/admin/applications/{application_id}
DELETE /api/admin/applications/{application_id} #deactive application
```

Frontend pages/features:

Applications list page:

Table with: name, slug, client_type, is_active, created_at.

“Create Application” button.

Row actions: View / Edit / Deactivate.

Create/Edit Application form:

Fields: name, description (optional), client_type, allowed_origins (multi-value).

On create: show the generated api_key once with a “copy” button and a warning that it cannot be viewed again.

Application detail view:

Show all fields.

Show API key prefix (not full key).

Link to: Knowledge Base / Documents / Widgets / Settings for that application.

3. Knowledge base & documents (ingestion UI)
Backend endpoints (from documents.py and ingestion router):

text

POST /api/admin/documents/upload          # multipart form
POST /api/admin/documents                 # create from URL / source
GET  /api/admin/documents?knowledge_base_id=...&status=...
GET  /api/admin/documents/{document_id}
PUT  /api/admin/documents/{document_id}
POST /api/admin/documents/{document_id}/processing
POST /api/admin/documents/{document_id}/ready
POST /api/admin/documents/{document_id}/failed
POST /api/admin/documents/{document_id}/archive
Upload example:

text

POST /api/admin/documents/upload
Authorization: Basic ...
Content-Type: multipart/form-data

knowledge_base_id: <uuid>
title: "Product Guide"
description: "..."
file: <binary>
Frontend pages/features:

Knowledge Base / Documents page (per application):

List documents with: title, source_type, status (uploaded, processing, ready, failed, archived), created_at.

Filters: by status, by knowledge_base.

“Upload Document” button:

File upload (PDF, DOCX, etc.).

Or “Add from URL” / “Add from CSV” depending on your supported source types.

Document detail:

Metadata (title, description, source_type, source_uri, status, failure_reason).

Actions: Re-process, Mark as ready/failed, Archive.

Optional: show ingestion progress / status polling.

This is the main UI for feeding knowledge into each application.

4. Widgets management
You already have:

Schema: CreateWidgetRequest, UpdateWidgetRequest, WidgetResponse, PublicWidgetConfigurationResponse.

Admin router: /api/admin/widgets (included in api_router).

Client config endpoint: GET /api/client/widget/configuration with X-Widget-Key.

Assuming standard CRUD patterns (consistent with applications/documents), the admin widget endpoints will be:

text

POST   /api/admin/widgets
GET    /api/admin/widgets?application_id=...
GET    /api/admin/widgets/{widget_id}
PUT    /api/admin/widgets/{widget_id}
DELETE /api/admin/widgets/{widget_id}  # or deactivate
WidgetResponse includes:

json

{
  "id": "...",
  "application_id": "...",
  "display_name": "Support Widget",
  "public_key": "wk_...",
  "theme": "light",
  "launcher_label": "Chat with us",
  "welcome_message": "Hi!",
  "placeholder_text": "Type your message...",
  "is_enabled": true,
  "created_at": "...",
  "updated_at": "..."
}
Frontend pages/features:

Widgets list (per application):

Table with: display_name, theme, is_enabled, created_at.

“Create Widget” button.

Row actions: Edit, Copy public key, Enable/Disable, Delete.

Create/Edit Widget form:

Fields:

application_id (selected from existing apps if global, or implicit if inside an app).

display_name

theme (e.g., light/dark or future options)

launcher_label (optional)

welcome_message (optional)

placeholder_text (optional)

is_enabled (checkbox)

On create: show public_key once with copy button.

Widget detail view:

Show all config fields.

Show public_key (masked/unmasked).

Show integration snippet:

js

CHATBOT_API_BASE_URL = "https://your-backend.com/api";
CHATBOT_WIDGET_KEY = "wk_...";
Link to “Test Widget” page (your minimal HTML harness).

5. Settings (optional but useful)
You have a settings module and admin settings router. Frontend can expose:

Per-application settings page:

Toggle features (if you add more flags later).

Configure retention, max context length, etc., once you expose them via settings endpoints.

6. Conversations & monitoring (optional phase 2)
Admin conversations endpoints exist:

text

GET /api/admin/conversations?application_id=...
GET /api/admin/conversations/{conversation_id}
Frontend (later) can provide:

Conversations list per application:

conversation_identity, last message preview, created_at, updated_at.

Conversation detail:

Full message thread.

Useful for support QA and debugging.

7. Suggested frontend structure
A minimal but complete admin UI:

Login

Dashboard (optional)

Applications

List

Create / Edit

Detail

Knowledge Base / Documents

Widgets

Settings

(Later) Conversations

Global Widgets (optional, if you want cross-app view)

(Later) System settings / health

8. Integration flow for an admin user
In practice, the admin workflow will be:

Log in to admin panel.

Create an Application.

Copy the API key (for backend integrations).

Go to the application’s Documents page and upload knowledge.

Wait for documents to become ready.

Create a Widget for that application.

Copy the widget’s public_key.

Configure allowed origins on the application.

Use the widget key in your frontend test page or embedded widget.

Document API operations.

Examples:

``` text
Upload document
Get document
List documents
Start ingestion
Get ingestion status
Retry ingestion
Delete document
```

### `chat.js`

Client/admin chat API operations.

Examples:

``` text
Send message
Create or resolve conversation
Get conversation history
Close conversation
```

### `widgets.js`

Widget configuration and initialization-related API operations.

Examples:

``` text
Get widget configuration
Update widget configuration
Generate public widget key
Rotate public widget key
Validate widget initialization
```

The exact endpoint paths and request/response fields must follow the
backend OpenAPI contract.

------------------------------------------------------------------------

# 8. Utilities

``` text
src/utils/
└── utils.js
```

Utilities contain small reusable frontend helpers that do not belong to
a particular business feature.

Examples may include:

-   Formatting.
-   Local storage helpers.
-   Client-side validation helpers.
-   Small transformation functions.

Do not turn `utils.js` into a general dumping ground. When the file
becomes large, split it according to actual responsibility.

------------------------------------------------------------------------

# 9. Public Assets

Static assets belong under:

``` text
public/assets/
```

Example:

``` text
public/assets/
├── hero.png
├── favicon.svg
└── icons.svg
```

Default Vite assets such as `react.svg` and `vite.svg` can be removed if
they are not used.

------------------------------------------------------------------------

# 10. Chat Widget

The widget is deliberately separated from the Admin Portal:

``` text
widget/
├── index.html
├── widget.js
└── widget.css
```

The widget is not another Admin Portal page. It is a distributable
client integration.

Its runtime responsibility is:

``` text
Customer Website
       |
       v
widget.js
       |
       v
Widget Initialization
       |
       v
Backend validates public widget key + origin
       |
       v
Widget Session
       |
       v
Conversation Identity
       |
       v
Chat API
       |
       v
FastAPI
       |
       v
Knowledge Retrieval + LLM
       |
       v
Answer + Citations
       |
       v
Widget UI
```

### `widget/widget.js`

The widget bootstrap/integration entry point.

It is responsible for:

-   Loading the widget.
-   Reading the public widget configuration/key.
-   Initializing the widget session.
-   Connecting the widget to the client API.
-   Creating or restoring conversation state.
-   Rendering or mounting the chat interface.

The actual customer integration should eventually be distributable
through a script such as:

``` html
<script src="https://platform.example/widget/widget.js"></script>
```

The public widget key must not be treated as a secret server credential.

### `widget/widget.css`

Widget-specific styling.

It should cover:

-   Launcher.
-   Chat panel.
-   Header.
-   Message list.
-   User/assistant messages.
-   Input.
-   Loading state.
-   Error state.
-   Citations.
-   Responsive behavior.
-   Theme customization.
-   Accessibility states.

Widget styles should remain isolated from Admin Portal styles as much as
practical.

### `widget/index.html`

Development/test entry page for the widget.

It is useful for testing the widget independently during development. It
is not the page that a customer embeds into their website.

------------------------------------------------------------------------

# 11. Frontend-to-Backend Runtime Architecture

## Admin Portal

``` text
Admin Browser
      |
      v
React Admin Portal
      |
      v
Page
      |
      v
API Feature Module
      |
      v
API Client
      |
      | HTTP/JSON
      v
FastAPI
      |
      v
Admin Security
      |
      v
Application Service
      |
      v
Repository / Knowledge Pipeline
      |
      v
Database / Storage / AI Providers
```

## Client Widget

``` text
Client Website
      |
      v
widget.js
      |
      v
Widget Initialization
      |
      v
Public Widget Key + Origin
      |
      v
FastAPI Client API
      |
      v
Widget Session
      |
      v
Conversation Identity
      |
      v
Chat Request
      |
      v
Application Resolution
      |
      v
Knowledge Base Resolution
      |
      v
Conversation Resolution
      |
      v
Hybrid RAG
      |
      v
Answer + Citations
      |
      v
Widget UI
```

------------------------------------------------------------------------

# 12. Frontend-to-Backend Business Mapping

The frontend should map to backend capabilities rather than duplicate
backend internals.

``` text
Backend Capability             Frontend Responsibility
----------------------------------------------------------------
Application                     Application management screens
Knowledge Base                  Knowledge base information
Document                        Upload and document management
Ingestion                       Status, retry, processing display
Conversation                     loads conversation history
Chat                            Question/answer interface
Widget                          Configuration and embed setup
Settings                        Configuration screens
Authentication                 Admin login/session handling
```

so, The frontend does not implement:

-   RAG retrieval logic.
-   Chunking.
-   Embedding generation.
-   Vector search.
-   Reranking.
-   Prompt construction.
-   LLM provider selection.
-   Database operations.

Those remain backend responsibilities.

------------------------------------------------------------------------

# 13. Admin Application Flow

The intended administrator workflow is:

``` text
Admin Login
    |
    v
Dashboard
    |
    v
Create Application
    |
    v
Backend creates:
    - Application
    - Knowledge Base
    - Default Settings
    - Application Credentials
    |
    v
Application Detail
    |
    +----> Configure Widget
    |
    +----> Upload Documents
    |
    +----> Monitor Ingestion
    |
    +----> Test Questions
    |
    v
Application Ready
    |
    v
Copy Widget Embed Code
```

The frontend only initiates and displays these operations. The backend
owns the actual business workflow.

------------------------------------------------------------------------

# 14. Document Management Flow

``` text
Admin selects document
        |
        v
Frontend upload
        |
        v
POST document/upload
        |
        v
Backend stores source
        |
        v
Ingestion Job
        |
        v
Parsing
        |
        v
Normalization
        |
        v
Smart Chunking
        |
        v
Metadata Enrichment
        |
        v
Embedding
        |
        v
Vector Indexing
        |
        v
Document Ready
        |
        v
Frontend displays status
```
------------------------------------------------------------------------

# 15. Chat Flow

``` text
Visitor enters question
        |
        v
Widget
        |
        v
Chat API
        |
        v
Backend validates widget session
        |
        v
Resolve Application
        |
        v
Resolve Conversation
        |
        v
Load recent conversation context
        |
        v
Hybrid Retrieval
        |
        v
Metadata Filtering
        |
        v
Reranking
        |
        v
Context Builder
        |
        v
LLM
        |
        v
Citation Builder
        |
        v
Persist Messages
        |
        v
Return Answer + Citations + Conversation ID
        |
        v
Widget renders response
```

------------------------------------------------------------------------

# 16. Conversation Identity

The frontend widget does not create a platform User account.

For anonymous visitors, the widget can maintain an external conversation
identity.

Conceptually:

``` text
Visitor
   |
   v
Browser Session
   |
   v
Conversation Identity
   |
   v
Backend
   |
   v
Conversation
```

The widget should retain the returned `conversation_id` and reuse it for
subsequent messages while the conversation remains active.

The backend remains responsible for:

-   Conversation ownership.
-   Application isolation.
-   Conversation lifecycle.
-   Message persistence.
-   Inactivity rules.
-   Retention policies.

------------------------------------------------------------------------

# 17. Security Responsibilities

## Admin Portal

The frontend must:

-   Authenticate through the backend.
-   Maintain the admin session according to the backend contract.
-   Protect admin routes.
-   Handle expired sessions.
-   Redirect unauthenticated users.
-   Avoid storing sensitive backend secrets in browser code.

## Widget

The frontend must:

-   Use only the public widget credential/configuration intended for
    browser use.
-   Never expose database credentials.
-   Never expose Supabase service-role credentials.
-   Never expose LLM provider secrets.
-   Never expose backend application secret API keys.
-   Initialize through the backend.
-   Maintain the widget session and conversation state.
-   Handle expired/invalid widget sessions.
-   Handle rate-limit and authorization errors.

------------------------------------------------------------------------

# 18. Environment Configuration

Development configuration should use Vite environment variables.

Example:

``` text
VITE_API_BASE_URL=http://localhost:8000
```

Use:

``` text
.env.example
.env
```

The frontend must never contain server-side secrets such as:

``` text
DATABASE_URL
SUPABASE_SERVICE_ROLE_KEY
OPENAI_API_KEY
ANTHROPIC_API_KEY
OLLAMA_SECRET
```

Only browser-safe configuration belongs in `VITE_*` variables.

------------------------------------------------------------------------

# 21. Frontend API Integration Rule

The frontend should not invent backend behavior.

The contract should be:

``` text
FastAPI
   |
   v
OpenAPI Contract
   |
   v
Frontend API Layer
   |
   v
React Components
```

For every API integration, define:

-   Request fields.
-   Response fields.
-   Authentication requirement.
-   HTTP status codes.
-   Error format.
-   Loading state.
-   Empty state.
-   Failure state.
-   Retry behavior.

The backend OpenAPI specification is the source of truth for endpoint
names and schemas.

------------------------------------------------------------------------

# 22. Error and Loading States

Every API-driven frontend screen should consider:

``` text
Initial
  |
  +--> Loading
  |
  +--> Success
  |
  +--> Empty
  |
  +--> Error
           |
           +--> Retry
```

For example, document ingestion:

``` text
Upload
  |
  v
Processing
  |
  +--> Ready
  |
  +--> Failed
          |
          v
        Retry
```

The frontend displays these states; the backend determines the actual
business status.



------------------------------------------------------------------------

# 23. Production Boundary

The final architecture should preserve this separation:

``` text
                    AI KNOWLEDGE PLATFORM
                           |
        +------------------+------------------+
        |                                     |
        v                                     v
   ADMIN PORTAL                         CLIENT WIDGET
   React application                    Embeddable JS
        |                                     |
        +------------------+------------------+
                           |
                           v
                    FASTAPI BACKEND
                           |
        +------------------+------------------+
        |                  |                  |
        v                  v                  v
   PostgreSQL          Storage           AI Providers
                                           |
                                  +--------+--------+
                                  |        |        |
                               Ollama   Cloud LLM  Embeddings
```

The frontend should remain a consumer of this backend architecture
rather than becoming responsible for backend business logic.

------------------------------------------------------------------------

# 24. Final Principle

The frontend should stay simple:

``` text
Pages
  ↓
Components
  ↓
API Modules
  ↓
FastAPI
```

The widget has its own integration boundary:

``` text
Client Website
  ↓
widget.js
  ↓
Client API
  ↓
FastAPI
```

The backend remains responsible for:

``` text
Application
Knowledge Base
Documents
Ingestion
Hybrid RAG
Retrieval
Reranking
LLM
Conversations
Citations
Security
Persistence
```

The frontend remains responsible for:

``` text
UI
Navigation
Forms
User Interaction
API Consumption
Session Presentation
Conversation UI
Widget Rendering
Loading/Error/Retry States
Responsive Design
Accessibility
```

This structure gives the project a clear separation without
over-engineering the frontend. New abstractions should be introduced
only when real feature complexity justifies them.