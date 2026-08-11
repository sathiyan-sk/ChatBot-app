# Development Setup

## Step 1 --- Create the React/Vite project

If a project does not already exist:

``` bash
npm create vite@latest frontend -- --template react
```

Then:

``` bash
cd frontend
npm install
```

Use:

``` text
React
JavaScript / JSX
ESLint
Vite
```

## Step 2 --- Install application dependencies

Core routing/data dependencies can be added as required:

``` bash
npm install react-router-dom @tanstack/react-query
```

Forms and validation:

``` bash
npm install react-hook-form zod @hookform/resolvers
```

Notifications:

``` bash
npm install sonner
```

Only install packages that are actually required by the implementation.

## Step 3 --- Bring in the existing UI

Move the existing files into the new structure without rewriting their
behavior first.

Example:

``` text
Existing                     Target
------------------------------------------------
App.js                       src/App.js
main.jsx                     src/main.jsx
App.css                      src/App.css
index.css                    src/index.css
Login.jsx                    src/pages/Login.jsx
Dashboard.jsx                src/pages/Dashboard.jsx
ApplicationDetail.jsx        src/pages/ApplicationDetail.jsx
Chat.jsx                     src/pages/Chat.jsx
Navbar.jsx                   src/components/Navbar.jsx
sonner.jsx                   src/components/Sonner.jsx
```

Keep the existing `.js` files if they already work. Rename `.js` to
`.jsx` only when it improves clarity; it is not a prerequisite for
React.

## Step 4 --- Verify the UI before backend integration

Run:

``` bash
npm run dev
```

First make sure:

-   React starts.
-   Pages render.
-   Existing components render.
-   CSS loads.
-   Navigation works.
-   There are no import errors.